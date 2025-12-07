import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../core/levels.dart';
import '../l10n/app_localizations.dart';
import '../state/game_state.dart';
import '../theme/app_theme.dart';
import '../widgets/animated_button.dart';
import '../widgets/responsive_container.dart';
import 'boss_victory_screen.dart';
import 'gameplay_screen.dart';
import 'world_map_screen.dart';

/// Level result screen showing stars and score.
class ResultScreen extends StatelessWidget {
  const ResultScreen({
    super.key,
    required this.levelNumber,
    required this.stars,
    required this.isNewBest,
    required this.correctCount,
    required this.totalProblems,
    required this.score,
    required this.bestStreak,
  });

  final int levelNumber;
  final int stars;
  final bool isNewBest;
  final int correctCount;
  final int totalProblems;
  final int score;
  final int bestStreak;

  void _continue(BuildContext context) {
    final level = getLevel(levelNumber);
    final gameState = context.read<GameState>();

    if (level != null && level.levelInWorld == 10 && stars >= 2) {
      // Beat the boss! Show victory screen
      Navigator.of(context).pushReplacement(
        MaterialPageRoute(
          builder: (_) => BossVictoryScreen(worldNumber: level.worldNumber),
        ),
      );
    } else {
      // Back to world map
      if (stars >= 2) {
        // Advance to next world if needed
        final nextLevel = levelNumber + 1;
        final nextLevelData = getLevel(nextLevel);
        if (nextLevelData != null &&
            nextLevelData.worldNumber > gameState.currentWorld) {
          gameState.setWorld(nextLevelData.worldNumber);
        }
      }
      Navigator.of(context).pushReplacement(
        MaterialPageRoute(builder: (_) => const WorldMapScreen()),
      );
    }
  }

  void _replay(BuildContext context) {
    Navigator.of(context).pushReplacement(
      MaterialPageRoute(
        builder: (_) => GameplayScreen(levelNumber: levelNumber),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final l10n = AppLocalizations.of(context)!;
    final passed = stars >= 2;

    return BaseScreen(
      child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              // Title
              Text(
                passed ? l10n.resultComplete : l10n.resultFailed,
                style: Theme.of(context).textTheme.headlineMedium?.copyWith(
                      color: passed
                          ? AppColors.correctGreen
                          : AppColors.starYellow,
                    ),
              ),
              const SizedBox(height: 20),

              // Stars
              Text(
                '${'⭐' * stars}${'·' * (3 - stars)}',
                style: const TextStyle(fontSize: 36),
              ),
              const SizedBox(height: 10),

              // New best indicator
              if (isNewBest)
                Text(
                  '🎉 ${l10n.resultNewBest} 🎉',
                  style: const TextStyle(
                    fontSize: 18,
                    color: AppColors.correctGreen,
                  ),
                ),
              const SizedBox(height: 20),

              // Stats
              Text(
                l10n.resultCorrectCount(correctCount, totalProblems),
                style: const TextStyle(fontSize: 16),
              ),
              const SizedBox(height: 5),
              Text(
                l10n.resultScore(score),
                style: const TextStyle(fontSize: 16),
              ),
              if (bestStreak > 0) ...[
                const SizedBox(height: 5),
                Text(
                  l10n.resultBestStreak(bestStreak),
                  style: const TextStyle(fontSize: 16),
                ),
              ],
              const SizedBox(height: 40),

              // Buttons
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  AnimatedElevatedButton(
                    onPressed: () => _continue(context),
                    child: Text(l10n.navContinue),
                  ),
                  const SizedBox(width: 10),
                  AnimatedElevatedButton(
                    onPressed: () => _replay(context),
                    child: Text(l10n.navReplay),
                  ),
                ],
              ),
            ],
          ),
    );
  }
}
