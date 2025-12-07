import 'package:flutter_test/flutter_test.dart';
import 'package:flashy_app/core/problems.dart';

void main() {
  group('Problem', () {
    test('display addition', () {
      const problem = Problem(
        operand1: 3,
        operand2: 5,
        operation: Operation.add,
        answer: 8,
      );
      expect(problem.display(), equals('3 + 5'));
    });

    test('display subtraction', () {
      const problem = Problem(
        operand1: 10,
        operand2: 4,
        operation: Operation.subtract,
        answer: 6,
      );
      expect(problem.display(), equals('10 - 4'));
    });

    test('display multiplication', () {
      const problem = Problem(
        operand1: 6,
        operand2: 7,
        operation: Operation.multiply,
        answer: 42,
      );
      expect(problem.display(), equals('6 × 7'));
    });

    test('display division', () {
      const problem = Problem(
        operand1: 20,
        operand2: 4,
        operation: Operation.divide,
        answer: 5,
      );
      expect(problem.display(), equals('20 ÷ 4'));
    });

    test('display negative operand in parentheses', () {
      const problem = Problem(
        operand1: -1,
        operand2: -8,
        operation: Operation.subtract,
        answer: 7,
      );
      expect(problem.display(), equals('-1 - (-8)'));
    });
  });

  group('generateProblem', () {
    test('addition answer is correct', () {
      for (var i = 0; i < 100; i++) {
        final problem = generateProblem(Operation.add, 1, 10);
        expect(problem.answer, equals(problem.operand1 + problem.operand2));
      }
    });

    test('addition operands in range', () {
      for (var i = 0; i < 100; i++) {
        final problem = generateProblem(Operation.add, 5, 15);
        expect(problem.operand1, inInclusiveRange(5, 15));
        expect(problem.operand2, inInclusiveRange(5, 15));
      }
    });

    test('subtraction answer is correct', () {
      for (var i = 0; i < 100; i++) {
        final problem = generateProblem(Operation.subtract, 1, 10);
        expect(problem.answer, equals(problem.operand1 - problem.operand2));
      }
    });

    test('subtraction result non-negative', () {
      for (var i = 0; i < 100; i++) {
        final problem = generateProblem(Operation.subtract, 1, 10);
        expect(problem.answer, greaterThanOrEqualTo(0));
        expect(problem.operand1, greaterThanOrEqualTo(problem.operand2));
      }
    });

    test('multiplication answer is correct', () {
      for (var i = 0; i < 100; i++) {
        final problem = generateProblem(Operation.multiply, 1, 10);
        expect(problem.answer, equals(problem.operand1 * problem.operand2));
      }
    });

    test('multiplication operands in range', () {
      for (var i = 0; i < 100; i++) {
        final problem = generateProblem(Operation.multiply, 2, 8);
        expect(problem.operand1, inInclusiveRange(2, 8));
        expect(problem.operand2, inInclusiveRange(2, 8));
      }
    });

    test('division answer is correct', () {
      for (var i = 0; i < 100; i++) {
        final problem = generateProblem(Operation.divide, 1, 10);
        expect(problem.answer, equals(problem.operand1 ~/ problem.operand2));
      }
    });

    test('division is clean (no remainder)', () {
      for (var i = 0; i < 100; i++) {
        final problem = generateProblem(Operation.divide, 1, 10);
        expect(problem.operand1 % problem.operand2, equals(0));
      }
    });

    test('division no divide by zero', () {
      for (var i = 0; i < 100; i++) {
        final problem = generateProblem(Operation.divide, 0, 10);
        expect(problem.operand2, isNot(equals(0)));
      }
    });
  });

  group('Operation', () {
    test('add symbol', () {
      expect(Operation.add.symbol, equals('+'));
    });

    test('subtract symbol', () {
      expect(Operation.subtract.symbol, equals('-'));
    });

    test('multiply symbol', () {
      expect(Operation.multiply.symbol, equals('×'));
    });

    test('divide symbol', () {
      expect(Operation.divide.symbol, equals('÷'));
    });
  });
}
