import 'package:flutter/material.dart';
import 'package:url_launcher/url_launcher.dart';

import '../theme/app_theme.dart';
import '../widgets/responsive_container.dart';

/// Privacy policy screen.
class PrivacyScreen extends StatelessWidget {
  const PrivacyScreen({super.key});

  Future<void> _launchUrl(String url) async {
    final uri = Uri.parse(url);
    if (await canLaunchUrl(uri)) {
      await launchUrl(uri, mode: LaunchMode.externalApplication);
    }
  }

  @override
  Widget build(BuildContext context) {
    return BaseScreen(
      scrollable: true,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
              // Title
              Center(
                child: Text(
                  'Privacy Policy',
                  style: Theme.of(context).textTheme.headlineMedium?.copyWith(
                        color: AppColors.accentCyan,
                        fontWeight: FontWeight.bold,
                      ),
                ),
              ),
              const SizedBox(height: 10),

              Center(
                child: Text(
                  'Last updated: November 2025',
                  style: TextStyle(
                    fontSize: 14,
                    fontStyle: FontStyle.italic,
                    color: AppColors.textSecondary,
                  ),
                ),
              ),
              const SizedBox(height: 25),

              // What We Collect
              Text(
                'What We Collect',
                style: Theme.of(context).textTheme.titleLarge?.copyWith(
                      color: AppColors.starYellow,
                    ),
              ),
              const SizedBox(height: 10),
              const Text(
                "Flashy collects only your chosen player name for the leaderboard. That's it.",
                style: TextStyle(fontSize: 16),
              ),
              const SizedBox(height: 10),
              Padding(
                padding: const EdgeInsets.only(left: 20),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: const [
                    Text('• No email addresses',
                        style: TextStyle(fontSize: 16)),
                    Text('• No personal information',
                        style: TextStyle(fontSize: 16)),
                    Text('• No tracking or analytics',
                        style: TextStyle(fontSize: 16)),
                    Text('• No cookies', style: TextStyle(fontSize: 16)),
                  ],
                ),
              ),
              const SizedBox(height: 25),

              // Local Storage
              Text(
                'Local Storage',
                style: Theme.of(context).textTheme.titleLarge?.copyWith(
                      color: AppColors.starYellow,
                    ),
              ),
              const SizedBox(height: 10),
              const Text(
                'Your game progress is stored locally on your device using secure storage.',
                style: TextStyle(fontSize: 16),
              ),
              const SizedBox(height: 25),

              // Leaderboard
              Text(
                'Leaderboard',
                style: Theme.of(context).textTheme.titleLarge?.copyWith(
                      color: AppColors.starYellow,
                    ),
              ),
              const SizedBox(height: 10),
              const Text(
                'When you create a player, your chosen name and score are stored on our server and displayed on the public leaderboard. No other data is collected.',
                style: TextStyle(fontSize: 16),
              ),
              const SizedBox(height: 25),

              // No Commercial Use
              Text(
                'No Commercial Use',
                style: Theme.of(context).textTheme.titleLarge?.copyWith(
                      color: AppColors.starYellow,
                    ),
              ),
              const SizedBox(height: 10),
              const Text(
                "Flashy is a non-commercial, open-source educational project. We don't sell data, show ads, or have any commercial objectives.",
                style: TextStyle(fontSize: 16),
              ),
              const SizedBox(height: 25),

              // No Warranty
              Text(
                'No Warranty',
                style: Theme.of(context).textTheme.titleLarge?.copyWith(
                      color: AppColors.starYellow,
                    ),
              ),
              const SizedBox(height: 10),
              Wrap(
                children: [
                  const Text(
                    'This software is provided "as is", without warranty of any kind. See the ',
                    style: TextStyle(fontSize: 16),
                  ),
                  GestureDetector(
                    onTap: () => _launchUrl(
                        'https://github.com/Ported/flashy/blob/main/LICENSE'),
                    child: Text(
                      'MIT License',
                      style: TextStyle(
                        fontSize: 16,
                        color: AppColors.accentCyan,
                        decoration: TextDecoration.underline,
                      ),
                    ),
                  ),
                  const Text(
                    ' for full terms.',
                    style: TextStyle(fontSize: 16),
                  ),
                ],
              ),
              const SizedBox(height: 25),

              // Contact
              Text(
                'Contact',
                style: Theme.of(context).textTheme.titleLarge?.copyWith(
                      color: AppColors.starYellow,
                    ),
              ),
              const SizedBox(height: 10),
              Wrap(
                children: [
                  const Text(
                    'Questions? Open an issue on ',
                    style: TextStyle(fontSize: 16),
                  ),
                  GestureDetector(
                    onTap: () =>
                        _launchUrl('https://github.com/Ported/flashy/issues'),
                    child: Text(
                      'GitHub',
                      style: TextStyle(
                        fontSize: 16,
                        color: AppColors.accentCyan,
                        decoration: TextDecoration.underline,
                      ),
                    ),
                  ),
                  const Text(
                    '.',
                    style: TextStyle(fontSize: 16),
                  ),
                ],
              ),
              const SizedBox(height: 30),

              // Back button
              Center(
                child: ElevatedButton(
                  onPressed: () => Navigator.of(context).pop(),
                  child: const Text('Back'),
                ),
              ),
            ],
          ),
    );
  }
}
