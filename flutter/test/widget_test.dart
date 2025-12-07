import 'package:flutter/material.dart';
import 'package:flutter_localizations/flutter_localizations.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:provider/provider.dart';

import 'package:flashy_app/core/storage.dart';
import 'package:flashy_app/l10n/app_localizations.dart';
import 'package:flashy_app/main.dart';
import 'package:flashy_app/screens/welcome_screen.dart';
import 'package:flashy_app/state/game_state.dart';
import 'package:flashy_app/theme/app_theme.dart';

/// Helper to create a localized test app with providers.
Widget createTestApp({required Widget child, LocaleState? localeState}) {
  final storage = MemoryStorageBackend();
  final locale = localeState ?? LocaleState();

  return MultiProvider(
    providers: [
      ChangeNotifierProvider(create: (_) => GameState(storage: storage)),
      ChangeNotifierProvider.value(value: locale),
    ],
    child: Consumer<LocaleState>(
      builder: (context, localeState, _) => MaterialApp(
        title: "Flashy's Math Adventure",
        theme: AppTheme.darkTheme,
        locale: localeState.locale,
        supportedLocales: AppLocalizations.supportedLocales,
        localizationsDelegates: const [
          AppLocalizations.delegate,
          GlobalMaterialLocalizations.delegate,
          GlobalWidgetsLocalizations.delegate,
          GlobalCupertinoLocalizations.delegate,
        ],
        home: child,
      ),
    ),
  );
}

void main() {
  testWidgets('App renders welcome screen', (WidgetTester tester) async {
    await tester.pumpWidget(createTestApp(child: const WelcomeScreen()));
    await tester.pump();

    // Verify the app title is displayed
    expect(find.text("Flashy's Math Adventure"), findsOneWidget);
  });

  testWidgets('Language switch changes text to Swedish', (WidgetTester tester) async {
    await tester.pumpWidget(createTestApp(child: const WelcomeScreen()));
    await tester.pump();

    // Verify English text
    expect(find.text("Flashy's Math Adventure"), findsOneWidget);
    expect(find.text('Help Flashy find the way home!'), findsOneWidget);

    // Tap Swedish language button
    await tester.tap(find.text('SV'));
    await tester.pumpAndSettle();

    // Verify Swedish text
    expect(find.text("Flashy's Matematikäventyr"), findsOneWidget);
    expect(find.text('Hjälp Flashy att hitta hem!'), findsOneWidget);
  });

  testWidgets('Language switch back to English', (WidgetTester tester) async {
    final localeState = LocaleState()..setLocale(const Locale('sv'));

    await tester.pumpWidget(createTestApp(
      child: const WelcomeScreen(),
      localeState: localeState,
    ));
    await tester.pumpAndSettle();

    // Verify Swedish text
    expect(find.text("Flashy's Matematikäventyr"), findsOneWidget);

    // Tap English language button
    await tester.tap(find.text('EN'));
    await tester.pumpAndSettle();

    // Verify English text
    expect(find.text("Flashy's Math Adventure"), findsOneWidget);
  });
}
