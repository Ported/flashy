import 'package:flutter/material.dart';
import 'package:flutter_svg/flutter_svg.dart';
import 'package:provider/provider.dart';

import '../l10n/app_localizations.dart';
import '../main.dart';
import '../theme/app_theme.dart';
import '../widgets/animated_button.dart';
import '../widgets/responsive_container.dart';
import 'about_screen.dart';
import 'player_select_screen.dart';
import 'privacy_screen.dart';

/// Welcome/Title screen with game logo and Play button.
class WelcomeScreen extends StatelessWidget {
  const WelcomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final localeState = context.watch<LocaleState>();
    final l10n = AppLocalizations.of(context)!;
    final isEnglish = localeState.locale.languageCode == 'en';

    return BaseScreen(
      child: Column(
            children: [
              // Language toggle (top right)
              Row(
                mainAxisAlignment: MainAxisAlignment.end,
                children: [
                  _LanguageButton(
                    label: 'EN',
                    isActive: isEnglish,
                    onTap: () {
                      localeState.setLocale(const Locale('en'));
                    },
                  ),
                  const SizedBox(width: 5),
                  _LanguageButton(
                    label: 'SV',
                    isActive: !isEnglish,
                    onTap: () {
                      localeState.setLocale(const Locale('sv'));
                    },
                  ),
                ],
              ),

              const Spacer(),

              // Flashy logo
              SvgPicture.asset(
                'assets/flashy-icon.svg',
                width: 180,
                height: 180,
              ),

              const SizedBox(height: 20),

              // Title
              Text(
                l10n.appTitle,
                style: Theme.of(context).textTheme.headlineLarge,
                textAlign: TextAlign.center,
              ),

              const SizedBox(height: 10),

              // Tagline
              Text(
                l10n.appTagline,
                style: Theme.of(context).textTheme.bodyLarge?.copyWith(
                      color: AppColors.textSecondary,
                    ),
                textAlign: TextAlign.center,
              ),

              const SizedBox(height: 40),

              // Play button
              AnimatedElevatedButton(
                onPressed: () {
                  Navigator.of(context).push(
                    MaterialPageRoute(
                      builder: (_) => const PlayerSelectScreen(),
                    ),
                  );
                },
                style: ElevatedButton.styleFrom(
                  padding:
                      const EdgeInsets.symmetric(horizontal: 40, vertical: 15),
                  textStyle: const TextStyle(
                    fontSize: 20,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                child: Text(l10n.navPlay),
              ),

              const Spacer(),

              // Footer links
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  AnimatedTextButton(
                    onPressed: () {
                      Navigator.of(context).push(
                        MaterialPageRoute(
                          builder: (_) => const AboutScreen(),
                        ),
                      );
                    },
                    child: Text(
                      l10n.navAbout,
                      style: const TextStyle(color: AppColors.textSecondary),
                    ),
                  ),
                  const Text(
                    '|',
                    style: TextStyle(color: AppColors.textSecondary),
                  ),
                  AnimatedTextButton(
                    onPressed: () {
                      Navigator.of(context).push(
                        MaterialPageRoute(
                          builder: (_) => const PrivacyScreen(),
                        ),
                      );
                    },
                    child: Text(
                      l10n.navPrivacy,
                      style: const TextStyle(color: AppColors.textSecondary),
                    ),
                  ),
                ],
              ),
            ],
          ),
    );
  }
}

/// Language toggle button.
class _LanguageButton extends StatelessWidget {
  const _LanguageButton({
    required this.label,
    required this.isActive,
    required this.onTap,
  });

  final String label;
  final bool isActive;
  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onTap,
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 5),
        decoration: BoxDecoration(
          color: isActive ? AppColors.accentCyan : AppColors.darkBackground,
          border: Border.all(color: AppColors.accentCyan, width: 2),
          borderRadius: BorderRadius.circular(4),
        ),
        child: Text(
          label,
          style: TextStyle(
            fontSize: 14,
            fontWeight: isActive ? FontWeight.bold : FontWeight.normal,
            color: isActive ? AppColors.darkBackground : AppColors.textSecondary,
          ),
        ),
      ),
    );
  }
}
