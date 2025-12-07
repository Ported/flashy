import 'package:flutter/material.dart';
import 'package:flutter_localizations/flutter_localizations.dart';
import 'package:provider/provider.dart';

import 'l10n/app_localizations.dart';
import 'screens/welcome_screen.dart';
import 'state/game_state.dart';
import 'theme/app_theme.dart';

void main() {
  runApp(const FlashyApp());
}

/// Locale state management.
class LocaleState extends ChangeNotifier {
  Locale _locale = const Locale('en');

  Locale get locale => _locale;

  void setLocale(Locale locale) {
    if (_locale == locale) return;
    _locale = locale;
    notifyListeners();
  }
}

class FlashyApp extends StatelessWidget {
  const FlashyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => GameState()),
        ChangeNotifierProvider(create: (_) => LocaleState()),
      ],
      child: Consumer<LocaleState>(
        builder: (context, localeState, _) => MaterialApp(
          title: "Flashy's Math Adventure",
          theme: AppTheme.darkTheme,
          debugShowCheckedModeBanner: false,
          locale: localeState.locale,
          supportedLocales: AppLocalizations.supportedLocales,
          localizationsDelegates: const [
            AppLocalizations.delegate,
            GlobalMaterialLocalizations.delegate,
            GlobalWidgetsLocalizations.delegate,
            GlobalCupertinoLocalizations.delegate,
          ],
          home: const AppShell(),
        ),
      ),
    );
  }
}

/// App shell that initializes state and shows the welcome screen.
class AppShell extends StatefulWidget {
  const AppShell({super.key});

  @override
  State<AppShell> createState() => _AppShellState();
}

class _AppShellState extends State<AppShell> {
  @override
  void initState() {
    super.initState();
    // Initialize game state
    WidgetsBinding.instance.addPostFrameCallback((_) {
      context.read<GameState>().initialize();
    });
  }

  @override
  Widget build(BuildContext context) {
    final gameState = context.watch<GameState>();

    if (!gameState.isInitialized) {
      return const Scaffold(
        body: Center(
          child: CircularProgressIndicator(),
        ),
      );
    }

    return const WelcomeScreen();
  }
}
