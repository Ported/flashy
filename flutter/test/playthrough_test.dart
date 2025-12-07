// Full game playthrough test - verifies complete game flow from start to finish.
//
// This test plays through all 40 levels (4 worlds x 10 levels) by solving
// every math problem, verifying the entire game is playable.
// Tests run in both English and Swedish to verify localization.

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_localizations/flutter_localizations.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:provider/provider.dart';

import 'package:flashy_app/api/flashy_api.dart';
import 'package:flashy_app/core/game.dart';
import 'package:flashy_app/core/storage.dart';
import 'package:flashy_app/l10n/app_localizations.dart';
import 'package:flashy_app/main.dart';
import 'package:flashy_app/screens/welcome_screen.dart';
import 'package:flashy_app/state/game_state.dart';
import 'package:flashy_app/theme/app_theme.dart';

/// Localized strings helper for tests.
/// Provides the correct strings based on locale.
class L10nStrings {
  L10nStrings(this.locale);

  final Locale locale;

  bool get isSwedish => locale.languageCode == 'sv';

  // Navigation
  String get play => isSwedish ? 'Spela' : 'Play';
  String get newPlayer => isSwedish ? 'Ny spelare' : 'New Player';
  String get create => isSwedish ? 'Skapa' : 'Create';
  String get continueButton => isSwedish ? 'Fortsätt' : 'Continue';
  String get leaderboard => isSwedish ? 'Topplista' : 'Leaderboard';

  // Intro
  String get flashy => 'FLASHY'; // Same in both languages

  // World names
  String get world1Name => isSwedish ? 'Additions-Alperna' : 'Addition Alps';
  String get world2Name =>
      isSwedish ? 'Subtraktions-Träsket' : 'Subtraction Swamp';
  String get world3Name =>
      isSwedish ? 'Multiplikations-Ängarna' : 'Multiplication Meadows';
  String get world4Name => isSwedish ? 'Divisions-Öknen' : 'Division Desert';

  // Results
  String get levelComplete => isSwedish ? 'Nivå klar!' : 'Level Complete!';
  String get keepPracticing => isSwedish ? 'Fortsätt träna!' : 'Keep Practicing!';

  // Game complete
  String get gameCompleteTitle =>
      isSwedish ? 'ÄNTLIGEN HEMMA!' : 'HOME AT LAST!';

  // Friend meet - partial match
  String get meetPartial => isSwedish ? 'Jag är' : 'Meet';
}

/// Mock API that always succeeds for testing.
class TestFlashyApi extends FlashyApi {
  @override
  Future<bool> checkNameAvailable(String name) async => true;

  @override
  Future<RegisterResult> register(String name) async {
    return RegisterResult(
      success: true,
      playerName: name,
      token: 'test-token-$name',
    );
  }

  @override
  Future<List<LeaderboardEntry>> getLeaderboard() async => [];

  @override
  Future<SyncResult> syncScore({
    required String playerName,
    required String token,
    required int totalScore,
    required int highestLevel,
    required int totalStars,
  }) async {
    return const SyncResult(success: true, rank: 1);
  }
}

/// Test wrapper that provides mocked dependencies.
class TestApp extends StatelessWidget {
  const TestApp({
    super.key,
    required this.storage,
    required this.api,
    this.locale = const Locale('en'),
  });

  final MemoryStorageBackend storage;
  final TestFlashyApi api;
  final Locale locale;

  @override
  Widget build(BuildContext context) {
    return MultiProvider(
      providers: [
        ChangeNotifierProvider(
            create: (_) => GameState(storage: storage, api: api)),
        ChangeNotifierProvider(create: (_) => LocaleState()..setLocale(locale)),
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
          home: const _AppShell(),
        ),
      ),
    );
  }
}

class _AppShell extends StatefulWidget {
  const _AppShell();

  @override
  State<_AppShell> createState() => _AppShellState();
}

class _AppShellState extends State<_AppShell> {
  bool _initialized = false;

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    if (!_initialized) {
      _init();
    }
  }

  Future<void> _init() async {
    // Schedule for after the current build
    WidgetsBinding.instance.addPostFrameCallback((_) async {
      await context.read<GameState>().initialize();
      if (mounted) {
        setState(() => _initialized = true);
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    if (!_initialized) {
      return const Scaffold(body: Center(child: CircularProgressIndicator()));
    }
    return const WelcomeScreen();
  }
}

void main() {
  test('Level 6 direct solve gives 2+ stars', () async {
    final storage = MemoryStorageBackend();
    final controller = GameController(
      playerName: 'TestPlayer',
      levelNumber: 6,
      storage: storage,
    );

    // Answer all 10 problems correctly with quick times
    for (var i = 0; i < 10; i++) {
      final problem = controller.currentProblem!;
      final feedback =
          controller.submitAnswer(problem.answer, timeTaken: 2.0);
      expect(feedback.isCorrect, true, reason: 'Problem $i should be correct');
    }

    expect(controller.isComplete, true);
    expect(controller.correctCount, 10);

    // Finish and check stars
    final (stars, _) = await controller.finish();
    expect(stars, greaterThanOrEqualTo(2),
        reason: '100% correct should give at least 2 stars');
  });

  // Run localization tests for both English and Swedish
  for (final locale in [const Locale('en'), const Locale('sv')]) {
    final langName = locale.languageCode == 'en' ? 'English' : 'Swedish';
    final l10n = L10nStrings(locale);

    testWidgets('[$langName] Level 6 to 7 progression', (tester) async {
      final storage = MemoryStorageBackend();
      final api = TestFlashyApi();

      await tester.pumpWidget(TestApp(storage: storage, api: api, locale: locale));
      await tester.pumpAndSettle();

      // Navigate to gameplay
      await tester.tap(find.text(l10n.play));
      await tester.pumpAndSettle();
      await tester.tap(find.text(l10n.newPlayer));
      await tester.pumpAndSettle();
      await tester.enterText(find.byType(TextField), 'TestLevel6$langName');
      await tester.tap(find.text(l10n.create));
      await tester.pumpAndSettle();

      // Skip intro screens
      await tester.tap(find.byType(GestureDetector).first);
      await tester.pumpAndSettle();
      await tester.tap(find.byType(GestureDetector).first);
      await tester.pumpAndSettle();

      // Complete levels 1-5 to unlock level 6
      for (var level = 1; level <= 5; level++) {
        await tester.tap(find.text('$level').first);
        await tester.pumpAndSettle();
        await _completeLevel(tester, l10n);
        expect(find.text(l10n.continueButton), findsOneWidget);
        await tester.tap(find.text(l10n.continueButton));
        await tester.pumpAndSettle();
      }

      // Now on world map - tap level 6 (should show friend meet)
      expect(find.text('6'), findsWidgets, reason: 'Level 6 should be visible');
      await tester.tap(find.text('6').first);
      await tester.pumpAndSettle();

      // Friend meet screen - look for partial text that appears in intro
      await tester.tap(find.byType(GestureDetector).first);
      await tester.pumpAndSettle();

      // Complete level 6
      await _completeLevel(tester, l10n);
      expect(find.text(l10n.continueButton), findsOneWidget);
      await tester.tap(find.text(l10n.continueButton));
      await tester.pumpAndSettle();

      // Should be back on world map with level 7 unlocked
      expect(find.text(l10n.leaderboard), findsOneWidget,
          reason: 'Should be on world map');
      expect(find.text('7'), findsWidgets,
          reason: 'Level 7 should be visible after completing level 6');
    });

    testWidgets('[$langName] Full game playthrough - all 40 levels',
        (tester) async {
      // Set a larger screen size to avoid overflow errors
      await tester.binding.setSurfaceSize(const Size(800, 1200));

      final storage = MemoryStorageBackend();
      final api = TestFlashyApi();

      await tester.pumpWidget(TestApp(storage: storage, api: api, locale: locale));
      await tester.pumpAndSettle();

      // Welcome screen - tap Play
      expect(find.text(l10n.play), findsOneWidget);
      await tester.tap(find.text(l10n.play));
      await tester.pumpAndSettle();

      // Player select - tap New Player
      expect(find.text(l10n.newPlayer), findsOneWidget);
      await tester.tap(find.text(l10n.newPlayer));
      await tester.pumpAndSettle();

      // New player screen - enter name and create
      await tester.enterText(find.byType(TextField), 'Test$langName');
      await tester.tap(find.text(l10n.create));
      await tester.pumpAndSettle();

      // Intro screen - tap to continue
      expect(find.textContaining(l10n.flashy), findsWidgets);
      await tester.tap(find.byType(GestureDetector).first);
      await tester.pumpAndSettle();

      // World intro screen - tap to continue
      expect(find.textContaining(l10n.world1Name), findsWidgets);
      await tester.tap(find.byType(GestureDetector).first);
      await tester.pumpAndSettle();

      // Now on world map - play through all 4 worlds
      final worldNames = [
        l10n.world1Name,
        l10n.world2Name,
        l10n.world3Name,
        l10n.world4Name,
      ];

      for (var world = 1; world <= 4; world++) {
        for (var levelInWorld = 1; levelInWorld <= 10; levelInWorld++) {
          final globalLevel = (world - 1) * 10 + levelInWorld;

          // Find and tap the level node
          // Levels should be visible - find by level number text
          final levelFinder = find.text('$levelInWorld');
          expect(levelFinder, findsWidgets,
              reason:
                  'Level $levelInWorld should be visible on world $world map');

          // Tap the level node (it's inside a GestureDetector)
          await tester.tap(levelFinder.first);
          await tester.pumpAndSettle();

          // Level 6: Friend meet screen
          if (levelInWorld == 6) {
            await tester.tap(find.byType(GestureDetector).first);
            await tester.pumpAndSettle();
          }

          // Level 10: Boss intro screen
          if (levelInWorld == 10) {
            // Boss intro appears before gameplay
            await tester.tap(find.byType(GestureDetector).first);
            await tester.pumpAndSettle();
          }

          // Now in gameplay - solve all problems
          await _completeLevel(tester, l10n);

          // Result screen - tap Continue
          expect(find.text(l10n.continueButton), findsOneWidget,
              reason: 'Result screen should show Continue button');
          await tester.tap(find.text(l10n.continueButton));
          await tester.pumpAndSettle();

          // Level 10: Boss victory screen
          if (levelInWorld == 10) {
            // Tap to continue past victory
            await tester.tap(find.byType(GestureDetector).first);
            await tester.pumpAndSettle();

            if (world < 4) {
              // World intro for next world - tap to continue
              // Verify the correct world name appears
              expect(find.textContaining(worldNames[world]), findsWidgets,
                  reason: 'World ${world + 1} intro should show ${worldNames[world]}');
              await tester.tap(find.byType(GestureDetector).first);
              await tester.pumpAndSettle();
            }
          }

          // Should be back on world map (or game complete after final boss)
          if (!(world == 4 && levelInWorld == 10)) {
            // Verify we're on world map by checking for Leaderboard button
            expect(find.text(l10n.leaderboard), findsOneWidget,
                reason:
                    'Should be on world map after level $globalLevel (world $world, level $levelInWorld)');
          }
        }
      }

      // Game complete screen - Flashy made it home!
      expect(find.textContaining(l10n.gameCompleteTitle), findsOneWidget,
          reason: 'Game complete screen should show');
    }, timeout: const Timeout(Duration(minutes: 5)));

    testWidgets('[$langName] Level 1 completes with correct answers',
        (tester) async {
      final storage = MemoryStorageBackend();
      final api = TestFlashyApi();

      await tester.pumpWidget(TestApp(storage: storage, api: api, locale: locale));
      await tester.pumpAndSettle();

      // Navigate to gameplay
      await tester.tap(find.text(l10n.play));
      await tester.pumpAndSettle();
      await tester.tap(find.text(l10n.newPlayer));
      await tester.pumpAndSettle();
      await tester.enterText(find.byType(TextField), 'Quick$langName');
      await tester.tap(find.text(l10n.create));
      await tester.pumpAndSettle();

      // Skip intro screens
      await tester.tap(find.byType(GestureDetector).first);
      await tester.pumpAndSettle();
      await tester.tap(find.byType(GestureDetector).first);
      await tester.pumpAndSettle();

      // Tap level 1
      await tester.tap(find.text('1').first);
      await tester.pumpAndSettle();

      // Complete the level by solving problems
      await _completeLevel(tester, l10n);

      // Verify result screen shows
      expect(find.text(l10n.continueButton), findsOneWidget);
      expect(find.textContaining(l10n.levelComplete), findsOneWidget);
    });

    testWidgets('[$langName] F10 cheat code fails level', (tester) async {
      final storage = MemoryStorageBackend();
      final api = TestFlashyApi();

      await tester.pumpWidget(TestApp(storage: storage, api: api, locale: locale));
      await tester.pumpAndSettle();

      // Navigate to gameplay
      await tester.tap(find.text(l10n.play));
      await tester.pumpAndSettle();
      await tester.tap(find.text(l10n.newPlayer));
      await tester.pumpAndSettle();
      await tester.enterText(find.byType(TextField), 'Fail$langName');
      await tester.tap(find.text(l10n.create));
      await tester.pumpAndSettle();

      // Skip intro screens
      await tester.tap(find.byType(GestureDetector).first);
      await tester.pumpAndSettle();
      await tester.tap(find.byType(GestureDetector).first);
      await tester.pumpAndSettle();

      // Tap level 1
      await tester.tap(find.text('1').first);
      await tester.pumpAndSettle();

      // Use F10 cheat to fail all problems
      await tester.sendKeyEvent(LogicalKeyboardKey.f10);
      await tester.pumpAndSettle();

      // Verify result screen shows failed message (0 stars)
      expect(find.text(l10n.continueButton), findsOneWidget);
      expect(find.textContaining(l10n.keepPracticing), findsOneWidget);

      // Should show 0 / 10 correct (note spaces around /)
      expect(find.textContaining('0 / 10'), findsOneWidget);

      // Should have 0 stars (shown as ···)
      expect(find.text('···'), findsOneWidget);
    });

    testWidgets('[$langName] F9 cheat code passes level with 3 stars',
        (tester) async {
      final storage = MemoryStorageBackend();
      final api = TestFlashyApi();

      await tester.pumpWidget(TestApp(storage: storage, api: api, locale: locale));
      await tester.pumpAndSettle();

      // Navigate to gameplay
      await tester.tap(find.text(l10n.play));
      await tester.pumpAndSettle();
      await tester.tap(find.text(l10n.newPlayer));
      await tester.pumpAndSettle();
      await tester.enterText(find.byType(TextField), 'Pass$langName');
      await tester.tap(find.text(l10n.create));
      await tester.pumpAndSettle();

      // Skip intro screens
      await tester.tap(find.byType(GestureDetector).first);
      await tester.pumpAndSettle();
      await tester.tap(find.byType(GestureDetector).first);
      await tester.pumpAndSettle();

      // Tap level 1
      await tester.tap(find.text('1').first);
      await tester.pumpAndSettle();

      // Use F9 cheat to pass all problems
      await tester.sendKeyEvent(LogicalKeyboardKey.f9);
      await tester.pumpAndSettle();

      // Verify result screen shows "Level Complete"
      expect(find.text(l10n.continueButton), findsOneWidget);
      expect(find.textContaining(l10n.levelComplete), findsOneWidget);

      // Should show 10 / 10 correct (note spaces around /)
      expect(find.textContaining('10 / 10'), findsOneWidget);

      // Should have 3 stars (shown as ⭐⭐⭐)
      expect(find.text('⭐⭐⭐'), findsOneWidget);
    });
  }
}

/// Complete a level by solving all math problems.
Future<void> _completeLevel(WidgetTester tester, L10nStrings l10n,
    {bool debug = false}) async {
  // Keep solving until we see the result screen
  var attempts = 0;
  var solved = 0;
  var failed = 0;
  const maxAttempts = 50; // Safety limit

  while (attempts < maxAttempts) {
    attempts++;
    await tester.pumpAndSettle();

    // Check if we're on the result screen (use localized strings)
    if (find.text(l10n.continueButton).evaluate().isNotEmpty &&
        (find.textContaining(l10n.levelComplete).evaluate().isNotEmpty ||
            find.textContaining(l10n.keepPracticing).evaluate().isNotEmpty)) {
      if (debug) debugPrint('Level done: solved=$solved, failed=$failed');
      break;
    }

    // Find and solve the current problem
    final problemFinder = find.textContaining('= ?');
    if (problemFinder.evaluate().isEmpty) {
      // No problem visible yet, pump more
      await tester.pump(const Duration(milliseconds: 100));
      continue;
    }

    final problemText =
        (problemFinder.evaluate().first.widget as Text).data ?? '';
    final answer = _solveProblem(problemText);

    if (answer != null) {
      if (debug) debugPrint('Problem: $problemText -> $answer');
      // Type the answer
      await _typeAnswer(tester, answer, debug: debug);
      solved++;
      // Wait for feedback
      await tester.pump(const Duration(milliseconds: 600));
    } else {
      if (debug) debugPrint('FAILED to parse: $problemText');
      failed++;
      // Couldn't parse - just wait and try again
      await tester.pump(const Duration(milliseconds: 100));
    }
  }
}

/// Parse a problem string and return the correct answer.
int? _solveProblem(String problemText) {
  // Parse problems like "5 + 3 = ?" or "-20 - (-8) = ?"
  // Operations: + - × ÷
  final regex = RegExp(r'(-?\d+)\s*([+\-×÷])\s*\(?(-?\d+)\)?\s*=');
  final match = regex.firstMatch(problemText);

  if (match == null) return null;

  final operand1 = int.parse(match.group(1)!);
  final op = match.group(2)!;
  final operand2 = int.parse(match.group(3)!);

  switch (op) {
    case '+':
      return operand1 + operand2;
    case '-':
      return operand1 - operand2;
    case '×':
      return operand1 * operand2;
    case '÷':
      return operand1 ~/ operand2;
    default:
      return null;
  }
}

/// Type an answer using keyboard events.
Future<void> _typeAnswer(WidgetTester tester, int answer,
    {bool debug = false}) async {
  final answerStr = answer.toString();

  // Use keyboard events which are more reliable than finding/tapping buttons
  for (final char in answerStr.split('')) {
    switch (char) {
      case '-':
        await tester.sendKeyEvent(LogicalKeyboardKey.minus);
      case '0':
        await tester.sendKeyEvent(LogicalKeyboardKey.digit0);
      case '1':
        await tester.sendKeyEvent(LogicalKeyboardKey.digit1);
      case '2':
        await tester.sendKeyEvent(LogicalKeyboardKey.digit2);
      case '3':
        await tester.sendKeyEvent(LogicalKeyboardKey.digit3);
      case '4':
        await tester.sendKeyEvent(LogicalKeyboardKey.digit4);
      case '5':
        await tester.sendKeyEvent(LogicalKeyboardKey.digit5);
      case '6':
        await tester.sendKeyEvent(LogicalKeyboardKey.digit6);
      case '7':
        await tester.sendKeyEvent(LogicalKeyboardKey.digit7);
      case '8':
        await tester.sendKeyEvent(LogicalKeyboardKey.digit8);
      case '9':
        await tester.sendKeyEvent(LogicalKeyboardKey.digit9);
    }
    if (debug) debugPrint('Sent key: $char');
    await tester.pump(const Duration(milliseconds: 50));
  }

  // Press Enter
  await tester.sendKeyEvent(LogicalKeyboardKey.enter);
  if (debug) debugPrint('Sent Enter');
  await tester.pump();
}
