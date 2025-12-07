import 'package:flutter/material.dart';

import '../core/world_l10n.dart';
import '../core/worlds.dart';
import '../l10n/app_localizations.dart';
import '../widgets/story_screen.dart';
import 'world_map_screen.dart';

/// World intro story screen.
class WorldIntroScreen extends StatelessWidget {
  const WorldIntroScreen({super.key, required this.worldNumber});

  final int worldNumber;

  @override
  Widget build(BuildContext context) {
    final world = getWorld(worldNumber);
    if (world == null) {
      return const Scaffold(
        body: Center(child: Text('World not found')),
      );
    }

    final l10n = AppLocalizations.of(context)!;
    final worldName = getWorldNameL10n(l10n, worldNumber);
    final worldIntro = getWorldIntroL10n(l10n, worldNumber);

    return StoryScreenLayout(
      title: '${world.themeEmoji} $worldName ${world.themeEmoji}',
      storyText: worldIntro,
      onContinue: () {
        Navigator.of(context).pushReplacement(
          MaterialPageRoute(
            builder: (_) => const WorldMapScreen(),
          ),
        );
      },
    );
  }
}
