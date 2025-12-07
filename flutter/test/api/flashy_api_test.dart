import 'dart:convert';

import 'package:flutter_test/flutter_test.dart';
import 'package:http/http.dart' as http;
import 'package:http/testing.dart';
import 'package:flashy_app/api/flashy_api.dart';

void main() {
  group('FlashyApi', () {
    group('checkNameAvailable', () {
      test('returns true when name is available', () async {
        final client = MockClient((request) async {
          expect(request.url.path, equals('/api/register'));
          expect(request.url.queryParameters['name'], equals('newplayer'));
          return http.Response(
            json.encode({'available': true, 'player_name': 'newplayer'}),
            200,
          );
        });

        final api = FlashyApi(client: client);
        final available = await api.checkNameAvailable('newplayer');
        expect(available, isTrue);
      });

      test('returns false when name is taken', () async {
        final client = MockClient((request) async {
          return http.Response(
            json.encode({'available': false, 'player_name': 'taken'}),
            200,
          );
        });

        final api = FlashyApi(client: client);
        final available = await api.checkNameAvailable('taken');
        expect(available, isFalse);
      });

      test('returns false on network error', () async {
        final client = MockClient((request) async {
          throw Exception('Network error');
        });

        final api = FlashyApi(client: client);
        final available = await api.checkNameAvailable('test');
        expect(available, isFalse);
      });
    });

    group('register', () {
      test('returns success with token', () async {
        final client = MockClient((request) async {
          expect(request.method, equals('POST'));
          expect(request.url.path, equals('/api/register'));
          final body = json.decode(request.body);
          expect(body['player_name'], equals('newplayer'));

          return http.Response(
            json.encode({
              'success': true,
              'player_name': 'newplayer',
              'token': 'abc-123-token',
            }),
            200,
          );
        });

        final api = FlashyApi(client: client);
        final result = await api.register('newplayer');
        expect(result.success, isTrue);
        expect(result.playerName, equals('newplayer'));
        expect(result.token, equals('abc-123-token'));
        expect(result.error, isNull);
      });

      test('returns error when name is taken', () async {
        final client = MockClient((request) async {
          return http.Response(
            json.encode({
              'error': 'Name already taken',
              'available': false,
            }),
            409,
          );
        });

        final api = FlashyApi(client: client);
        final result = await api.register('taken');
        expect(result.success, isFalse);
        expect(result.error, equals('Name already taken'));
        expect(result.nameTaken, isTrue);
      });

      test('returns error on network failure', () async {
        final client = MockClient((request) async {
          throw Exception('Connection refused');
        });

        final api = FlashyApi(client: client);
        final result = await api.register('test');
        expect(result.success, isFalse);
        expect(result.error, contains('Network error'));
      });
    });

    group('getLeaderboard', () {
      test('returns leaderboard entries', () async {
        final client = MockClient((request) async {
          expect(request.method, equals('GET'));
          expect(request.url.path, equals('/api/leaderboard'));

          return http.Response(
            json.encode({
              'leaderboard': [
                {
                  'rank': 1,
                  'player_name': 'TopPlayer',
                  'total_score': 50000,
                  'highest_level': 40,
                  'total_stars': 120,
                },
                {
                  'rank': 2,
                  'player_name': 'SecondPlace',
                  'total_score': 45000,
                  'highest_level': 38,
                  'total_stars': 110,
                },
              ],
            }),
            200,
          );
        });

        final api = FlashyApi(client: client);
        final leaderboard = await api.getLeaderboard();
        expect(leaderboard, hasLength(2));
        expect(leaderboard[0].rank, equals(1));
        expect(leaderboard[0].playerName, equals('TopPlayer'));
        expect(leaderboard[0].totalScore, equals(50000));
        expect(leaderboard[0].highestLevel, equals(40));
        expect(leaderboard[0].totalStars, equals(120));
        expect(leaderboard[1].rank, equals(2));
        expect(leaderboard[1].playerName, equals('SecondPlace'));
      });

      test('returns empty list on error', () async {
        final client = MockClient((request) async {
          return http.Response(
            json.encode({'error': 'Database error'}),
            500,
          );
        });

        final api = FlashyApi(client: client);
        final leaderboard = await api.getLeaderboard();
        expect(leaderboard, isEmpty);
      });

      test('returns empty list on network error', () async {
        final client = MockClient((request) async {
          throw Exception('Network error');
        });

        final api = FlashyApi(client: client);
        final leaderboard = await api.getLeaderboard();
        expect(leaderboard, isEmpty);
      });
    });

    group('syncScore', () {
      test('returns success with rank', () async {
        final client = MockClient((request) async {
          expect(request.method, equals('POST'));
          expect(request.url.path, equals('/api/leaderboard'));
          final body = json.decode(request.body);
          expect(body['player_name'], equals('TestPlayer'));
          expect(body['token'], equals('secret-token'));
          expect(body['total_score'], equals(5000));
          expect(body['highest_level'], equals(15));
          expect(body['total_stars'], equals(42));

          return http.Response(
            json.encode({
              'success': true,
              'rank': 5,
            }),
            200,
          );
        });

        final api = FlashyApi(client: client);
        final result = await api.syncScore(
          playerName: 'TestPlayer',
          token: 'secret-token',
          totalScore: 5000,
          highestLevel: 15,
          totalStars: 42,
        );
        expect(result.success, isTrue);
        expect(result.rank, equals(5));
        expect(result.error, isNull);
      });

      test('returns error on invalid token', () async {
        final client = MockClient((request) async {
          return http.Response(
            json.encode({'error': 'Invalid token for player'}),
            403,
          );
        });

        final api = FlashyApi(client: client);
        final result = await api.syncScore(
          playerName: 'TestPlayer',
          token: 'wrong-token',
          totalScore: 5000,
          highestLevel: 15,
          totalStars: 42,
        );
        expect(result.success, isFalse);
        expect(result.error, equals('Invalid token for player'));
      });

      test('returns error on network failure', () async {
        final client = MockClient((request) async {
          throw Exception('Network timeout');
        });

        final api = FlashyApi(client: client);
        final result = await api.syncScore(
          playerName: 'TestPlayer',
          token: 'secret-token',
          totalScore: 5000,
          highestLevel: 15,
          totalStars: 42,
        );
        expect(result.success, isFalse);
        expect(result.error, contains('Network error'));
      });
    });
  });

  group('LeaderboardEntry', () {
    test('fromJson creates entry correctly', () {
      final entry = LeaderboardEntry.fromJson({
        'rank': 3,
        'player_name': 'Player3',
        'total_score': 30000,
        'highest_level': 25,
        'total_stars': 75,
      });

      expect(entry.rank, equals(3));
      expect(entry.playerName, equals('Player3'));
      expect(entry.totalScore, equals(30000));
      expect(entry.highestLevel, equals(25));
      expect(entry.totalStars, equals(75));
    });
  });

  group('RegisterResult', () {
    test('nameTaken returns true for taken error', () {
      const result = RegisterResult(
        success: false,
        error: 'Name already taken',
      );
      expect(result.nameTaken, isTrue);
    });

    test('nameTaken returns false for other errors', () {
      const result = RegisterResult(
        success: false,
        error: 'Invalid player name',
      );
      expect(result.nameTaken, isFalse);
    });
  });
}
