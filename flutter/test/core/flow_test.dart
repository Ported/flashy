import 'package:flutter_test/flutter_test.dart';
import 'package:flashy_app/core/flow.dart';
import 'package:flashy_app/core/models.dart';

void main() {
  late GameFlow flow;

  setUp(() {
    flow = GameFlow();
  });

  group('GameFlow', () {
    test('app started goes to player select', () {
      final result = flow.handle(const AppStarted());
      expect(result.screen, equals(Screen.playerSelect));
    });

    test('new player selected goes to new player', () {
      final result = flow.handle(
        const PlayerSelected('test', isNewPlayer: true),
      );
      expect(result.screen, equals(Screen.newPlayer));
    });

    test('existing player no progress goes to intro', () {
      final progress = PlayerProgress();
      final result = flow.handle(
        const PlayerSelected('test', isNewPlayer: false),
        progress,
      );
      expect(result.screen, equals(Screen.intro));
      expect(result.params['player_name'], equals('test'));
    });

    test('existing player with progress goes to world map', () {
      final progress = PlayerProgress(stars: {1: 3, 2: 2});
      final result = flow.handle(
        const PlayerSelected('test', isNewPlayer: false),
        progress,
      );
      expect(result.screen, equals(Screen.worldMap));
      expect(result.params['player_name'], equals('test'));
    });

    test('new player created goes to intro', () {
      final result = flow.handle(const NewPlayerCreated('newbie'));
      expect(result.screen, equals(Screen.intro));
      expect(result.params['player_name'], equals('newbie'));
    });

    test('intro dismissed goes to world intro', () {
      final result = flow.handle(const IntroDismissed('test'));
      expect(result.screen, equals(Screen.worldIntro));
      expect(result.params['world_number'], equals(1));
    });

    test('world intro dismissed goes to world map', () {
      final result = flow.handle(
        const WorldIntroDismissed('test', worldNumber: 2),
      );
      expect(result.screen, equals(Screen.worldMap));
      expect(result.params['world_number'], equals(2));
    });
  });

  group('Level selection', () {
    test('regular level goes to gameplay', () {
      final result = flow.handle(
        const LevelSelected('test', levelNumber: 1),
      );
      expect(result.screen, equals(Screen.gameplay));
      expect(result.params['level_number'], equals(1));
    });

    test('level 6 goes to friend meet', () {
      final result = flow.handle(
        const LevelSelected('test', levelNumber: 6),
      );
      expect(result.screen, equals(Screen.friendMeet));
      expect(result.params['level_number'], equals(6));
      expect(result.params['world_number'], equals(1));
    });

    test('level 16 goes to friend meet', () {
      // Level 16 is level 6 of world 2
      final result = flow.handle(
        const LevelSelected('test', levelNumber: 16),
      );
      expect(result.screen, equals(Screen.friendMeet));
      expect(result.params['level_number'], equals(16));
      expect(result.params['world_number'], equals(2));
    });

    test('level 10 goes to boss intro', () {
      final result = flow.handle(
        const LevelSelected('test', levelNumber: 10),
      );
      expect(result.screen, equals(Screen.bossIntro));
      expect(result.params['level_number'], equals(10));
    });

    test('friend meet dismissed goes to gameplay', () {
      final result = flow.handle(
        const FriendMeetDismissed('test', levelNumber: 6),
      );
      expect(result.screen, equals(Screen.gameplay));
      expect(result.params['level_number'], equals(6));
    });

    test('boss intro dismissed goes to gameplay', () {
      final result = flow.handle(
        const BossIntroDismissed('test', levelNumber: 10),
      );
      expect(result.screen, equals(Screen.gameplay));
      expect(result.params['level_number'], equals(10));
    });
  });

  group('Level completion', () {
    test('level completed goes to result', () {
      final result = flow.handle(
        const LevelCompleted(
          playerName: 'test',
          levelNumber: 1,
          stars: 3,
          isNewBest: true,
          correct: 10,
          total: 10,
          score: 1000,
          bestStreak: 10,
        ),
      );
      expect(result.screen, equals(Screen.result));
      expect(result.params['stars'], equals(3));
      expect(result.params['score'], equals(1000));
    });

    test('result continue regular goes to world map', () {
      final result = flow.handle(
        const ResultContinue(playerName: 'test', levelNumber: 5, stars: 2),
      );
      expect(result.screen, equals(Screen.worldMap));
      expect(result.params['selected_level'], equals(6)); // Next level
    });

    test('result continue failed stays on same level', () {
      final result = flow.handle(
        const ResultContinue(playerName: 'test', levelNumber: 5, stars: 1),
      );
      expect(result.screen, equals(Screen.worldMap));
      expect(result.params['selected_level'], equals(5)); // Same level
    });

    test('result continue boss victory goes to boss victory', () {
      final result = flow.handle(
        const ResultContinue(playerName: 'test', levelNumber: 10, stars: 3),
      );
      expect(result.screen, equals(Screen.bossVictory));
      expect(result.params['world_number'], equals(1));
    });

    test('result continue boss failed goes to world map', () {
      final result = flow.handle(
        const ResultContinue(playerName: 'test', levelNumber: 10, stars: 1),
      );
      expect(result.screen, equals(Screen.worldMap));
    });

    test('result replay goes to gameplay', () {
      final result = flow.handle(
        const ResultReplay(playerName: 'test', levelNumber: 5),
      );
      expect(result.screen, equals(Screen.gameplay));
      expect(result.params['level_number'], equals(5));
    });
  });

  group('Boss victory and game complete', () {
    test('boss victory world 1 goes to world 2 intro', () {
      final result = flow.handle(
        const BossVictoryDismissed(playerName: 'test', worldNumber: 1),
      );
      expect(result.screen, equals(Screen.worldIntro));
      expect(result.params['world_number'], equals(2));
    });

    test('boss victory world 3 goes to world 4 intro', () {
      final result = flow.handle(
        const BossVictoryDismissed(playerName: 'test', worldNumber: 3),
      );
      expect(result.screen, equals(Screen.worldIntro));
      expect(result.params['world_number'], equals(4));
    });

    test('boss victory final world goes to game complete', () {
      final result = flow.handle(
        const BossVictoryDismissed(playerName: 'test', worldNumber: 4),
      );
      expect(result.screen, equals(Screen.gameComplete));
    });

    test('game complete dismissed goes to player select', () {
      final result = flow.handle(const GameCompleteDismissed());
      expect(result.screen, equals(Screen.playerSelect));
    });
  });
}
