import 'dart:math' show sqrt;

import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../core/levels.dart';
import '../core/world_l10n.dart';
import '../core/worlds.dart';
import '../l10n/app_localizations.dart';
import '../state/game_state.dart';
import '../theme/app_theme.dart';
import '../widgets/level_node.dart';
import '../widgets/responsive_container.dart';
import 'boss_intro_screen.dart';
import 'friend_meet_screen.dart';
import 'gameplay_screen.dart';
import 'leaderboard_screen.dart';
import 'player_select_screen.dart';

/// World map screen showing level progression.
class WorldMapScreen extends StatelessWidget {
  const WorldMapScreen({super.key});

  void _selectLevel(BuildContext context, int levelNumber) {
    final level = getLevel(levelNumber);
    if (level == null) return;

    final worldNumber = level.worldNumber;
    final levelInWorld = level.levelInWorld;

    // Check for story screens before certain levels
    if (levelInWorld == 6) {
      // Friend meet before level 6
      Navigator.of(context).push(
        MaterialPageRoute(
          builder: (_) => FriendMeetScreen(
            worldNumber: worldNumber,
            levelNumber: levelNumber,
          ),
        ),
      );
    } else if (levelInWorld == 10) {
      // Boss intro before level 10
      Navigator.of(context).push(
        MaterialPageRoute(
          builder: (_) => BossIntroScreen(
            worldNumber: worldNumber,
            levelNumber: levelNumber,
          ),
        ),
      );
    } else {
      // Regular level - go straight to gameplay
      Navigator.of(context).push(
        MaterialPageRoute(
          builder: (_) => GameplayScreen(levelNumber: levelNumber),
        ),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    final gameState = context.watch<GameState>();
    final currentWorld = gameState.currentWorld;
    final world = getWorld(currentWorld);
    final progress = gameState.progress;
    final levels = getLevelsForWorld(currentWorld);

    if (world == null) {
      return const Scaffold(
        body: Center(child: Text('World not found')),
      );
    }

    return Scaffold(
      body: SafeArea(
        child: Center(
          child: ConstrainedBox(
            constraints: const BoxConstraints(maxWidth: BaseScreenConfig.maxWidth),
            child: Container(
              margin: BaseScreenConfig.margin,
              decoration: BoxDecoration(
                border: Border.all(
                  color: BaseScreenConfig.borderColor,
                  width: BaseScreenConfig.borderWidth,
                ),
                borderRadius: BorderRadius.circular(BaseScreenConfig.borderRadius),
              ),
              child: Padding(
                padding: BaseScreenConfig.padding,
                child: LayoutBuilder(
            builder: (context, constraints) {
              // Calculate the width to match the square map
              // The map takes all available height minus header (~60) and footer (~70)
              final availableHeight = constraints.maxHeight - 130;
              final mapWidth = availableHeight < constraints.maxWidth
                  ? availableHeight
                  : constraints.maxWidth;

              return Column(
                children: [
                  // Header with world title and navigation - constrained to map width
                  Center(
                    child: SizedBox(
                      width: mapWidth,
                      child: _WorldHeader(
                        world: world,
                        playerName: gameState.currentPlayer ?? '',
                        onPreviousWorld: currentWorld > 1
                            ? () => gameState.previousWorld()
                            : null,
                        onNextWorld: currentWorld < 4 &&
                                gameState.canAccessWorld(currentWorld + 1)
                            ? () => gameState.nextWorld()
                            : null,
                        showNextArrow: currentWorld < 4,
                      ),
                    ),
                  ),
                  const SizedBox(height: 5),

                  // Map with level nodes
                  Expanded(
                    child: _WorldMap(
                      world: world,
                      levels: levels,
                      progress: progress,
                      onLevelTap: (levelNumber) =>
                          _selectLevel(context, levelNumber),
                    ),
                  ),

                  const SizedBox(height: 10),

                  // Footer buttons
                  Builder(
                    builder: (context) {
                      final l10n = AppLocalizations.of(context)!;
                      return Row(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          ElevatedButton(
                            onPressed: () {
                              Navigator.of(context).push(
                                MaterialPageRoute(
                                  builder: (_) => const LeaderboardScreen(),
                                ),
                              );
                            },
                            style: ElevatedButton.styleFrom(
                              backgroundColor: AppColors.starYellow,
                            ),
                            child: Text(l10n.leaderboardTitle),
                          ),
                          const SizedBox(width: 10),
                          ElevatedButton(
                            onPressed: () {
                              gameState.logout();
                              Navigator.of(context).pushAndRemoveUntil(
                                MaterialPageRoute(
                                  builder: (_) => const PlayerSelectScreen(),
                                ),
                                (route) => false,
                              );
                            },
                            style: ElevatedButton.styleFrom(
                              backgroundColor: AppColors.dangerRed,
                            ),
                            child: Text(l10n.navBack),
                          ),
                        ],
                      );
                    },
                  ),
            ],
          );
        },
      ),
            ),
          ),
        ),
      ),
      ),
    );
  }
}

/// World header with title and navigation arrows.
class _WorldHeader extends StatelessWidget {
  const _WorldHeader({
    required this.world,
    required this.playerName,
    required this.onPreviousWorld,
    required this.onNextWorld,
    required this.showNextArrow,
  });

  final World world;
  final String playerName;
  final VoidCallback? onPreviousWorld;
  final VoidCallback? onNextWorld;
  final bool showNextArrow;

  @override
  Widget build(BuildContext context) {
    final l10n = AppLocalizations.of(context)!;
    final worldName = getWorldNameL10n(l10n, world.number);

    return Row(
      children: [
        // Previous world button
        SizedBox(
          width: 40,
          child: onPreviousWorld != null
              ? IconButton(
                  onPressed: onPreviousWorld,
                  icon: const Icon(Icons.chevron_left, size: 30),
                  color: Colors.white,
                )
              : null,
        ),

        // Title
        Expanded(
          child: Container(
            padding: const EdgeInsets.symmetric(horizontal: 15, vertical: 8),
            decoration: BoxDecoration(
              color: Colors.black.withValues(alpha: 0.5),
              borderRadius: BorderRadius.circular(20),
            ),
            child: Column(
              children: [
                Text(
                  '${world.themeEmoji} $worldName ${world.themeEmoji}',
                  style: const TextStyle(
                    fontSize: 18,
                    fontWeight: FontWeight.bold,
                    color: Colors.white,
                  ),
                  textAlign: TextAlign.center,
                ),
                Text(
                  playerName,
                  style: TextStyle(
                    fontSize: 14,
                    color: AppColors.textSecondary,
                  ),
                ),
              ],
            ),
          ),
        ),

        // Next world button
        SizedBox(
          width: 40,
          child: showNextArrow
              ? IconButton(
                  onPressed: onNextWorld,
                  icon: const Icon(Icons.chevron_right, size: 30),
                  color: onNextWorld != null
                      ? Colors.white
                      : Colors.white.withValues(alpha: 0.3),
                )
              : null,
        ),
      ],
    );
  }
}

/// World map with background and level nodes.
class _WorldMap extends StatelessWidget {
  const _WorldMap({
    required this.world,
    required this.levels,
    required this.progress,
    required this.onLevelTap,
  });

  final World world;
  final List<Level> levels;
  final dynamic progress;
  final void Function(int levelNumber) onLevelTap;

  @override
  Widget build(BuildContext context) {
    return AspectRatio(
      aspectRatio: 1,
      child: Container(
        decoration: BoxDecoration(
          border: Border.all(color: const Color(0xFF5a3d2b), width: 6),
          borderRadius: BorderRadius.circular(8),
          boxShadow: [
            BoxShadow(
              color: Colors.black.withValues(alpha: 0.4),
              blurRadius: 12,
              offset: const Offset(0, 4),
            ),
          ],
        ),
        child: ClipRRect(
          borderRadius: BorderRadius.circular(2),
          child: LayoutBuilder(
            builder: (context, constraints) {
              final mapSize = constraints.biggest.shortestSide;
              return Stack(
                children: [
                  // Background image
                  Positioned.fill(
                    child: Image.asset(
                      'assets/${world.background}',
                      fit: BoxFit.cover,
                      errorBuilder: (context, error, stackTrace) {
                        // Fallback color if image not found
                        return Container(
                          color: _parseColor(world.nodeColor),
                        );
                      },
                    ),
                  ),

                  // Path connecting levels
                  Positioned.fill(
                    child: CustomPaint(
                      painter: _PathPainter(
                        waypoints: world.mapWaypoints,
                        mapSize: mapSize,
                        pathColor: _parseColor(world.pathColor),
                      ),
                    ),
                  ),

                  // Level nodes
                  ..._buildLevelNodes(mapSize),
                ],
              );
            },
          ),
        ),
      ),
    );
  }

  List<Widget> _buildLevelNodes(double mapSize) {
    // Get positions distributed evenly along the path
    final positions = _getLevelPositions(world.mapWaypoints, mapSize, levels.length);
    if (positions.length < levels.length) {
      return [];
    }

    const nodeSize = 44.0;

    return levels.map((level) {
      final index = level.levelInWorld - 1;
      if (index >= positions.length) return const SizedBox.shrink();

      final pos = positions[index];
      final stars = progress?.getStars(level.number) ?? 0;
      final unlocked = progress?.isUnlocked(level.number) ?? (level.number == 1);

      return Positioned(
        left: pos.dx - nodeSize / 2,
        top: pos.dy - nodeSize / 2,
        child: SizedBox(
          width: nodeSize,
          height: nodeSize,
          child: LevelNode(
            levelInWorld: level.levelInWorld,
            stars: stars,
            isUnlocked: unlocked,
            friendEmoji:
                level.levelInWorld == 6 ? world.friendEmoji : null,
            bossEmoji: level.levelInWorld == 10 ? world.bossEmoji : null,
            nodeColor: _parseColor(world.nodeColor),
            glowColor: _parseColor(world.nodeGlow),
            onTap: unlocked ? () => onLevelTap(level.number) : null,
          ),
        ),
      );
    }).toList();
  }

  /// Parse waypoints and distribute levels evenly along the Catmull-Rom curve.
  List<Offset> _getLevelPositions(String waypoints, double mapSize, int levelCount) {
    // Parse waypoints into pixel coordinates
    final points = waypoints.trim().split(RegExp(r'\s+'));
    final pathPoints = points.map((p) {
      final parts = p.split(',');
      if (parts.length != 2) return Offset.zero;
      final x = double.tryParse(parts[0]) ?? 0;
      final y = double.tryParse(parts[1]) ?? 0;
      return Offset(x / 100 * mapSize, y / 100 * mapSize);
    }).toList();

    if (pathPoints.isEmpty) return [];
    if (pathPoints.length == 1) return pathPoints;

    // Sample the Catmull-Rom curve at many points to get accurate arc length
    const samplesPerSegment = 20;
    final sampledPoints = <Offset>[];

    for (var i = 0; i < pathPoints.length - 1; i++) {
      final p0 = pathPoints[i > 0 ? i - 1 : 0];
      final p1 = pathPoints[i];
      final p2 = pathPoints[i + 1];
      final p3 = pathPoints[i + 2 < pathPoints.length ? i + 2 : pathPoints.length - 1];

      for (var s = 0; s < samplesPerSegment; s++) {
        final t = s / samplesPerSegment;
        sampledPoints.add(_sampleCatmullRom(p0, p1, p2, p3, t));
      }
    }
    // Add the final point
    sampledPoints.add(pathPoints.last);

    // Calculate cumulative distances along sampled curve
    final distances = <double>[0.0];
    for (var i = 1; i < sampledPoints.length; i++) {
      final dx = sampledPoints[i].dx - sampledPoints[i - 1].dx;
      final dy = sampledPoints[i].dy - sampledPoints[i - 1].dy;
      distances.add(distances.last + sqrt(dx * dx + dy * dy));
    }
    final totalLength = distances.last;

    if (totalLength == 0) return pathPoints;

    // Place levels at equal intervals along the curve
    final levelPositions = <Offset>[];
    for (var level = 0; level < levelCount; level++) {
      final targetDist = (level / (levelCount - 1)) * totalLength;

      // Find which sampled segment this falls on
      var segmentIndex = 0;
      for (var i = 1; i < distances.length; i++) {
        if (distances[i] >= targetDist) {
          segmentIndex = i - 1;
          break;
        }
        segmentIndex = i - 1;
      }

      // Interpolate within the sampled segment
      final segmentStart = distances[segmentIndex];
      final segmentEnd = distances[segmentIndex + 1];
      final segmentLength = segmentEnd - segmentStart;
      final t = segmentLength > 0 ? (targetDist - segmentStart) / segmentLength : 0.0;

      final p1 = sampledPoints[segmentIndex];
      final p2 = sampledPoints[segmentIndex + 1];
      levelPositions.add(Offset(
        p1.dx + (p2.dx - p1.dx) * t,
        p1.dy + (p2.dy - p1.dy) * t,
      ));
    }

    return levelPositions;
  }

  /// Sample a point on the Catmull-Rom curve at parameter t (0-1).
  Offset _sampleCatmullRom(Offset p0, Offset p1, Offset p2, Offset p3, double t) {
    const tension = 0.5;
    // Convert to cubic Bezier control points
    final cp1 = Offset(
      p1.dx + (p2.dx - p0.dx) * tension / 3,
      p1.dy + (p2.dy - p0.dy) * tension / 3,
    );
    final cp2 = Offset(
      p2.dx - (p3.dx - p1.dx) * tension / 3,
      p2.dy - (p3.dy - p1.dy) * tension / 3,
    );

    // Evaluate cubic Bezier at t
    final mt = 1 - t;
    final mt2 = mt * mt;
    final mt3 = mt2 * mt;
    final t2 = t * t;
    final t3 = t2 * t;

    return Offset(
      mt3 * p1.dx + 3 * mt2 * t * cp1.dx + 3 * mt * t2 * cp2.dx + t3 * p2.dx,
      mt3 * p1.dy + 3 * mt2 * t * cp1.dy + 3 * mt * t2 * cp2.dy + t3 * p2.dy,
    );
  }

  Color _parseColor(String hex) {
    final hexCode = hex.replaceAll('#', '');
    return Color(int.parse('FF$hexCode', radix: 16));
  }
}

/// Custom painter for the path connecting levels.
class _PathPainter extends CustomPainter {
  _PathPainter({
    required this.waypoints,
    required this.mapSize,
    required this.pathColor,
  });

  final String waypoints;
  final double mapSize;
  final Color pathColor;

  @override
  void paint(Canvas canvas, Size size) {
    final points = _parseWaypoints();
    if (points.length < 2) return;

    // Create smooth path using Catmull-Rom splines converted to cubic Bezier
    final path = Path();
    path.moveTo(points.first.dx, points.first.dy);

    for (var i = 0; i < points.length - 1; i++) {
      // Get the 4 points needed for Catmull-Rom
      final p0 = points[i > 0 ? i - 1 : 0];
      final p1 = points[i];
      final p2 = points[i + 1];
      final p3 = points[i + 2 < points.length ? i + 2 : points.length - 1];

      // Convert Catmull-Rom to cubic Bezier control points
      final (cp1, cp2) = _catmullRomToBezier(p0, p1, p2, p3);
      path.cubicTo(cp1.dx, cp1.dy, cp2.dx, cp2.dy, p2.dx, p2.dy);
    }

    // Draw shadow/outline first
    final shadowPaint = Paint()
      ..color = Colors.black.withValues(alpha: 0.4)
      ..strokeWidth = 12
      ..style = PaintingStyle.stroke
      ..strokeCap = StrokeCap.round
      ..strokeJoin = StrokeJoin.round;
    canvas.drawPath(path, shadowPaint);

    // Draw main path
    final pathPaint = Paint()
      ..color = pathColor
      ..strokeWidth = 8
      ..style = PaintingStyle.stroke
      ..strokeCap = StrokeCap.round
      ..strokeJoin = StrokeJoin.round;
    canvas.drawPath(path, pathPaint);
  }

  /// Convert Catmull-Rom spline segment to cubic Bezier control points.
  /// Uses tension factor of 0.5 (centripetal).
  (Offset, Offset) _catmullRomToBezier(Offset p0, Offset p1, Offset p2, Offset p3) {
    const t = 0.5; // Tension factor
    final cp1 = Offset(
      p1.dx + (p2.dx - p0.dx) * t / 3,
      p1.dy + (p2.dy - p0.dy) * t / 3,
    );
    final cp2 = Offset(
      p2.dx - (p3.dx - p1.dx) * t / 3,
      p2.dy - (p3.dy - p1.dy) * t / 3,
    );
    return (cp1, cp2);
  }

  List<Offset> _parseWaypoints() {
    final pointStrs = waypoints.trim().split(RegExp(r'\s+'));
    return pointStrs.map((p) {
      final parts = p.split(',');
      if (parts.length != 2) return Offset.zero;
      final x = double.tryParse(parts[0]) ?? 0;
      final y = double.tryParse(parts[1]) ?? 0;
      return Offset(x / 100 * mapSize, y / 100 * mapSize);
    }).toList();
  }

  @override
  bool shouldRepaint(covariant _PathPainter oldDelegate) {
    return oldDelegate.waypoints != waypoints ||
        oldDelegate.mapSize != mapSize ||
        oldDelegate.pathColor != pathColor;
  }
}
