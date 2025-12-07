import 'package:flutter/material.dart';

import '../core/world_l10n.dart';
import '../core/worlds.dart';
import '../l10n/app_localizations.dart';
import '../theme/app_theme.dart';
import '../widgets/story_screen.dart';
import 'gameplay_screen.dart';

/// Friend meet story screen (before level 6).
class FriendMeetScreen extends StatelessWidget {
  const FriendMeetScreen({
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
    final friendName = getFriendNameL10n(l10n, worldNumber);
    final friendIntro = getFriendIntroL10n(l10n, worldNumber);

    return StoryScreenLayout(
      title: 'Meet $friendName! ${world.friendEmoji}',
      titleColor: AppColors.starYellow,
      storyText: friendIntro,
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
