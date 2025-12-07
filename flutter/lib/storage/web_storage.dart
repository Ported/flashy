// Web-specific storage backend using raw localStorage.
//
// Uses the same localStorage keys as the Python web version for seamless
// data migration. This bypasses SharedPreferences to avoid encoding issues.

import 'dart:convert';
import 'package:web/web.dart' as web;

import '../core/models.dart';
import '../core/storage.dart';

/// Storage backend using raw localStorage for web.
///
/// This implementation directly accesses localStorage without any prefix
/// or encoding, making it fully compatible with the Python web app.
class WebStorageBackend implements StorageBackend {
  WebStorageBackend._();

  static Future<WebStorageBackend> create() async {
    return WebStorageBackend._();
  }

  // Storage keys (matching Python web implementation)
  static const _playersKey = 'flashy_players';
  static String _playerKey(String name) => 'flashy_player_$name';
  static String _tokenKey(String name) => 'flashy_token_$name';
  static const _historyKey = 'flashy_history';

  String? _getItem(String key) {
    return web.window.localStorage.getItem(key);
  }

  void _setItem(String key, String value) {
    web.window.localStorage.setItem(key, value);
  }

  void _removeItem(String key) {
    web.window.localStorage.removeItem(key);
  }

  @override
  Future<PlayerProgress?> loadProgress(String playerName) async {
    final dataStr = _getItem(_playerKey(playerName));
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
      _setItem(_playersKey, json.encode(updatedPlayers));
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

    _setItem(_playerKey(playerName), json.encode(data));
  }

  @override
  Future<List<String>> listPlayers() async {
    final playersStr = _getItem(_playersKey);
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
    _setItem(_playersKey, json.encode(players));

    // Remove player data
    _removeItem(_playerKey(playerName));
    _removeItem(_tokenKey(playerName));
  }

  @override
  Future<void> logSession(LevelResult result) async {
    final historyStr = _getItem(_historyKey) ?? '[]';
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
    _setItem(_historyKey, json.encode(history));
  }

  /// Load session history.
  Future<List<Map<String, dynamic>>> loadHistory() async {
    final historyStr = _getItem(_historyKey) ?? '[]';
    try {
      final list = json.decode(historyStr) as List<dynamic>;
      return list.cast<Map<String, dynamic>>();
    } catch (e) {
      return [];
    }
  }

  @override
  Future<void> saveToken(String playerName, String token) async {
    _setItem(_tokenKey(playerName), token);
  }

  @override
  Future<String?> loadToken(String playerName) async {
    return _getItem(_tokenKey(playerName));
  }

  /// Check if a player exists locally.
  Future<bool> playerExists(String playerName) async {
    final players = await listPlayers();
    return players.contains(playerName);
  }

  /// Clear all flashy-related storage.
  Future<void> clearAll() async {
    final storage = web.window.localStorage;
    final keysToRemove = <String>[];

    for (var i = 0; i < storage.length; i++) {
      final key = storage.key(i);
      if (key != null && key.startsWith('flashy_')) {
        keysToRemove.add(key);
      }
    }

    for (final key in keysToRemove) {
      storage.removeItem(key);
    }
  }
}
