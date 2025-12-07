import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

/// App color palette - matching web CSS.
class AppColors {
  AppColors._();

  static const darkBackground = Color(0xFF1a1a2e);
  static const cardBackground = Color(0xFF16213e);
  static const accentCyan = Color(0xFF00FFFF);
  static const correctGreen = Color(0xFF00FF00);
  static const incorrectRed = Color(0xFFFF0000);
  static const starYellow = Color(0xFFFFFF00);
  static const textPrimary = Color(0xFFEEEEEE);
  static const textSecondary = Color(0xFF888888);
  static const dangerRed = Color(0xFFFF6666);
}

/// App theme configuration.
class AppTheme {
  AppTheme._();

  static ThemeData get darkTheme {
    // Base text theme with Fredoka font
    final baseTextTheme = GoogleFonts.fredokaTextTheme(
      ThemeData.dark().textTheme,
    );

    return ThemeData(
      useMaterial3: true,
      brightness: Brightness.dark,
      scaffoldBackgroundColor: AppColors.darkBackground,
      fontFamily: GoogleFonts.fredoka().fontFamily,
      colorScheme: const ColorScheme.dark(
        primary: AppColors.accentCyan,
        secondary: AppColors.accentCyan,
        surface: AppColors.cardBackground,
        error: AppColors.dangerRed,
      ),
      appBarTheme: const AppBarTheme(
        backgroundColor: AppColors.darkBackground,
        foregroundColor: AppColors.accentCyan,
        elevation: 0,
      ),
      cardTheme: CardThemeData(
        color: AppColors.cardBackground,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(10),
          side: const BorderSide(color: AppColors.accentCyan, width: 2),
        ),
      ),
      elevatedButtonTheme: ElevatedButtonThemeData(
        style: ButtonStyle(
          backgroundColor: WidgetStateProperty.resolveWith((states) {
            if (states.contains(WidgetState.pressed)) {
              return AppColors.accentCyan.withValues(alpha: 0.8);
            }
            if (states.contains(WidgetState.hovered)) {
              return AppColors.accentCyan;
            }
            return AppColors.accentCyan;
          }),
          foregroundColor: WidgetStateProperty.all(AppColors.darkBackground),
          padding: WidgetStateProperty.all(
            const EdgeInsets.symmetric(horizontal: 24, vertical: 12),
          ),
          shape: WidgetStateProperty.all(
            RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(8),
            ),
          ),
          textStyle: WidgetStateProperty.all(
            GoogleFonts.fredoka(
              fontSize: 16,
              fontWeight: FontWeight.w500,
            ),
          ),
          elevation: WidgetStateProperty.resolveWith((states) {
            if (states.contains(WidgetState.pressed)) {
              return 1;
            }
            if (states.contains(WidgetState.hovered)) {
              return 8;
            }
            return 4;
          }),
          shadowColor: WidgetStateProperty.all(
            AppColors.accentCyan.withValues(alpha: 0.5),
          ),
          overlayColor: WidgetStateProperty.resolveWith((states) {
            if (states.contains(WidgetState.pressed)) {
              return Colors.white.withValues(alpha: 0.2);
            }
            if (states.contains(WidgetState.hovered)) {
              return Colors.white.withValues(alpha: 0.1);
            }
            return null;
          }),
          animationDuration: const Duration(milliseconds: 100),
        ),
      ),
      outlinedButtonTheme: OutlinedButtonThemeData(
        style: ButtonStyle(
          foregroundColor: WidgetStateProperty.resolveWith((states) {
            if (states.contains(WidgetState.pressed)) {
              return AppColors.accentCyan.withValues(alpha: 0.8);
            }
            return AppColors.accentCyan;
          }),
          side: WidgetStateProperty.resolveWith((states) {
            if (states.contains(WidgetState.hovered)) {
              return const BorderSide(color: AppColors.accentCyan, width: 3);
            }
            return const BorderSide(color: AppColors.accentCyan, width: 2);
          }),
          padding: WidgetStateProperty.all(
            const EdgeInsets.symmetric(horizontal: 24, vertical: 12),
          ),
          shape: WidgetStateProperty.all(
            RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(8),
            ),
          ),
          textStyle: WidgetStateProperty.all(
            GoogleFonts.fredoka(
              fontSize: 16,
              fontWeight: FontWeight.w500,
            ),
          ),
          overlayColor: WidgetStateProperty.resolveWith((states) {
            if (states.contains(WidgetState.pressed)) {
              return AppColors.accentCyan.withValues(alpha: 0.2);
            }
            if (states.contains(WidgetState.hovered)) {
              return AppColors.accentCyan.withValues(alpha: 0.1);
            }
            return null;
          }),
          animationDuration: const Duration(milliseconds: 100),
        ),
      ),
      textButtonTheme: TextButtonThemeData(
        style: ButtonStyle(
          foregroundColor: WidgetStateProperty.resolveWith((states) {
            if (states.contains(WidgetState.pressed)) {
              return AppColors.accentCyan.withValues(alpha: 0.7);
            }
            if (states.contains(WidgetState.hovered)) {
              return AppColors.accentCyan;
            }
            return AppColors.textSecondary;
          }),
          padding: WidgetStateProperty.all(
            const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
          ),
          textStyle: WidgetStateProperty.all(
            GoogleFonts.fredoka(
              fontSize: 18,
              fontWeight: FontWeight.w400,
            ),
          ),
          overlayColor: WidgetStateProperty.resolveWith((states) {
            if (states.contains(WidgetState.pressed)) {
              return AppColors.accentCyan.withValues(alpha: 0.15);
            }
            if (states.contains(WidgetState.hovered)) {
              return AppColors.accentCyan.withValues(alpha: 0.08);
            }
            return null;
          }),
          animationDuration: const Duration(milliseconds: 100),
        ),
      ),
      inputDecorationTheme: InputDecorationTheme(
        filled: true,
        fillColor: AppColors.darkBackground,
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(5),
          borderSide: const BorderSide(color: AppColors.accentCyan, width: 2),
        ),
        enabledBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(5),
          borderSide: const BorderSide(color: AppColors.accentCyan, width: 2),
        ),
        focusedBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(5),
          borderSide: const BorderSide(color: AppColors.accentCyan, width: 2),
        ),
        labelStyle: const TextStyle(color: AppColors.textSecondary),
        hintStyle: const TextStyle(color: AppColors.textSecondary),
      ),
      textTheme: baseTextTheme.copyWith(
        headlineLarge: baseTextTheme.headlineLarge?.copyWith(
          color: AppColors.accentCyan,
          fontSize: 32,
          fontWeight: FontWeight.bold,
        ),
        headlineMedium: baseTextTheme.headlineMedium?.copyWith(
          color: AppColors.accentCyan,
          fontSize: 24,
          fontWeight: FontWeight.bold,
        ),
        headlineSmall: baseTextTheme.headlineSmall?.copyWith(
          color: AppColors.accentCyan,
          fontSize: 20,
          fontWeight: FontWeight.bold,
        ),
        bodyLarge: baseTextTheme.bodyLarge?.copyWith(
          color: AppColors.textPrimary,
          fontSize: 16,
        ),
        bodyMedium: baseTextTheme.bodyMedium?.copyWith(
          color: AppColors.textPrimary,
          fontSize: 14,
        ),
        bodySmall: baseTextTheme.bodySmall?.copyWith(
          color: AppColors.textSecondary,
          fontSize: 12,
        ),
      ),
    );
  }
}
