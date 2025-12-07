import 'package:flutter/material.dart';

import '../theme/app_theme.dart';

/// Level node on the world map.
class LevelNode extends StatelessWidget {
  const LevelNode({
    super.key,
    required this.levelInWorld,
    required this.stars,
    required this.isUnlocked,
    this.friendEmoji,
    this.bossEmoji,
    required this.nodeColor,
    required this.glowColor,
    this.onTap,
  });

  final int levelInWorld;
  final int stars;
  final bool isUnlocked;
  final String? friendEmoji;
  final String? bossEmoji;
  final Color nodeColor;
  final Color glowColor;
  final VoidCallback? onTap;

  @override
  Widget build(BuildContext context) {
    final isCompleted = stars > 0;
    final isPerfect = stars == 3;

    Color bgColor;
    Color borderColor;
    Color textColor;

    if (!isUnlocked) {
      // Locked
      bgColor = Colors.grey.shade800.withValues(alpha: 0.8);
      borderColor = Colors.grey.shade600.withValues(alpha: 0.8);
      textColor = Colors.grey.shade500;
    } else if (isPerfect) {
      // Perfect (3 stars)
      bgColor = const Color(0xFF6a5a2a);
      borderColor = AppColors.starYellow;
      textColor = Colors.white;
    } else if (isCompleted) {
      // Completed (1-2 stars)
      bgColor = const Color(0xFF3a6a3a);
      borderColor = AppColors.correctGreen;
      textColor = Colors.white;
    } else {
      // Available (unlocked but not completed)
      bgColor = nodeColor;
      borderColor = glowColor;
      textColor = Colors.white;
    }

    return GestureDetector(
      onTap: onTap,
      child: Stack(
        clipBehavior: Clip.none,
        children: [
          // Node circle
          Container(
            width: 44,
            height: 44,
            decoration: BoxDecoration(
              shape: BoxShape.circle,
              color: bgColor,
              border: Border.all(color: borderColor, width: 3),
              boxShadow: isUnlocked
                  ? [
                      BoxShadow(
                        color: borderColor.withValues(alpha: 0.5),
                        blurRadius: 10,
                        spreadRadius: 2,
                      ),
                    ]
                  : null,
            ),
            child: Center(
              child: Text(
                isUnlocked ? '$levelInWorld' : '🔒',
                style: TextStyle(
                  fontSize: 16,
                  fontWeight: FontWeight.bold,
                  color: textColor,
                ),
              ),
            ),
          ),

          // Stars display below node
          if (isUnlocked && stars > 0)
            Positioned(
              bottom: -18,
              left: 0,
              right: 0,
              child: Text(
                '⭐' * stars,
                textAlign: TextAlign.center,
                style: const TextStyle(fontSize: 10),
              ),
            ),

          // Character emoji for friend/boss levels
          if (friendEmoji != null || bossEmoji != null)
            Positioned(
              top: -5,
              right: -30,
              child: Text(
                friendEmoji ?? bossEmoji ?? '',
                style: const TextStyle(fontSize: 24),
              ),
            ),
        ],
      ),
    );
  }
}
