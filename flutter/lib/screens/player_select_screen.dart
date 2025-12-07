import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../l10n/app_localizations.dart';
import '../state/game_state.dart';
import '../theme/app_theme.dart';
import '../widgets/responsive_container.dart';
import 'intro_screen.dart';
import 'new_player_screen.dart';
import 'welcome_screen.dart';
import 'world_map_screen.dart';

/// Player selection screen - list existing players or create new.
class PlayerSelectScreen extends StatefulWidget {
  const PlayerSelectScreen({super.key});

  @override
  State<PlayerSelectScreen> createState() => _PlayerSelectScreenState();
}

class _PlayerSelectScreenState extends State<PlayerSelectScreen> {
  List<String> _players = [];
  Map<String, int> _playerLevels = {};
  bool _loading = true;

  @override
  void initState() {
    super.initState();
    _loadPlayers();
  }

  Future<void> _loadPlayers() async {
    final gameState = context.read<GameState>();
    final players = await gameState.listPlayers();

    final levels = <String, int>{};
    for (final name in players) {
      final progress = await gameState.storage?.loadProgress(name);
      levels[name] = progress?.getHighestUnlocked() ?? 1;
    }

    setState(() {
      _players = players;
      _playerLevels = levels;
      _loading = false;
    });
  }

  Future<void> _selectPlayer(String name) async {
    final gameState = context.read<GameState>();
    await gameState.selectPlayer(name);

    if (!mounted) return;

    // Check if player has made progress
    final progress = gameState.progress;
    if (progress != null && progress.getHighestUnlocked() > 1) {
      // Go to world map
      Navigator.of(context).pushReplacement(
        MaterialPageRoute(builder: (_) => const WorldMapScreen()),
      );
    } else {
      // Show intro for new-ish player
      Navigator.of(context).pushReplacement(
        MaterialPageRoute(builder: (_) => const IntroScreen()),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    final l10n = AppLocalizations.of(context)!;

    return BaseScreen(
      child: Column(
            children: [
              Text(
                l10n.playerWhoPlaying,
                style: Theme.of(context).textTheme.headlineMedium,
                textAlign: TextAlign.center,
              ),
              const SizedBox(height: 20),
              Expanded(
                child: _loading
                    ? const Center(child: CircularProgressIndicator())
                    : _players.isEmpty
                        ? Center(
                            child: Text(
                              l10n.playerNoPlayers,
                              style: TextStyle(
                                color: AppColors.textSecondary,
                                fontSize: 16,
                              ),
                            ),
                          )
                        : ListView.builder(
                            itemCount: _players.length,
                            itemBuilder: (context, index) {
                              final name = _players[index];
                              final level = _playerLevels[name] ?? 1;
                              return _PlayerTile(
                                name: name,
                                levelText: '${l10n.playerLevel} $level',
                                onTap: () => _selectPlayer(name),
                              );
                            },
                          ),
              ),
              const SizedBox(height: 20),
              ElevatedButton(
                onPressed: () async {
                  final result = await Navigator.of(context).push<bool>(
                    MaterialPageRoute(builder: (_) => const NewPlayerScreen()),
                  );
                  if (result == true) {
                    _loadPlayers();
                  }
                },
                child: Text(l10n.playerNewPlayer),
              ),
              const SizedBox(height: 10),
              TextButton(
                onPressed: () {
                  Navigator.of(context).pushAndRemoveUntil(
                    MaterialPageRoute(builder: (_) => const WelcomeScreen()),
                    (route) => false,
                  );
                },
                child: Text(l10n.navBack),
              ),
            ],
          ),
    );
  }
}

/// Player list tile.
class _PlayerTile extends StatelessWidget {
  const _PlayerTile({
    required this.name,
    required this.levelText,
    required this.onTap,
  });

  final String name;
  final String levelText;
  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onTap,
      child: Container(
        padding: const EdgeInsets.all(15),
        margin: const EdgeInsets.symmetric(vertical: 5),
        decoration: BoxDecoration(
          color: AppColors.darkBackground,
          borderRadius: BorderRadius.circular(5),
        ),
        child: Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Text(
              name,
              style: const TextStyle(
                fontSize: 16,
                color: AppColors.textPrimary,
              ),
            ),
            Text(
              levelText,
              style: const TextStyle(
                fontSize: 14,
                color: AppColors.textSecondary,
              ),
            ),
          ],
        ),
      ),
    );
  }
}
