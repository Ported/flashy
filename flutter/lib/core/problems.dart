// Problem generation - pure functions for creating math problems.
import 'dart:math';

/// Mathematical operations supported by the game.
enum Operation {
  add('+'),
  subtract('-'),
  multiply('×'),
  divide('÷');

  const Operation(this.symbol);

  /// The symbol used to display this operation.
  final String symbol;
}

/// A math problem with two operands and an operation.
///
/// This class is immutable - all fields are final.
class Problem {
  const Problem({
    required this.operand1,
    required this.operand2,
    required this.operation,
    required this.answer,
  });

  final int operand1;
  final int operand2;
  final Operation operation;
  final int answer;

  /// Return the problem as a string for display.
  ///
  /// Wraps negative second operand in parentheses for clarity.
  /// e.g., "-1 - (-8)" instead of "-1 - -8"
  String display() {
    final op2 = operand2 < 0 ? '($operand2)' : '$operand2';
    return '$operand1 ${operation.symbol} $op2';
  }

  @override
  bool operator ==(Object other) =>
      identical(this, other) ||
      other is Problem &&
          runtimeType == other.runtimeType &&
          operand1 == other.operand1 &&
          operand2 == other.operand2 &&
          operation == other.operation &&
          answer == other.answer;

  @override
  int get hashCode => Object.hash(operand1, operand2, operation, answer);
}

/// Generate a random problem for the given operation and number range.
///
/// For subtraction: ensures non-negative result.
/// For division: ensures clean integer result (no remainder).
Problem generateProblem(
  Operation operation,
  int minVal,
  int maxVal, {
  Random? random,
}) {
  final rng = random ?? Random();

  switch (operation) {
    case Operation.add:
      return _generateAddition(minVal, maxVal, rng);
    case Operation.subtract:
      return _generateSubtraction(minVal, maxVal, rng);
    case Operation.multiply:
      return _generateMultiplication(minVal, maxVal, rng);
    case Operation.divide:
      return _generateDivision(minVal, maxVal, rng);
  }
}

int _randomInRange(int min, int max, Random rng) {
  return min + rng.nextInt(max - min + 1);
}

Problem _generateAddition(int minVal, int maxVal, Random rng) {
  final a = _randomInRange(minVal, maxVal, rng);
  final b = _randomInRange(minVal, maxVal, rng);
  return Problem(
    operand1: a,
    operand2: b,
    operation: Operation.add,
    answer: a + b,
  );
}

Problem _generateSubtraction(int minVal, int maxVal, Random rng) {
  // Generate two numbers and ensure a >= b for non-negative result
  var a = _randomInRange(minVal, maxVal, rng);
  var b = _randomInRange(minVal, maxVal, rng);
  if (a < b) {
    final temp = a;
    a = b;
    b = temp;
  }
  return Problem(
    operand1: a,
    operand2: b,
    operation: Operation.subtract,
    answer: a - b,
  );
}

Problem _generateMultiplication(int minVal, int maxVal, Random rng) {
  final a = _randomInRange(minVal, maxVal, rng);
  final b = _randomInRange(minVal, maxVal, rng);
  return Problem(
    operand1: a,
    operand2: b,
    operation: Operation.multiply,
    answer: a * b,
  );
}

Problem _generateDivision(int minVal, int maxVal, Random rng) {
  // Generate answer and divisor, then compute dividend
  // This ensures clean integer division
  final answer = _randomInRange(minVal, maxVal, rng);
  var divisor = _randomInRange(minVal, maxVal, rng);
  // Avoid division by zero
  if (divisor == 0) {
    divisor = 1;
  }
  final dividend = answer * divisor;
  return Problem(
    operand1: dividend,
    operand2: divisor,
    operation: Operation.divide,
    answer: answer,
  );
}
