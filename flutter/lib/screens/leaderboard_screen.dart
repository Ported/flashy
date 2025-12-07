import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../api/flashy_api.dart';
import '../l10n/app_localizations.dart';
import '../state/game_state.dart';
import '../theme/app_theme.dart';
import '../widgets/animated_button.dart';
import '../widgets/responsive_container.dart';

/// Leaderboard screen showing top players.
class LeaderboardScreen extends StatefulWidget {
  const LeaderboardScreen({super.key});

  @override
  State<LeaderboardScreen> createState() => _LeaderboardScreenState();
}

class _LeaderboardScreenState extends State<LeaderboardScreen> {
  List<LeaderboardEntry>? _entries;
  bool _loading = true;
  bool _hasError = false;

  @override
  void initState() {
    super.initState();
    _loadLeaderboard();
  }

  Future<void> _loadLeaderboard() async {
    final gameState = context.read<GameState>();
    try {
      final entries = await gameState.api.getLeaderboard();
      setState(() {
        _entries = entries;
        _loading = false;
      });
    } catch (e) {
      setState(() {
        _hasError = true;
        _loading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    final l10n = AppLocalizations.of(context)!;
    final gameState = context.watch<GameState>();
    final currentPlayer = gameState.currentPlayer;

    return BaseScreen(
      child: Column(
            children: [
              Text(
                l10n.leaderboardTitle,
                style: Theme.of(context).textTheme.headlineMedium?.copyWith(
                      color: AppColors.starYellow,
                    ),
              ),
              const SizedBox(height: 20),
              Expanded(
                child: _loading
                    ? const Center(child: CircularProgressIndicator())
                    : _hasError
                        ? Center(
                            child: Text(
                              l10n.leaderboardError,
                              style: const TextStyle(
                                color: AppColors.dangerRed,
                              ),
                            ),
                          )
                        : _entries == null || _entries!.isEmpty
                            ? Center(
                                child: Text(
                                  l10n.leaderboardEmpty,
                                  style: TextStyle(
                                    color: AppColors.textSecondary,
                                  ),
                                ),
                              )
                            : ListView.builder(
                                itemCount: _entries!.length,
                                itemBuilder: (context, index) {
                                  final entry = _entries![index];
                                  final isTop3 = entry.rank <= 3;
                                  final isCurrentPlayer =
                                      entry.playerName == currentPlayer;

                                  return _LeaderboardEntryTile(
                                    entry: entry,
                                    isTop3: isTop3,
                                    isCurrentPlayer: isCurrentPlayer,
                                  );
                                },
                              ),
              ),
              const SizedBox(height: 20),
              AnimatedElevatedButton(
                onPressed: () => Navigator.of(context).pop(),
                child: Text(l10n.navBack),
              ),
            ],
          ),
    );
  }
}

/// Leaderboard entry tile.
class _LeaderboardEntryTile extends StatelessWidget {
  const _LeaderboardEntryTile({
    required this.entry,
    required this.isTop3,
    required this.isCurrentPlayer,
  });

  final LeaderboardEntry entry;
  final bool isTop3;
  final bool isCurrentPlayer;

  @override
  Widget build(BuildContext context) {
    Color borderColor;
    Color backgroundColor;

    if (isCurrentPlayer) {
      borderColor = AppColors.correctGreen;
      backgroundColor = const Color(0xFF1a2e1a);
    } else if (isTop3) {
      borderColor = AppColors.starYellow;
      backgroundColor = const Color(0xFF2a2a1e);
    } else {
      borderColor = AppColors.accentCyan;
      backgroundColor = AppColors.darkBackground;
    }

    return Container(
      margin: const EdgeInsets.symmetric(vertical: 5),
      padding: const EdgeInsets.symmetric(horizontal: 15, vertical: 10),
      decoration: BoxDecoration(
        color: backgroundColor,
        borderRadius: BorderRadius.circular(5),
        border: Border(
          left: BorderSide(color: borderColor, width: 3),
        ),
      ),
      child: Row(
        children: [
          SizedBox(
            width: 30,
            child: Text(
              '#${entry.rank}',
              style: TextStyle(
                fontWeight: FontWeight.bold,
                color: isTop3 ? AppColors.starYellow : AppColors.accentCyan,
              ),
            ),
          ),
          const SizedBox(width: 15),
          Expanded(
            child: Text(
              entry.playerName,
              style: const TextStyle(fontSize: 16),
            ),
          ),
          Text(
            '${entry.totalScore} pts',
            style: TextStyle(
              color: AppColors.textSecondary,
            ),
          ),
        ],
      ),
    );
  }
}
