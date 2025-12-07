import 'package:flutter/material.dart';

import '../core/world_l10n.dart';
import '../core/worlds.dart';
import '../l10n/app_localizations.dart';
import '../theme/app_theme.dart';
import '../widgets/story_screen.dart';
import 'gameplay_screen.dart';

/// Boss intro story screen (before level 10).
class BossIntroScreen extends StatelessWidget {
  const BossIntroScreen({
    super.key,
    required this.worldNumber,
    required this.levelNumber,
  });

  final int worldNumber;
  final int levelNumber;

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
    final bossIntro = getBossIntroL10n(l10n, worldNumber);

    return StoryScreenLayout(
      title: '$bossName Appears! ${world.bossEmoji}',
      titleColor: AppColors.incorrectRed,
      storyText: bossIntro,
      onContinue: () {
        Navigator.of(context).pushReplacement(
          MaterialPageRoute(
            builder: (_) => GameplayScreen(levelNumber: levelNumber),
          ),
        );
      },
    );
  }
}
