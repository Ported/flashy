import 'package:flutter/material.dart';

import '../core/models.dart';
import '../theme/app_theme.dart';

/// Progress dots showing problem completion status.
class ProgressDots extends StatelessWidget {
  const ProgressDots({
    super.key,
    required this.total,
    required this.results,
    required this.currentIndex,
  });

  final int total;
  final List<ProblemResult> results;
  final int currentIndex;

  @override
  Widget build(BuildContext context) {
    return Wrap(
      spacing: 4,
      runSpacing: 4,
      alignment: WrapAlignment.center,
      children: List.generate(total, (index) {
        Color color;
        String symbol;

        if (index < results.length) {
          // Answered
          if (results[index].isCorrect) {
            color = AppColors.correctGreen;
            symbol = '●';
          } else {
            color = AppColors.incorrectRed;
            symbol = '●';
          }
        } else if (index == currentIndex) {
          // Current
          color = AppColors.starYellow;
          symbol = '◉';
        } else {
          // Pending
          color = AppColors.textSecondary;
          symbol = '○';
        }

        return Text(
          symbol,
          style: TextStyle(
            fontSize: 18,
            color: color,
          ),
        );
      }),
    );
  }
}
