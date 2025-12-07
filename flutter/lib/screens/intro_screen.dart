import 'package:flutter/material.dart';

import '../l10n/app_localizations.dart';
import '../widgets/story_screen.dart';
import 'world_intro_screen.dart';

/// Game intro story screen.
class IntroScreen extends StatelessWidget {
  const IntroScreen({super.key});

  static const _flashyAscii = r'''
 /\_/\
 ( o.o )
 > ^ <
 /|   |\
''';

  @override
  Widget build(BuildContext context) {
    final l10n = AppLocalizations.of(context)!;

    return StoryScreenLayout(
      title: l10n.introFlashy,
      storyText: l10n.introStory,
      asciiArt: _flashyAscii,
      onContinue: () {
        Navigator.of(context).pushReplacement(
          MaterialPageRoute(
            builder: (_) => const WorldIntroScreen(worldNumber: 1),
          ),
        );
      },
    );
  }
}
