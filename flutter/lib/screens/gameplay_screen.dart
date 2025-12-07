import 'dart:async';

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:provider/provider.dart';

import '../core/game.dart';
import '../l10n/app_localizations.dart';
import '../state/game_state.dart';
import '../theme/app_theme.dart';
import '../widgets/numpad.dart';
import '../widgets/progress_dots.dart';
import '../widgets/responsive_container.dart';
import 'result_screen.dart';

/// Gameplay screen with math problems and numpad.
class GameplayScreen extends StatefulWidget {
  const GameplayScreen({super.key, required this.levelNumber});

  final int levelNumber;

  @override
  State<GameplayScreen> createState() => _GameplayScreenState();
}

class _GameplayScreenState extends State<GameplayScreen> {
  GameController? _controller;
  String _currentAnswer = '';
  DateTime? _problemStartTime;
  Timer? _timer;
  double _elapsedTime = 0;
  bool _showingFeedback = false;
  AnswerFeedback? _lastFeedback;
  final FocusNode _focusNode = FocusNode();

  @override
  void initState() {
    super.initState();
    // Defer state modification to avoid calling notifyListeners during build
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (!mounted) return;
      final gameState = context.read<GameState>();
      gameState.startLevel(widget.levelNumber);
      final controller = gameState.gameController!;
      _controller = controller;
      _startProblem();

      // Start timer if boss battle
      if (controller.isTimed) {
        _timer = Timer.periodic(const Duration(seconds: 1), (_) {
          if (!mounted) return;
          setState(() {
            _elapsedTime += 1;
            if (controller.isTimeExpired(_elapsedTime)) {
              _finishLevel();
            }
          });
        });
      }
      setState(() {}); // Trigger rebuild now that controller is ready
    });
  }

  @override
  void dispose() {
    _timer?.cancel();
    _focusNode.dispose();
    super.dispose();
  }

  void _startProblem() {
    _problemStartTime = DateTime.now();
    _currentAnswer = '';
    _showingFeedback = false;
    _lastFeedback = null;
  }

  void _submitAnswer() {
    final controller = _controller;
    if (controller == null) return;
    if (_showingFeedback || _currentAnswer.isEmpty || _currentAnswer == '-') {
      return;
    }

    final answer = int.tryParse(_currentAnswer);
    final timeTaken =
        DateTime.now().difference(_problemStartTime!).inMilliseconds / 1000.0;

    final feedback = controller.submitAnswer(answer, timeTaken: timeTaken);

    setState(() {
      _lastFeedback = feedback;
      _showingFeedback = true;
    });

    // Show feedback for 500ms, then move to next problem or finish
    Future.delayed(const Duration(milliseconds: 500), () {
      if (!mounted) return;

      if (controller.isComplete) {
        _finishLevel();
      } else {
        setState(() {
          _startProblem();
        });
      }
    });
  }

  void _addDigit(String digit) {
    if (_showingFeedback) return;
    if (digit == '-' && _currentAnswer.isNotEmpty) return;
    setState(() {
      _currentAnswer += digit;
    });
  }

  void _backspace() {
    if (_showingFeedback || _currentAnswer.isEmpty) return;
    setState(() {
      _currentAnswer = _currentAnswer.substring(0, _currentAnswer.length - 1);
    });
  }

  Future<void> _finishLevel() async {
    _timer?.cancel();
    final controller = _controller;
    if (controller == null) return;

    final gameState = context.read<GameState>();
    final (stars, isNewBest) = await gameState.finishLevel();

    if (!mounted) return;

    Navigator.of(context).pushReplacement(
      MaterialPageRoute(
        builder: (_) => ResultScreen(
          levelNumber: widget.levelNumber,
          stars: stars,
          isNewBest: isNewBest,
          correctCount: controller.correctCount,
          totalProblems: controller.totalProblems,
          score: controller.totalScore,
          bestStreak: controller.bestStreak,
        ),
      ),
    );
  }

  void _handleKeyEvent(KeyEvent event) {
    if (event is! KeyDownEvent) return;

    final key = event.logicalKey;

    // Number keys
    if (key == LogicalKeyboardKey.digit0 ||
        key == LogicalKeyboardKey.numpad0) {
      _addDigit('0');
    } else if (key == LogicalKeyboardKey.digit1 ||
        key == LogicalKeyboardKey.numpad1) {
      _addDigit('1');
    } else if (key == LogicalKeyboardKey.digit2 ||
        key == LogicalKeyboardKey.numpad2) {
      _addDigit('2');
    } else if (key == LogicalKeyboardKey.digit3 ||
        key == LogicalKeyboardKey.numpad3) {
      _addDigit('3');
    } else if (key == LogicalKeyboardKey.digit4 ||
        key == LogicalKeyboardKey.numpad4) {
      _addDigit('4');
    } else if (key == LogicalKeyboardKey.digit5 ||
        key == LogicalKeyboardKey.numpad5) {
      _addDigit('5');
    } else if (key == LogicalKeyboardKey.digit6 ||
        key == LogicalKeyboardKey.numpad6) {
      _addDigit('6');
    } else if (key == LogicalKeyboardKey.digit7 ||
        key == LogicalKeyboardKey.numpad7) {
      _addDigit('7');
    } else if (key == LogicalKeyboardKey.digit8 ||
        key == LogicalKeyboardKey.numpad8) {
      _addDigit('8');
    } else if (key == LogicalKeyboardKey.digit9 ||
        key == LogicalKeyboardKey.numpad9) {
      _addDigit('9');
    } else if (key == LogicalKeyboardKey.minus ||
        key == LogicalKeyboardKey.numpadSubtract) {
      _addDigit('-');
    } else if (key == LogicalKeyboardKey.backspace) {
      _backspace();
    } else if (key == LogicalKeyboardKey.enter ||
        key == LogicalKeyboardKey.numpadEnter) {
      _submitAnswer();
    }
    // Cheat codes for dev
    else if (key == LogicalKeyboardKey.f9) {
      _controller?.cheatPassAll();
      _finishLevel();
    } else if (key == LogicalKeyboardKey.f10) {
      _controller?.cheatFailAll();
      _finishLevel();
    }
  }

  @override
  Widget build(BuildContext context) {
    final l10n = AppLocalizations.of(context)!;
    final controller = _controller;

    // Show loading while controller initializes
    if (controller == null) {
      return const Scaffold(
        body: Center(child: CircularProgressIndicator()),
      );
    }

    final isBoss = controller.isTimed;
    final problem = controller.currentProblem;

    return Scaffold(
      body: SafeArea(
        child: KeyboardListener(
          focusNode: _focusNode,
          autofocus: true,
          onKeyEvent: _handleKeyEvent,
          child: Center(
            child: ConstrainedBox(
              constraints: const BoxConstraints(maxWidth: BaseScreenConfig.maxWidth),
              child: SizedBox.expand(
                child: Container(
                  margin: BaseScreenConfig.margin,
                  decoration: BoxDecoration(
                    border: Border.all(
                      color: BaseScreenConfig.borderColor,
                      width: BaseScreenConfig.borderWidth,
                    ),
                    borderRadius: BorderRadius.circular(BaseScreenConfig.borderRadius),
                  ),
                  child: SingleChildScrollView(
                    child: Padding(
                      padding: BaseScreenConfig.padding,
                      child: Column(
                        children: [
                // Title
                Text(
                  isBoss
                      ? l10n.gameplayBossLevel(widget.levelNumber)
                      : l10n.gameplayLevel(widget.levelNumber),
                  style: TextStyle(
                    fontSize: 16,
                    fontWeight: FontWeight.bold,
                    color: isBoss
                        ? AppColors.incorrectRed
                        : AppColors.correctGreen,
                  ),
                ),

                // Timer for boss battles
                if (isBoss) ...[
                  const SizedBox(height: 5),
                  _TimerDisplay(
                    remaining: controller.timeRemaining(_elapsedTime),
                  ),
                ],

                // Score bar
                const SizedBox(height: 5),
                _ScoreBar(
                  score: controller.totalScore,
                  streak: controller.streak,
                ),

                // Progress dots
                const SizedBox(height: 5),
                ProgressDots(
                  total: controller.totalProblems,
                  results: controller.results,
                  currentIndex: controller.problemIndex,
                ),

                // Problem display
                const SizedBox(height: 10),
                _ProblemDisplay(
                  problemText: problem?.display() ?? '',
                  showingFeedback: _showingFeedback,
                  feedback: _lastFeedback,
                ),

                // Answer box and enter button
                const SizedBox(height: 10),
                Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    _AnswerBox(
                      answer: _currentAnswer,
                      hasInput: _currentAnswer.isNotEmpty,
                    ),
                    const SizedBox(width: 10),
                    ElevatedButton(
                      onPressed: _submitAnswer,
                      style: ElevatedButton.styleFrom(
                        backgroundColor: AppColors.correctGreen,
                        padding: const EdgeInsets.symmetric(
                          horizontal: 25,
                          vertical: 15,
                        ),
                      ),
                      child: Text(
                        l10n.gameplayEnter,
                        style: const TextStyle(
                          fontSize: 20,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ),
                  ],
                ),

                // Hint
                const SizedBox(height: 5),
                Text(
                  l10n.gameplayTypeAnswer,
                  style: TextStyle(
                    fontSize: 14,
                    color: AppColors.textSecondary,
                  ),
                ),

                // Numpad
                const SizedBox(height: 15),
                Numpad(
                  onDigit: _addDigit,
                  onBackspace: _backspace,
                  onEnter: _submitAnswer,
                ),
                        ],
                      ),
                    ),
                  ),
                ),
              ),
            ),
          ),
        ),
      ),
    );
  }
}

/// Timer display for boss battles.
class _TimerDisplay extends StatelessWidget {
  const _TimerDisplay({required this.remaining});

  final double remaining;

  @override
  Widget build(BuildContext context) {
    final isLow = remaining <= 15;
    final mins = (remaining ~/ 60).toString();
    final secs = (remaining % 60).toInt().toString().padLeft(2, '0');

    return Text(
      '$mins:$secs',
      style: TextStyle(
        fontSize: 24,
        fontWeight: FontWeight.bold,
        color: isLow ? AppColors.incorrectRed : AppColors.starYellow,
      ),
    );
  }
}

/// Score bar showing current score and streak.
class _ScoreBar extends StatelessWidget {
  const _ScoreBar({required this.score, required this.streak});

  final int score;
  final int streak;

  @override
  Widget build(BuildContext context) {
    final l10n = AppLocalizations.of(context)!;
    return Text(
      streak >= 2
          ? l10n.gameplayStreak(score, streak)
          : l10n.gameplayScore(score),
      style: const TextStyle(
        fontSize: 14,
        color: AppColors.starYellow,
      ),
    );
  }
}

/// Problem display with feedback.
class _ProblemDisplay extends StatelessWidget {
  const _ProblemDisplay({
    required this.problemText,
    required this.showingFeedback,
    this.feedback,
  });

  final String problemText;
  final bool showingFeedback;
  final AnswerFeedback? feedback;

  @override
  Widget build(BuildContext context) {
    final l10n = AppLocalizations.of(context)!;

    if (showingFeedback && feedback != null) {
      if (feedback!.isCorrect) {
        return Text(
          l10n.gameplayPointsEarned(feedback!.pointsEarned),
          style: const TextStyle(
            fontSize: 48,
            fontWeight: FontWeight.bold,
            color: AppColors.correctGreen,
          ),
        );
      } else {
        return Text(
          l10n.gameplayWrong,
          style: const TextStyle(
            fontSize: 48,
            fontWeight: FontWeight.bold,
            color: AppColors.incorrectRed,
          ),
        );
      }
    }

    return Text(
      '$problemText = ?',
      style: const TextStyle(
        fontSize: 48,
        fontWeight: FontWeight.bold,
        color: Colors.white,
      ),
    );
  }
}

/// Answer input box.
class _AnswerBox extends StatelessWidget {
  const _AnswerBox({required this.answer, required this.hasInput});

  final String answer;
  final bool hasInput;

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 25, vertical: 10),
      constraints: const BoxConstraints(minWidth: 120),
      decoration: BoxDecoration(
        color: hasInput ? const Color(0xFF1a2e1a) : AppColors.darkBackground,
        border: Border.all(
          color: hasInput ? AppColors.correctGreen : AppColors.accentCyan,
          width: 2,
        ),
        borderRadius: BorderRadius.circular(8),
      ),
      child: Text(
        answer.isEmpty ? ' ' : answer,
        style: const TextStyle(
          fontSize: 32,
          fontWeight: FontWeight.bold,
          color: Colors.white,
        ),
        textAlign: TextAlign.center,
      ),
    );
  }
}
