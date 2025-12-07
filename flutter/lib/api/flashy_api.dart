// API client for Cloudflare Functions backend.
//
// Handles player registration and leaderboard operations.
import 'dart:convert';

import 'package:http/http.dart' as http;

/// Result of player registration.
class RegisterResult {
  const RegisterResult({
    required this.success,
    this.playerName,
    this.token,
    this.error,
  });

  final bool success;
  final String? playerName;
  final String? token;
  final String? error;

  /// Check if the name was already taken.
  bool get nameTaken => error == 'Name already taken';
}

/// A leaderboard entry.
class LeaderboardEntry {
  const LeaderboardEntry({
    required this.rank,
    required this.playerName,
    required this.totalScore,
    required this.highestLevel,
    required this.totalStars,
  });

  final int rank;
  final String playerName;
  final int totalScore;
  final int highestLevel;
  final int totalStars;

  factory LeaderboardEntry.fromJson(Map<String, dynamic> json) {
    return LeaderboardEntry(
      rank: json['rank'] as int,
      playerName: json['player_name'] as String,
      totalScore: json['total_score'] as int,
      highestLevel: json['highest_level'] as int,
      totalStars: json['total_stars'] as int,
    );
  }
}

/// Result of score sync.
class SyncResult {
  const SyncResult({
    required this.success,
    this.rank,
    this.error,
  });

  final bool success;
  final int? rank;
  final String? error;
}

/// API client for the Flashy backend.
///
/// Communicates with Cloudflare Functions for:
/// - Player registration (POST /api/register)
/// - Name availability check (GET /api/register?name=X)
/// - Leaderboard fetch (GET /api/leaderboard)
/// - Score sync (POST /api/leaderboard)
class FlashyApi {
  FlashyApi({
    String? baseUrl,
    http.Client? client,
  })  : _baseUrl = baseUrl ?? '',
        _client = client ?? http.Client();

  final String _baseUrl;
  final http.Client _client;

  /// Check if a player name is available.
  ///
  /// Returns true if the name is available for registration.
  Future<bool> checkNameAvailable(String name) async {
    try {
      final uri = Uri.parse('$_baseUrl/api/register').replace(
        queryParameters: {'name': name},
      );
      final response = await _client.get(uri);

      if (response.statusCode == 200) {
        final data = json.decode(response.body) as Map<String, dynamic>;
        return data['available'] as bool? ?? false;
      }
      return false;
    } catch (e) {
      return false;
    }
  }

  /// Register a new player name.
  ///
  /// Returns a RegisterResult with the token if successful.
  Future<RegisterResult> register(String name) async {
    try {
      final uri = Uri.parse('$_baseUrl/api/register');
      final response = await _client.post(
        uri,
        headers: {'Content-Type': 'application/json'},
        body: json.encode({'player_name': name}),
      );

      final data = json.decode(response.body) as Map<String, dynamic>;

      if (response.statusCode == 200) {
        return RegisterResult(
          success: true,
          playerName: data['player_name'] as String?,
          token: data['token'] as String?,
        );
      } else {
        return RegisterResult(
          success: false,
          error: data['error'] as String?,
        );
      }
    } catch (e) {
      return RegisterResult(
        success: false,
        error: 'Network error: $e',
      );
    }
  }

  /// Fetch the leaderboard.
  ///
  /// Returns top 50 players sorted by total score.
  Future<List<LeaderboardEntry>> getLeaderboard() async {
    try {
      final uri = Uri.parse('$_baseUrl/api/leaderboard');
      final response = await _client.get(uri);

      if (response.statusCode == 200) {
        final data = json.decode(response.body) as Map<String, dynamic>;
        final leaderboard = data['leaderboard'] as List<dynamic>? ?? [];
        return leaderboard
            .map((e) => LeaderboardEntry.fromJson(e as Map<String, dynamic>))
            .toList();
      }
      return [];
    } catch (e) {
      return [];
    }
  }

  /// Sync a player's score to the leaderboard.
  ///
  /// Returns a SyncResult with the player's rank if successful.
  Future<SyncResult> syncScore({
    required String playerName,
    required String token,
    required int totalScore,
    required int highestLevel,
    required int totalStars,
  }) async {
    try {
      final uri = Uri.parse('$_baseUrl/api/leaderboard');
      final response = await _client.post(
        uri,
        headers: {'Content-Type': 'application/json'},
        body: json.encode({
          'player_name': playerName,
          'token': token,
          'total_score': totalScore,
          'highest_level': highestLevel,
          'total_stars': totalStars,
        }),
      );

      final data = json.decode(response.body) as Map<String, dynamic>;

      if (response.statusCode == 200) {
        return SyncResult(
          success: true,
          rank: data['rank'] as int?,
        );
      } else {
        return SyncResult(
          success: false,
          error: data['error'] as String?,
        );
      }
    } catch (e) {
      return SyncResult(
        success: false,
        error: 'Network error: $e',
      );
    }
  }

  /// Close the HTTP client.
  void dispose() {
    _client.close();
  }
}
