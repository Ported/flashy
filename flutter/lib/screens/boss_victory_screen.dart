import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../core/world_l10n.dart';
import '../core/worlds.dart';
import '../l10n/app_localizations.dart';
import '../state/game_state.dart';
import '../theme/app_theme.dart';
import '../widgets/story_screen.dart';
import 'game_complete_screen.dart';
import 'world_intro_screen.dart';

/// Boss victory screen shown after defeating a world boss.
class BossVictoryScreen extends StatelessWidget {
  const BossVictoryScreen({super.key, required this.worldNumber});

  final int worldNumber;

  static const _flashyAscii = r'''
    /\_/\
   ( ^.^ )
    > ^ <
   /|   |\
''';

  @override
  Widget build(BuildContext context) {
    final world = getWorld(worldNumber);
    if (world == null) {
      return const Scaffold(
        body: Center(child: Text('World not found')),
      );
    }

    final l10n = AppLocalizations.of(context)!;
    final bossName = getBossNameL10n(l10n, worldNumber);
    final bossDefeat = getBossDefeatL10n(l10n, worldNumber);
    final storyText = 'You defeated $bossName!\n\n$bossDefeat';

    return StoryScreenLayout(
      title: l10n.victoryTitle,
      titleColor: AppColors.correctGreen,
      storyText: storyText,
      asciiArt: _flashyAscii,
      onContinue: () {
        final gameState = context.read<GameState>();
        final nextWorld = getWorld(worldNumber + 1);

        if (nextWorld != null) {
          // More worlds to explore
          gameState.setWorld(worldNumber + 1);
          Navigator.of(context).pushReplacement(
            MaterialPageRoute(
              builder: (_) => WorldIntroScreen(worldNumber: worldNumber + 1),
            ),
          );
        } else {
          // All worlds complete!
          Navigator.of(context).pushReplacement(
            MaterialPageRoute(builder: (_) => const GameCompleteScreen()),
          );
        }
      },
    );
  }
}
