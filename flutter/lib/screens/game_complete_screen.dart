import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../l10n/app_localizations.dart';
import '../state/game_state.dart';
import '../widgets/story_screen.dart';
import 'player_select_screen.dart';

/// Game complete screen shown after finishing all worlds.
class GameCompleteScreen extends StatelessWidget {
  const GameCompleteScreen({super.key});

  static const _familyAscii = r'''
      /\_/\           /\_/\           /\_/\
     ( ^.^ )         ( o.o )         ( o.o )
      > ^ <           > ^ <           > ^ <
     /|   |\   ~     /|   |\   ~     /|   |\
     FLASHY           MOM             DAD
''';

  @override
  Widget build(BuildContext context) {
    final l10n = AppLocalizations.of(context)!;

    return StoryScreenLayout(
      title: l10n.gameCompleteTitle,
      titleColor: const Color(0xFFFF00FF), // Magenta
      storyText: l10n.gameCompleteStory,
      asciiArt: _familyAscii,
      hint: l10n.gameCompleteHint,
      onContinue: () {
        final gameState = context.read<GameState>();
        gameState.logout();
        Navigator.of(context).pushAndRemoveUntil(
          MaterialPageRoute(builder: (_) => const PlayerSelectScreen()),
          (route) => false,
        );
      },
    );
  }
}
