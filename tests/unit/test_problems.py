"""Tests for problem generation."""

from flashy.core.problems import Operation, Problem, generate_problem


class TestProblem:
    """Tests for the Problem dataclass."""

    def test_display_addition(self) -> None:
        problem = Problem(3, 5, Operation.ADD, 8)
        assert problem.display() == "3 + 5"

    def test_display_subtraction(self) -> None:
        problem = Problem(10, 4, Operation.SUBTRACT, 6)
        assert problem.display() == "10 - 4"

    def test_display_multiplication(self) -> None:
        problem = Problem(6, 7, Operation.MULTIPLY, 42)
        assert problem.display() == "6 × 7"

    def test_display_division(self) -> None:
        problem = Problem(20, 4, Operation.DIVIDE, 5)
        assert problem.display() == "20 ÷ 4"


class TestGenerateProblem:
    """Tests for problem generation."""

    def test_addition_answer_is_correct(self) -> None:
        for _ in range(100):
            problem = generate_problem(Operation.ADD, 1, 10)
            assert problem.answer == problem.operand1 + problem.operand2

    def test_addition_operands_in_range(self) -> None:
        for _ in range(100):
            problem = generate_problem(Operation.ADD, 5, 15)
            assert 5 <= problem.operand1 <= 15
            assert 5 <= problem.operand2 <= 15

    def test_subtraction_answer_is_correct(self) -> None:
        for _ in range(100):
            problem = generate_problem(Operation.SUBTRACT, 1, 10)
            assert problem.answer == problem.operand1 - problem.operand2

    def test_subtraction_result_non_negative(self) -> None:
        for _ in range(100):
            problem = generate_problem(Operation.SUBTRACT, 1, 10)
            assert problem.answer >= 0
            assert problem.operand1 >= problem.operand2

    def test_multiplication_answer_is_correct(self) -> None:
        for _ in range(100):
            problem = generate_problem(Operation.MULTIPLY, 1, 10)
            assert problem.answer == problem.operand1 * problem.operand2

    def test_multiplication_operands_in_range(self) -> None:
        for _ in range(100):
            problem = generate_problem(Operation.MULTIPLY, 2, 8)
            assert 2 <= problem.operand1 <= 8
            assert 2 <= problem.operand2 <= 8

    def test_division_answer_is_correct(self) -> None:
        for _ in range(100):
            problem = generate_problem(Operation.DIVIDE, 1, 10)
            assert problem.answer == problem.operand1 // problem.operand2

    def test_division_is_clean(self) -> None:
        """Division should have no remainder."""
        for _ in range(100):
            problem = generate_problem(Operation.DIVIDE, 1, 10)
            assert problem.operand1 % problem.operand2 == 0

    def test_division_no_divide_by_zero(self) -> None:
        for _ in range(100):
            problem = generate_problem(Operation.DIVIDE, 0, 10)
            assert problem.operand2 != 0
