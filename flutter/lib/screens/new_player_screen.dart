import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../l10n/app_localizations.dart';
import '../state/game_state.dart';
import '../theme/app_theme.dart';
import '../widgets/animated_button.dart';
import '../widgets/responsive_container.dart';
import 'intro_screen.dart';

/// New player creation screen.
class NewPlayerScreen extends StatefulWidget {
  const NewPlayerScreen({super.key});

  @override
  State<NewPlayerScreen> createState() => _NewPlayerScreenState();
}

class _NewPlayerScreenState extends State<NewPlayerScreen> {
  final _controller = TextEditingController();
  String? _error;
  bool _loading = false;

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  Future<void> _createPlayer() async {
    final l10n = AppLocalizations.of(context)!;
    final name = _controller.text.trim();

    if (name.isEmpty) {
      setState(() => _error = l10n.playerErrorEmpty);
      return;
    }

    setState(() {
      _error = null;
      _loading = true;
    });

    final gameState = context.read<GameState>();
    final error = await gameState.createPlayer(name);

    if (!mounted) return;

    if (error != null) {
      setState(() {
        _error = error;
        _loading = false;
      });
      return;
    }

    // Success - go to intro
    Navigator.of(context).pushReplacement(
      MaterialPageRoute(builder: (_) => const IntroScreen()),
    );
  }

  @override
  Widget build(BuildContext context) {
    final l10n = AppLocalizations.of(context)!;

    return BaseScreen(
      child: Column(
            children: [
              Text(
                l10n.playerNewTitle,
                style: Theme.of(context).textTheme.headlineMedium,
                textAlign: TextAlign.center,
              ),
              const SizedBox(height: 30),
              TextField(
                controller: _controller,
                decoration: InputDecoration(
                  hintText: l10n.playerEnterName,
                ),
                maxLength: 20,
                textCapitalization: TextCapitalization.words,
                enabled: !_loading,
                onSubmitted: (_) => _createPlayer(),
              ),
              if (_error != null) ...[
                const SizedBox(height: 10),
                Text(
                  _error!,
                  style: const TextStyle(
                    color: AppColors.dangerRed,
                  ),
                  textAlign: TextAlign.center,
                ),
              ],
              const SizedBox(height: 20),
              if (_loading)
                const CircularProgressIndicator()
              else
                Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    AnimatedElevatedButton(
                      onPressed: _createPlayer,
                      child: Text(l10n.playerCreate),
                    ),
                    const SizedBox(width: 10),
                    AnimatedElevatedButton(
                      onPressed: () => Navigator.of(context).pop(false),
                      style: ElevatedButton.styleFrom(
                        backgroundColor: AppColors.dangerRed,
                      ),
                      child: Text(l10n.playerCancel),
                    ),
                  ],
                ),
            ],
          ),
    );
  }
}
