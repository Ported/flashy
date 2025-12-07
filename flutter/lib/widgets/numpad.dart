import 'package:flutter/material.dart';

import '../theme/app_theme.dart';

/// Numpad widget for answer input.
class Numpad extends StatelessWidget {
  const Numpad({
    super.key,
    required this.onDigit,
    required this.onBackspace,
    required this.onEnter,
  });

  final void Function(String digit) onDigit;
  final VoidCallback onBackspace;
  final VoidCallback onEnter;

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            _NumpadButton(label: '1', onTap: () => onDigit('1')),
            _NumpadButton(label: '2', onTap: () => onDigit('2')),
            _NumpadButton(label: '3', onTap: () => onDigit('3')),
          ],
        ),
        const SizedBox(height: 8),
        Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            _NumpadButton(label: '4', onTap: () => onDigit('4')),
            _NumpadButton(label: '5', onTap: () => onDigit('5')),
            _NumpadButton(label: '6', onTap: () => onDigit('6')),
          ],
        ),
        const SizedBox(height: 8),
        Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            _NumpadButton(label: '7', onTap: () => onDigit('7')),
            _NumpadButton(label: '8', onTap: () => onDigit('8')),
            _NumpadButton(label: '9', onTap: () => onDigit('9')),
          ],
        ),
        const SizedBox(height: 8),
        Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            _NumpadButton(label: '-', onTap: () => onDigit('-')),
            _NumpadButton(label: '0', onTap: () => onDigit('0')),
            _NumpadButton(label: '⌫', onTap: onBackspace),
          ],
        ),
      ],
    );
  }
}

/// Individual numpad button.
class _NumpadButton extends StatelessWidget {
  const _NumpadButton({required this.label, required this.onTap});

  final String label;
  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 4),
      child: Material(
        color: AppColors.darkBackground,
        borderRadius: BorderRadius.circular(8),
        child: InkWell(
          onTap: onTap,
          borderRadius: BorderRadius.circular(8),
          child: Container(
            width: 75,
            height: 58,
            decoration: BoxDecoration(
              border: Border.all(color: AppColors.accentCyan, width: 2),
              borderRadius: BorderRadius.circular(8),
            ),
            child: Center(
              child: Text(
                label,
                style: const TextStyle(
                  fontSize: 26,
                  fontWeight: FontWeight.bold,
                  color: Colors.white,
                ),
              ),
            ),
          ),
        ),
      ),
    );
  }
}
