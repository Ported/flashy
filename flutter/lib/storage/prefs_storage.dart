// SharedPreferences storage backend for web and mobile.
//
// Uses the same localStorage keys as the Python web version for data
// continuity when migrating from Python to Flutter on web.
import 'dart:convert';

import 'package:shared_preferences/shared_preferences.dart';

import '../core/models.dart';
import '../core/storage.dart';

/// Storage backend using SharedPreferences.
///
/// On web, SharedPreferences uses localStorage with the same keys as the
/// Python implementation, allowing seamless data migration.
///
/// Data is stored with the following keys:
/// - flashy_players: List of player names (JSON array)
/// - flashy_player_{name}: Player progress (JSON object)
/// - flashy_token_{name}: Player token for API authentication
/// - flashy_history: Array of session log entries (JSON array)
class PrefsStorageBackend implements StorageBackend {
  PrefsStorageBackend._(this._prefs);

  final SharedPreferences _prefs;

  /// Create a PrefsStorageBackend instance.
  ///
  /// Must be awaited since SharedPreferences.getInstance() is async.
  static Future<PrefsStorageBackend> create() async {
    final prefs = await SharedPreferences.getInstance();
    return PrefsStorageBackend._(prefs);
  }

  // Storage keys (matching Python web implementation)
  static const _playersKey = 'flashy_players';
  static String _playerKey(String name) => 'flashy_player_$name';
  static String _tokenKey(String name) => 'flashy_token_$name';
  static const _historyKey = 'flashy_history';

  @override
  Future<PlayerProgress?> loadProgress(String playerName) async {
    final dataStr = _prefs.getString(_playerKey(playerName));
    if (dataStr == null) {
      return null;
    }

    try {
      final data = json.decode(dataStr) as Map<String, dynamic>;

      // Parse stars (keys are strings in JSON, need to convert to int)
      final starsJson = data['stars'] as Map<String, dynamic>? ?? {};
      final stars = <int, int>{};
      for (final entry in starsJson.entries) {
        stars[int.parse(entry.key)] = entry.value as int;
      }

      // Parse best_scores
      final scoresJson = data['best_scores'] as Map<String, dynamic>? ?? {};
      final bestScores = <int, int>{};
      for (final entry in scoresJson.entries) {
        bestScores[int.parse(entry.key)] = entry.value as int;
      }

      return PlayerProgress(stars: stars, bestScores: bestScores);
    } catch (e) {
      // Invalid data format, return null
      return null;
    }
  }

  @override
  Future<void> saveProgress(String playerName, PlayerProgress progress) async {
    // Ensure player is in the players list
    final players = await listPlayers();
    if (!players.contains(playerName)) {
      final updatedPlayers = [...players, playerName];
      await _prefs.setString(_playersKey, json.encode(updatedPlayers));
    }

    // Convert int keys to string keys for JSON
    final starsJson = <String, int>{};
    for (final entry in progress.stars.entries) {
      starsJson[entry.key.toString()] = entry.value;
    }

    final scoresJson = <String, int>{};
    for (final entry in progress.bestScores.entries) {
      scoresJson[entry.key.toString()] = entry.value;
    }

    final data = {
      'stars': starsJson,
      'best_scores': scoresJson,
    };

    await _prefs.setString(_playerKey(playerName), json.encode(data));
  }

  @override
  Future<List<String>> listPlayers() async {
    final playersStr = _prefs.getString(_playersKey);
    if (playersStr == null) {
      return [];
    }

    try {
      final list = json.decode(playersStr) as List<dynamic>;
      return list.cast<String>();
    } catch (e) {
      return [];
    }
  }

  @override
  Future<void> deletePlayer(String playerName) async {
    // Remove from players list
    final players = await listPlayers();
    players.remove(playerName);
    await _prefs.setString(_playersKey, json.encode(players));

    // Remove player data
    await _prefs.remove(_playerKey(playerName));
    await _prefs.remove(_tokenKey(playerName));
  }

  @override
  Future<void> logSession(LevelResult result) async {
    final historyStr = _prefs.getString(_historyKey) ?? '[]';
    List<dynamic> history;
    try {
      history = json.decode(historyStr) as List<dynamic>;
    } catch (e) {
      history = [];
    }

    final entry = {
      'timestamp': DateTime.now().toIso8601String(),
      'level_number': result.levelNumber,
      'level_name': result.levelName,
      'score': result.totalScore,
      'correct': result.correctCount,
      'total': result.totalProblems,
      'best_streak': result.bestStreak,
      'time_seconds': result.totalTimeSeconds,
      'problems': result.problems.map((p) => p.toJson()).toList(),
    };

    history.add(entry);
    await _prefs.setString(_historyKey, json.encode(history));
  }

  /// Load session history.
  Future<List<Map<String, dynamic>>> loadHistory() async {
    final historyStr = _prefs.getString(_historyKey) ?? '[]';
    try {
      final list = json.decode(historyStr) as List<dynamic>;
      return list.cast<Map<String, dynamic>>();
    } catch (e) {
      return [];
    }
  }

  /// Save a player's authentication token.
  Future<void> saveToken(String playerName, String token) async {
    await _prefs.setString(_tokenKey(playerName), token);
  }

  /// Load a player's authentication token.
  Future<String?> loadToken(String playerName) async {
    return _prefs.getString(_tokenKey(playerName));
  }

  /// Check if a player exists locally.
  Future<bool> playerExists(String playerName) async {
    final players = await listPlayers();
    return players.contains(playerName);
  }

  /// Clear all storage (for testing/debugging).
  Future<void> clearAll() async {
    await _prefs.clear();
  }
}
