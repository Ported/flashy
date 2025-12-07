// Game flow state machine - defines screen transitions.
//
// This module owns all navigation logic. Screens emit events, and GameFlow
// determines what screen to show next. This ensures consistent game flow
// across all platforms (web, iOS, Android).
import 'levels.dart';
import 'models.dart';
import 'worlds.dart';

/// All possible screens in the game.
enum Screen {
  playerSelect,
  newPlayer,
  intro,
  worldIntro,
  worldMap,
  friendMeet,
  bossIntro,
  gameplay,
  result,
  bossVictory,
  gameComplete,
}

/// Request to show a specific screen with parameters.
class ScreenRequest {
  const ScreenRequest(this.screen, [this.params = const {}]);

  final Screen screen;
  final Map<String, dynamic> params;

  @override
  String toString() => 'ScreenRequest(${screen.name}, $params)';
}

// --- Events that trigger screen transitions ---

/// Base class for game events.
sealed class GameEvent {
  const GameEvent();
}

/// App has started.
class AppStarted extends GameEvent {
  const AppStarted();
}

/// Player selected from player list.
class PlayerSelected extends GameEvent {
  const PlayerSelected(this.playerName, {required this.isNewPlayer});

  final String playerName;
  final bool isNewPlayer;
}

/// New player profile created.
class NewPlayerCreated extends GameEvent {
  const NewPlayerCreated(this.playerName);

  final String playerName;
}

/// Intro story screen dismissed.
class IntroDismissed extends GameEvent {
  const IntroDismissed(this.playerName);

  final String playerName;
}

/// World intro story screen dismissed.
class WorldIntroDismissed extends GameEvent {
  const WorldIntroDismissed(this.playerName, {required this.worldNumber});

  final String playerName;
  final int worldNumber;
}

/// Level selected from world map.
class LevelSelected extends GameEvent {
  const LevelSelected(this.playerName, {required this.levelNumber});

  final String playerName;
  final int levelNumber;
}

/// Friend meet story screen dismissed.
class FriendMeetDismissed extends GameEvent {
  const FriendMeetDismissed(this.playerName, {required this.levelNumber});

  final String playerName;
  final int levelNumber;
}

/// Boss intro story screen dismissed.
class BossIntroDismissed extends GameEvent {
  const BossIntroDismissed(this.playerName, {required this.levelNumber});

  final String playerName;
  final int levelNumber;
}

/// Level gameplay completed.
class LevelCompleted extends GameEvent {
  const LevelCompleted({
    required this.playerName,
    required this.levelNumber,
    required this.stars,
    required this.isNewBest,
    required this.correct,
    required this.total,
    required this.score,
    required this.bestStreak,
  });

  final String playerName;
  final int levelNumber;
  final int stars;
  final bool isNewBest;
  final int correct;
  final int total;
  final int score;
  final int bestStreak;
}

/// Continue button pressed on result screen.
class ResultContinue extends GameEvent {
  const ResultContinue({
    required this.playerName,
    required this.levelNumber,
    required this.stars,
  });

  final String playerName;
  final int levelNumber;
  final int stars;
}

/// Replay button pressed on result screen.
class ResultReplay extends GameEvent {
  const ResultReplay({required this.playerName, required this.levelNumber});

  final String playerName;
  final int levelNumber;
}

/// Boss victory screen dismissed.
class BossVictoryDismissed extends GameEvent {
  const BossVictoryDismissed({
    required this.playerName,
    required this.worldNumber,
  });

  final String playerName;
  final int worldNumber;
}

/// Game complete screen dismissed.
class GameCompleteDismissed extends GameEvent {
  const GameCompleteDismissed();
}

/// Determines screen transitions based on game events.
///
/// This is the single source of truth for game navigation. All platforms
/// should use this to ensure consistent behavior.
class GameFlow {
  /// Handle a game event and return the next screen to show.
  ///
  /// [event] The game event that occurred.
  /// [progress] Player's current progress (needed for some transitions).
  ///
  /// Returns ScreenRequest indicating which screen to show next.
  ScreenRequest handle(GameEvent event, [PlayerProgress? progress]) {
    switch (event) {
      case AppStarted():
        return const ScreenRequest(Screen.playerSelect);

      case PlayerSelected(:final playerName, :final isNewPlayer):
        if (isNewPlayer) {
          return const ScreenRequest(Screen.newPlayer);
        }
        // Existing player - check if they've played before
        if (progress != null && progress.getHighestUnlocked() > 1) {
          return ScreenRequest(Screen.worldMap, {'player_name': playerName});
        }
        // New-ish player, show intro
        return ScreenRequest(Screen.intro, {'player_name': playerName});

      case NewPlayerCreated(:final playerName):
        return ScreenRequest(Screen.intro, {'player_name': playerName});

      case IntroDismissed(:final playerName):
        return ScreenRequest(Screen.worldIntro, {
          'player_name': playerName,
          'world_number': 1,
        });

      case WorldIntroDismissed(:final playerName, :final worldNumber):
        return ScreenRequest(Screen.worldMap, {
          'player_name': playerName,
          'world_number': worldNumber,
        });

      case LevelSelected(:final playerName, :final levelNumber):
        final level = getLevel(levelNumber);
        if (level == null) {
          return ScreenRequest(Screen.worldMap, {'player_name': playerName});
        }

        // Check for story screens before certain levels
        if (level.levelInWorld == 6) {
          // Friend meet before level 6
          return ScreenRequest(Screen.friendMeet, {
            'player_name': playerName,
            'world_number': level.worldNumber,
            'level_number': levelNumber,
          });
        }
        if (level.levelInWorld == 10) {
          // Boss intro before level 10
          return ScreenRequest(Screen.bossIntro, {
            'player_name': playerName,
            'world_number': level.worldNumber,
            'level_number': levelNumber,
          });
        }

        // Regular level - go straight to gameplay
        return ScreenRequest(Screen.gameplay, {
          'player_name': playerName,
          'level_number': levelNumber,
        });

      case FriendMeetDismissed(:final playerName, :final levelNumber):
        return ScreenRequest(Screen.gameplay, {
          'player_name': playerName,
          'level_number': levelNumber,
        });

      case BossIntroDismissed(:final playerName, :final levelNumber):
        return ScreenRequest(Screen.gameplay, {
          'player_name': playerName,
          'level_number': levelNumber,
        });

      case LevelCompleted(
          :final playerName,
          :final levelNumber,
          :final stars,
          :final isNewBest,
          :final correct,
          :final total,
          :final score,
          :final bestStreak
        ):
        return ScreenRequest(Screen.result, {
          'player_name': playerName,
          'level_number': levelNumber,
          'stars': stars,
          'is_new_best': isNewBest,
          'correct': correct,
          'total': total,
          'score': score,
          'best_streak': bestStreak,
        });

      case ResultContinue(:final playerName, :final levelNumber, :final stars):
        final level = getLevel(levelNumber);
        if (level != null && level.levelInWorld == 10 && stars >= 2) {
          // Beat the boss! Show victory screen
          return ScreenRequest(Screen.bossVictory, {
            'player_name': playerName,
            'world_number': level.worldNumber,
          });
        }

        // Regular continue - back to world map
        final nextLevel = stars >= 2 ? levelNumber + 1 : levelNumber;
        return ScreenRequest(Screen.worldMap, {
          'player_name': playerName,
          'selected_level': nextLevel,
        });

      case ResultReplay(:final playerName, :final levelNumber):
        return ScreenRequest(Screen.gameplay, {
          'player_name': playerName,
          'level_number': levelNumber,
        });

      case BossVictoryDismissed(:final playerName, :final worldNumber):
        final nextWorld = getWorld(worldNumber + 1);
        if (nextWorld != null) {
          // More worlds to explore
          return ScreenRequest(Screen.worldIntro, {
            'player_name': playerName,
            'world_number': worldNumber + 1,
          });
        }
        // All worlds complete!
        return ScreenRequest(Screen.gameComplete, {'player_name': playerName});

      case GameCompleteDismissed():
        return const ScreenRequest(Screen.playerSelect);
    }
  }
}
