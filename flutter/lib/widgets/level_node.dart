import 'package:flutter/material.dart';

import '../l10n/app_localizations.dart';
import '../theme/app_theme.dart';

/// Get localized level name by level number.
String getLevelNameL10n(AppLocalizations l10n, int levelNumber) {
  switch (levelNumber) {
    case 1: return l10n.level1Name;
    case 2: return l10n.level2Name;
    case 3: return l10n.level3Name;
    case 4: return l10n.level4Name;
    case 5: return l10n.level5Name;
    case 6: return l10n.level6Name;
    case 7: return l10n.level7Name;
    case 8: return l10n.level8Name;
    case 9: return l10n.level9Name;
    case 10: return l10n.level10Name;
    case 11: return l10n.level11Name;
    case 12: return l10n.level12Name;
    case 13: return l10n.level13Name;
    case 14: return l10n.level14Name;
    case 15: return l10n.level15Name;
    case 16: return l10n.level16Name;
    case 17: return l10n.level17Name;
    case 18: return l10n.level18Name;
    case 19: return l10n.level19Name;
    case 20: return l10n.level20Name;
    case 21: return l10n.level21Name;
    case 22: return l10n.level22Name;
    case 23: return l10n.level23Name;
    case 24: return l10n.level24Name;
    case 25: return l10n.level25Name;
    case 26: return l10n.level26Name;
    case 27: return l10n.level27Name;
    case 28: return l10n.level28Name;
    case 29: return l10n.level29Name;
    case 30: return l10n.level30Name;
    case 31: return l10n.level31Name;
    case 32: return l10n.level32Name;
    case 33: return l10n.level33Name;
    case 34: return l10n.level34Name;
    case 35: return l10n.level35Name;
    case 36: return l10n.level36Name;
    case 37: return l10n.level37Name;
    case 38: return l10n.level38Name;
    case 39: return l10n.level39Name;
    case 40: return l10n.level40Name;
    default: return 'Level $levelNumber';
  }
}

/// Level node on the world map with hover effects.
class LevelNode extends StatefulWidget {
  const LevelNode({
    super.key,
    required this.levelNumber,
    required this.levelInWorld,
    required this.stars,
    required this.isUnlocked,
    this.friendEmoji,
    this.bossEmoji,
    required this.nodeColor,
    required this.glowColor,
    this.onTap,
  });

  final int levelNumber;
  final int levelInWorld;
  final int stars;
  final bool isUnlocked;
  final String? friendEmoji;
  final String? bossEmoji;
  final Color nodeColor;
  final Color glowColor;
  final VoidCallback? onTap;

  @override
  State<LevelNode> createState() => _LevelNodeState();
}

class _LevelNodeState extends State<LevelNode> with SingleTickerProviderStateMixin {
  bool _isHovered = false;
  late AnimationController _animController;
  late Animation<double> _scaleAnim;

  @override
  void initState() {
    super.initState();
    _animController = AnimationController(
      duration: const Duration(milliseconds: 150),
      vsync: this,
    );
    _scaleAnim = Tween<double>(begin: 1.0, end: 1.25).animate(
      CurvedAnimation(parent: _animController, curve: Curves.easeOut),
    );
  }

  @override
  void dispose() {
    _animController.dispose();
    super.dispose();
  }

  void _onEnter() {
    if (!widget.isUnlocked) return;
    setState(() => _isHovered = true);
    _animController.forward();
  }

  void _onExit() {
    setState(() => _isHovered = false);
    _animController.reverse();
  }

  @override
  Widget build(BuildContext context) {
    final isCompleted = widget.stars > 0;
    final isPerfect = widget.stars == 3;

    Color bgColor;
    Color borderColor;
    Color textColor;

    if (!widget.isUnlocked) {
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
      bgColor = widget.nodeColor;
      borderColor = widget.glowColor;
      textColor = Colors.white;
    }

    return MouseRegion(
      onEnter: (_) => _onEnter(),
      onExit: (_) => _onExit(),
      cursor: widget.isUnlocked ? SystemMouseCursors.click : SystemMouseCursors.basic,
      child: GestureDetector(
        onTap: widget.onTap,
        child: AnimatedBuilder(
          animation: _scaleAnim,
          builder: (context, child) {
            return Stack(
              clipBehavior: Clip.none,
              children: [
                // Node circle with scale animation
                Transform.scale(
                  scale: _scaleAnim.value,
                  child: Container(
                    width: 44,
                    height: 44,
                    decoration: BoxDecoration(
                      shape: BoxShape.circle,
                      color: bgColor,
                      border: Border.all(color: borderColor, width: 3),
                      boxShadow: widget.isUnlocked
                          ? [
                              BoxShadow(
                                color: borderColor.withValues(alpha: _isHovered ? 0.8 : 0.5),
                                blurRadius: _isHovered ? 20 : 10,
                                spreadRadius: _isHovered ? 5 : 2,
                              ),
                            ]
                          : null,
                    ),
                    child: Center(
                      child: Text(
                        widget.isUnlocked ? '${widget.levelInWorld}' : '🔒',
                        style: TextStyle(
                          fontSize: 16,
                          fontWeight: FontWeight.bold,
                          color: textColor,
                        ),
                      ),
                    ),
                  ),
                ),

                // Stars display below node
                if (widget.isUnlocked && widget.stars > 0)
                  Positioned(
                    bottom: -18,
                    left: 0,
                    right: 0,
                    child: Text(
                      '⭐' * widget.stars,
                      textAlign: TextAlign.center,
                      style: const TextStyle(fontSize: 10),
                    ),
                  ),

                // Character emoji for friend/boss levels
                if (widget.friendEmoji != null || widget.bossEmoji != null)
                  Positioned(
                    top: -5,
                    right: -30,
                    child: Text(
                      widget.friendEmoji ?? widget.bossEmoji ?? '',
                      style: const TextStyle(fontSize: 24),
                    ),
                  ),

                // Tooltip with level name on hover
                if (_isHovered && widget.isUnlocked)
                  Positioned(
                    bottom: 55,
                    left: -50,
                    right: -50,
                    child: Center(
                      child: Container(
                        padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 5),
                        decoration: BoxDecoration(
                          color: Colors.black.withValues(alpha: 0.85),
                          borderRadius: BorderRadius.circular(6),
                        ),
                        child: Text(
                          getLevelNameL10n(AppLocalizations.of(context)!, widget.levelNumber),
                          style: const TextStyle(
                            color: Colors.white,
                            fontSize: 12,
                            fontWeight: FontWeight.w500,
                          ),
                          textAlign: TextAlign.center,
                        ),
                      ),
                    ),
                  ),
              ],
            );
          },
        ),
      ),
    );
  }
}
