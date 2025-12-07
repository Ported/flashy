// Storage backend interface for player progress and session history.
import 'models.dart';

/// Abstract interface for storage backends.
///
/// Different platforms can implement this differently:
/// - Web: localStorage via shared_preferences
/// - Mobile: shared_preferences or local files
/// - Tests: In-memory mock storage
abstract class StorageBackend {
  /// Load player progress.
  ///
  /// Returns null if player has no saved progress.
  Future<PlayerProgress?> loadProgress(String playerName);

  /// Save player progress.
  Future<void> saveProgress(String playerName, PlayerProgress progress);

  /// List all player names.
  Future<List<String>> listPlayers();

  /// Delete a player and their progress.
  Future<void> deletePlayer(String playerName);

  /// Log a completed session (optional).
  ///
  /// Default implementation does nothing. Subclasses can override
  /// to log session history for analytics or debugging.
  Future<void> logSession(LevelResult result) async {}
}

/// In-memory storage backend for testing.
class MemoryStorageBackend implements StorageBackend {
  final Map<String, PlayerProgress> _players = {};
  final List<LevelResult> _sessions = [];

  @override
  Future<PlayerProgress?> loadProgress(String playerName) async {
    return _players[playerName];
  }

  @override
  Future<void> saveProgress(String playerName, PlayerProgress progress) async {
    _players[playerName] = progress;
  }

  @override
  Future<List<String>> listPlayers() async {
    return _players.keys.toList();
  }

  @override
  Future<void> deletePlayer(String playerName) async {
    _players.remove(playerName);
  }

  @override
  Future<void> logSession(LevelResult result) async {
    _sessions.add(result);
  }

  /// Get all logged sessions (for testing).
  List<LevelResult> get sessions => List.unmodifiable(_sessions);

  /// Clear all data (for testing).
  void clear() {
    _players.clear();
    _sessions.clear();
  }
}
