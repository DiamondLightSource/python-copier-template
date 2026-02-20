"""Example code to show complete use case."""


def add(x: float, y: float) -> float:
    """Adding two numbers.

    Args:
        x: first number
        y: second number

    Returns:
       The sum of the two numbers

    Raises:
        ValueError: when x is negative
    """
    if x < 0:
        raise ValueError("x must be positive")
    return x + y
