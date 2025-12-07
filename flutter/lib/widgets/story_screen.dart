import 'package:flutter/material.dart';

import '../theme/app_theme.dart';
import 'responsive_container.dart';

/// Reusable story screen layout with tap-to-continue.
class StoryScreenLayout extends StatelessWidget {
  const StoryScreenLayout({
    super.key,
    required this.title,
    required this.storyText,
    required this.onContinue,
    this.titleColor = AppColors.accentCyan,
    this.asciiArt,
    this.hint = 'Tap anywhere to continue...',
  });

  final String title;
  final String storyText;
  final VoidCallback onContinue;
  final Color titleColor;
  final String? asciiArt;
  final String hint;

  @override
  Widget build(BuildContext context) {
    return BaseScreen(
      child: SizedBox.expand(
        child: GestureDetector(
          onTap: onContinue,
          behavior: HitTestBehavior.opaque,
          child: Column(
          children: [
            const Spacer(),
            if (asciiArt != null) ...[
              Text(
                asciiArt!,
                style: const TextStyle(
                  fontFamily: 'monospace',
                  fontSize: 14,
                  height: 1.2,
                  color: AppColors.starYellow,
                ),
              ),
              const SizedBox(height: 20),
            ],
            Text(
              title,
              style: Theme.of(context).textTheme.headlineMedium?.copyWith(
                    color: titleColor,
                  ),
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 30),
            Expanded(
              flex: 2,
              child: SingleChildScrollView(
                child: Text(
                  storyText,
                  style: Theme.of(context).textTheme.bodyLarge?.copyWith(
                        height: 1.6,
                      ),
                  textAlign: TextAlign.center,
                ),
              ),
            ),
            const Spacer(),
            Text(
              hint,
              style: TextStyle(
                color: AppColors.textSecondary,
                fontSize: 14,
              ),
            ),
            const SizedBox(height: 20),
          ],
        ),
        ),
      ),
    );
  }
}
