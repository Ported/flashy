import 'package:flutter/material.dart';

import '../theme/app_theme.dart';

/// Global configuration for BaseScreen styling.
/// Modify these values to change the look across ALL screens consistently.
class BaseScreenConfig {
  BaseScreenConfig._();

  /// Maximum width of content area.
  static const double maxWidth = 600;

  /// Margin outside the border (space between screen edge and border).
  static const EdgeInsets margin = EdgeInsets.all(12);

  /// Padding inside the border (space between border and content).
  /// This is fixed for ALL screens to ensure consistent border appearance.
  static const EdgeInsets padding = EdgeInsets.all(16);

  /// Border color.
  static Color get borderColor => AppColors.accentCyan;

  /// Border width.
  static const double borderWidth = 2;

  /// Border radius.
  static const double borderRadius = 8;
}

/// Base screen widget that provides consistent layout across the app.
///
/// Features:
/// - Constrains content to max width (centered on wide screens)
/// - Adds consistent border, margin, and padding (same on ALL screens)
/// - Includes SafeArea
/// - Optional scrolling for long content
///
/// IMPORTANT: Padding is intentionally NOT configurable per-screen.
/// This ensures all screens have identical border appearance.
/// If you need different internal spacing, add it inside your content.
///
/// Use this as the root widget for all screens.
class BaseScreen extends StatelessWidget {
  const BaseScreen({
    super.key,
    required this.child,
    this.showBorder = true,
    this.scrollable = false,
  });

  /// The content to display.
  final Widget child;

  /// Whether to show a border around the container.
  final bool showBorder;

  /// Whether content should be scrollable.
  final bool scrollable;

  @override
  Widget build(BuildContext context) {
    Widget content = Padding(
      padding: BaseScreenConfig.padding,
      child: child,
    );

    if (scrollable) {
      content = SingleChildScrollView(child: content);
    }

    if (showBorder) {
      content = Container(
        margin: BaseScreenConfig.margin,
        decoration: BoxDecoration(
          border: Border.all(
            color: BaseScreenConfig.borderColor,
            width: BaseScreenConfig.borderWidth,
          ),
          borderRadius: BorderRadius.circular(BaseScreenConfig.borderRadius),
        ),
        child: content,
      );
    }

    return Scaffold(
      body: SafeArea(
        child: Center(
          child: ConstrainedBox(
            constraints: const BoxConstraints(maxWidth: BaseScreenConfig.maxWidth),
            child: content,
          ),
        ),
      ),
    );
  }
}

/// A container that constrains content width and centers it on wide screens.
///
/// Use this when you need responsive layout inside an existing Scaffold.
/// For most screens, prefer using BaseScreen instead.
///
/// NOTE: This is mainly kept for backwards compatibility.
/// New screens should use BaseScreen directly.
class ResponsiveContainer extends StatelessWidget {
  const ResponsiveContainer({
    super.key,
    required this.child,
    this.showBorder = true,
  });

  /// The content to display.
  final Widget child;

  /// Whether to show a border around the container.
  final bool showBorder;

  @override
  Widget build(BuildContext context) {
    Widget content = Padding(
      padding: BaseScreenConfig.padding,
      child: child,
    );

    if (showBorder) {
      content = Container(
        margin: BaseScreenConfig.margin,
        decoration: BoxDecoration(
          border: Border.all(
            color: BaseScreenConfig.borderColor,
            width: BaseScreenConfig.borderWidth,
          ),
          borderRadius: BorderRadius.circular(BaseScreenConfig.borderRadius),
        ),
        child: content,
      );
    }

    return Center(
      child: ConstrainedBox(
        constraints: const BoxConstraints(maxWidth: BaseScreenConfig.maxWidth),
        child: content,
      ),
    );
  }
}
