import 'package:flutter/material.dart';
import 'package:url_launcher/url_launcher.dart';

import '../theme/app_theme.dart';
import '../widgets/responsive_container.dart';

/// About screen with information about the game.
class AboutScreen extends StatelessWidget {
  const AboutScreen({super.key});

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
                  'About Flashy',
                  style: Theme.of(context).textTheme.headlineMedium?.copyWith(
                        color: AppColors.accentCyan,
                        fontWeight: FontWeight.bold,
                      ),
                ),
              ),
              const SizedBox(height: 20),

              // Description
              const Text(
                'Flashy is a free, open-source math game designed to help kids practice arithmetic in a fun, engaging way.',
                style: TextStyle(fontSize: 16),
              ),
              const SizedBox(height: 15),

              const Text(
                'Players guide Flashy the dog through 4 worlds, each focusing on a different operation:',
                style: TextStyle(fontSize: 16),
              ),
              const SizedBox(height: 10),

              // World list
              Padding(
                padding: const EdgeInsets.only(left: 20),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: const [
                    Text('• Addition Alps', style: TextStyle(fontSize: 16)),
                    Text('• Subtraction Swamp', style: TextStyle(fontSize: 16)),
                    Text('• Multiplication Meadows',
                        style: TextStyle(fontSize: 16)),
                    Text('• Division Desert', style: TextStyle(fontSize: 16)),
                  ],
                ),
              ),
              const SizedBox(height: 15),

              const Text(
                'The game features 40 levels of increasing difficulty, friendly characters to meet, and boss battles to conquer!',
                style: TextStyle(fontSize: 16),
              ),
              const SizedBox(height: 25),

              // Open Source section
              Text(
                'Open Source',
                style: Theme.of(context).textTheme.titleLarge?.copyWith(
                      color: AppColors.starYellow,
                    ),
              ),
              const SizedBox(height: 10),
              const Text(
                'Flashy is released under the MIT License. The source code is available on GitHub:',
                style: TextStyle(fontSize: 16),
              ),
              const SizedBox(height: 8),
              GestureDetector(
                onTap: () => _launchUrl('https://github.com/Ported/flashy'),
                child: Text(
                  'github.com/Ported/flashy',
                  style: TextStyle(
                    fontSize: 16,
                    color: AppColors.accentCyan,
                    decoration: TextDecoration.underline,
                  ),
                ),
              ),
              const SizedBox(height: 10),
              const Text(
                'Contributions, bug reports, and feedback are welcome!',
                style: TextStyle(fontSize: 16),
              ),
              const SizedBox(height: 25),

              // Technology section
              Text(
                'Technology',
                style: Theme.of(context).textTheme.titleLarge?.copyWith(
                      color: AppColors.starYellow,
                    ),
              ),
              const SizedBox(height: 10),
              const Text(
                'Built with Flutter for cross-platform support. The original web version was built with Python and Pyodide.',
                style: TextStyle(fontSize: 16),
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
