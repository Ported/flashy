import 'package:flutter/foundation.dart';

import '../api/flashy_api.dart';
import '../core/flow.dart';
import '../core/game.dart';
import '../core/models.dart';
import '../core/storage.dart';
import '../storage/prefs_storage.dart';

/// Central game state management.
///
/// Manages player state, navigation, and game sessions.
class GameState extends ChangeNotifier {
  GameState({
    StorageBackend? storage,
    FlashyApi? api,
  })  : _storage = storage,
        _api = api ?? FlashyApi(baseUrl: _getApiBaseUrl());

  /// Get the API base URL based on environment.
  static String _getApiBaseUrl() {
    // In debug mode, use local dev server
    if (kDebugMode) {
      return 'http://localhost:8765';
    }
    // In release, use relative URLs (same origin)
    return '';
  }

  StorageBackend? _storage;
  final FlashyApi _api;
  final GameFlow _flow = GameFlow();

  // Current state
  String? _currentPlayer;
  int _currentWorld = 1;
  PlayerProgress? _progress;
  GameController? _gameController;
  bool _isInitialized = false;

  // Getters
  String? get currentPlayer => _currentPlayer;
  int get currentWorld => _currentWorld;
  PlayerProgress? get progress => _progress;
  GameController? get gameController => _gameController;
  bool get isInitialized => _isInitialized;
  StorageBackend? get storage => _storage;
  FlashyApi get api => _api;
  GameFlow get flow => _flow;

  /// Initialize storage backend.
  Future<void> initialize() async {
    if (_isInitialized) return;

    _storage ??= await PrefsStorageBackend.create();
    _isInitialized = true;

    // Restore session if saved
    if (_storage is PrefsStorageBackend) {
      final prefsStorage = _storage as PrefsStorageBackend;
      final players = await prefsStorage.listPlayers();

      // Check for saved current player
      // For now, if there's exactly one player and they have a token, restore them
      // In the future, we could save/restore current player preference
      if (players.length == 1) {
        final token = await prefsStorage.loadToken(players.first);
        if (token != null) {
          await selectPlayer(players.first);
        }
      }
    }

    notifyListeners();
  }

  /// List all players.
  Future<List<String>> listPlayers() async {
    if (_storage == null) return [];
    return _storage!.listPlayers();
  }

  /// Select an existing player.
  Future<void> selectPlayer(String playerName) async {
    _currentPlayer = playerName;
    _progress = await _storage?.loadProgress(playerName);
    _progress ??= PlayerProgress();

    // Determine which world to show based on progress
    final highest = _progress!.getHighestUnlocked();
    _currentWorld = ((highest - 1) ~/ 10) + 1;
    if (_currentWorld < 1) _currentWorld = 1;
    if (_currentWorld > 4) _currentWorld = 4;

    notifyListeners();
  }

  /// Create a new player.
  ///
  /// Returns null on success, or error message on failure.
  Future<String?> createPlayer(String name) async {
    // Validate name
    final safeName = name.replaceAll(RegExp(r'[^a-zA-Z0-9 \-_]'), '').trim();
    if (safeName.isEmpty) {
      return 'Invalid name';
    }
    if (safeName.length > 20) {
      return 'Name too long (max 20 characters)';
    }

    // Check if exists locally
    final players = await listPlayers();
    if (players.contains(safeName)) {
      return 'Player "$safeName" already exists';
    }

    // Register with API
    final result = await _api.register(safeName);
    if (!result.success) {
      if (result.nameTaken) {
        return 'Name already taken';
      }
      return result.error ?? 'Registration failed';
    }

    // Save token and create local player
    if (_storage is PrefsStorageBackend && result.token != null) {
      await (_storage as PrefsStorageBackend).saveToken(safeName, result.token!);
    }

    _progress = PlayerProgress();
    await _storage?.saveProgress(safeName, _progress!);

    _currentPlayer = safeName;
    _currentWorld = 1;

    notifyListeners();
    return null;
  }

  /// Set current world for navigation.
  void setWorld(int worldNumber) {
    if (worldNumber < 1 || worldNumber > 4) return;
    _currentWorld = worldNumber;
    notifyListeners();
  }

  /// Navigate to previous world.
  void previousWorld() {
    if (_currentWorld > 1) {
      _currentWorld--;
      notifyListeners();
    }
  }

  /// Navigate to next world if unlocked.
  void nextWorld() {
    if (_currentWorld < 4 && canAccessWorld(_currentWorld + 1)) {
      _currentWorld++;
      notifyListeners();
    }
  }

  /// Check if a world is accessible.
  bool canAccessWorld(int worldNumber) {
    if (_progress == null) return worldNumber == 1;
    final highest = _progress!.getHighestUnlocked();
    final highestWorld = ((highest - 1) ~/ 10) + 1;
    return worldNumber <= highestWorld;
  }

  /// Start a new game for a level.
  void startLevel(int levelNumber) {
    _gameController = GameController(
      playerName: _currentPlayer!,
      levelNumber: levelNumber,
      storage: _storage,
    );
    notifyListeners();
  }

  /// End the current game.
  Future<(int, bool)> finishLevel() async {
    if (_gameController == null) {
      throw StateError('No active game');
    }

    final result = await _gameController!.finish();

    // Reload progress after save
    _progress = await _storage?.loadProgress(_currentPlayer!);
    _progress ??= PlayerProgress();

    // Sync score to leaderboard
    await _syncScore();

    notifyListeners();
    return result;
  }

  /// Sync current player's score to leaderboard.
  Future<int?> _syncScore() async {
    if (_currentPlayer == null || _progress == null) return null;

    String? token;
    if (_storage is PrefsStorageBackend) {
      token = await (_storage as PrefsStorageBackend).loadToken(_currentPlayer!);
    }
    if (token == null) return null;

    final result = await _api.syncScore(
      playerName: _currentPlayer!,
      token: token,
      totalScore: _progress!.getTotalBestScore(),
      highestLevel: _progress!.getHighestUnlocked(),
      totalStars: _progress!.stars.values.fold(0, (a, b) => a + b),
    );

    return result.success ? result.rank : null;
  }

  /// Clear game controller (after leaving gameplay).
  void clearGame() {
    _gameController = null;
    notifyListeners();
  }

  /// Log out current player.
  void logout() {
    _currentPlayer = null;
    _progress = null;
    _gameController = null;
    _currentWorld = 1;
    notifyListeners();
  }

  /// Handle a game flow event and return the next screen request.
  ScreenRequest handleEvent(GameEvent event) {
    return _flow.handle(event, _progress);
  }
}
