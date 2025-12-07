import 'package:flutter/material.dart';

/// A button wrapper that adds scale animation on hover and press.
/// Wraps any child widget (typically an ElevatedButton, OutlinedButton, etc.)
class _AnimatedButtonWrapper extends StatefulWidget {
  const _AnimatedButtonWrapper({
    required this.child,
    this.scaleOnHover = 1.05,
    this.scaleOnPress = 0.95,
  });

  final Widget child;
  final double scaleOnHover;
  final double scaleOnPress;
  static const Duration _duration = Duration(milliseconds: 100);

  @override
  State<_AnimatedButtonWrapper> createState() => _AnimatedButtonWrapperState();
}

class _AnimatedButtonWrapperState extends State<_AnimatedButtonWrapper> {
  bool _isHovered = false;
  bool _isPressed = false;

  double get _scale {
    if (_isPressed) return widget.scaleOnPress;
    if (_isHovered) return widget.scaleOnHover;
    return 1.0;
  }

  @override
  Widget build(BuildContext context) {
    return MouseRegion(
      onEnter: (_) => setState(() => _isHovered = true),
      onExit: (_) => setState(() {
        _isHovered = false;
        _isPressed = false;
      }),
      child: Listener(
        onPointerDown: (_) => setState(() => _isPressed = true),
        onPointerUp: (_) => setState(() => _isPressed = false),
        onPointerCancel: (_) => setState(() => _isPressed = false),
        child: AnimatedScale(
          scale: _scale,
          duration: _AnimatedButtonWrapper._duration,
          curve: Curves.easeOut,
          child: widget.child,
        ),
      ),
    );
  }
}

/// ElevatedButton with scale animation on hover/press.
class AnimatedElevatedButton extends StatelessWidget {
  const AnimatedElevatedButton({
    super.key,
    required this.onPressed,
    required this.child,
    this.style,
  });

  final VoidCallback? onPressed;
  final Widget child;
  final ButtonStyle? style;

  @override
  Widget build(BuildContext context) {
    return _AnimatedButtonWrapper(
      child: ElevatedButton(
        onPressed: onPressed,
        style: style,
        child: child,
      ),
    );
  }
}

/// TextButton with scale animation on hover/press.
class AnimatedTextButton extends StatelessWidget {
  const AnimatedTextButton({
    super.key,
    required this.onPressed,
    required this.child,
    this.style,
  });

  final VoidCallback? onPressed;
  final Widget child;
  final ButtonStyle? style;

  @override
  Widget build(BuildContext context) {
    return _AnimatedButtonWrapper(
      scaleOnHover: 1.03,
      scaleOnPress: 0.97,
      child: TextButton(
        onPressed: onPressed,
        style: style,
        child: child,
      ),
    );
  }
}
