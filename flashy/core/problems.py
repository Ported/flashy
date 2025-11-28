"""Problem generation - pure functions for creating math problems."""

import random
from dataclasses import dataclass
from enum import Enum


class Operation(Enum):
    ADD = "+"
    SUBTRACT = "-"
    MULTIPLY = "x"
    DIVIDE = "/"


@dataclass(frozen=True)
class Problem:
    """A math problem with two operands and an operation."""

    operand1: int
    operand2: int
    operation: Operation
    answer: int

    def display(self) -> str:
        """Return the problem as a string for display."""
        return f"{self.operand1} {self.operation.value} {self.operand2}"


def generate_problem(operation: Operation, min_val: int, max_val: int) -> Problem:
    """Generate a random problem for the given operation and number range.

    For subtraction: ensures non-negative result.
    For division: ensures clean integer result (no remainder).
    """
    if operation == Operation.ADD:
        return _generate_addition(min_val, max_val)
    elif operation == Operation.SUBTRACT:
        return _generate_subtraction(min_val, max_val)
    elif operation == Operation.MULTIPLY:
        return _generate_multiplication(min_val, max_val)
    elif operation == Operation.DIVIDE:
        return _generate_division(min_val, max_val)
    else:
        raise ValueError(f"Unknown operation: {operation}")


def _generate_addition(min_val: int, max_val: int) -> Problem:
    a = random.randint(min_val, max_val)
    b = random.randint(min_val, max_val)
    return Problem(operand1=a, operand2=b, operation=Operation.ADD, answer=a + b)


def _generate_subtraction(min_val: int, max_val: int) -> Problem:
    # Generate two numbers and ensure a >= b for non-negative result
    a = random.randint(min_val, max_val)
    b = random.randint(min_val, max_val)
    if a < b:
        a, b = b, a
    return Problem(operand1=a, operand2=b, operation=Operation.SUBTRACT, answer=a - b)


def _generate_multiplication(min_val: int, max_val: int) -> Problem:
    a = random.randint(min_val, max_val)
    b = random.randint(min_val, max_val)
    return Problem(operand1=a, operand2=b, operation=Operation.MULTIPLY, answer=a * b)


def _generate_division(min_val: int, max_val: int) -> Problem:
    # Generate answer and divisor, then compute dividend
    # This ensures clean integer division
    answer = random.randint(min_val, max_val)
    divisor = random.randint(min_val, max_val)
    # Avoid division by zero
    if divisor == 0:
        divisor = 1
    dividend = answer * divisor
    return Problem(
        operand1=dividend, operand2=divisor, operation=Operation.DIVIDE, answer=answer
    )
