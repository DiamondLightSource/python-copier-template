"""Example code to show complete use case."""


def add(x, y):
    """Adding two numbers.

    Args:
        x (float): first number
        y (float): second number

    Returns:
       the sum of the two numbers

    Raises:
        ValueError: when x is negative
    """
    if x < 0:
        raise ValueError("x must be positive")
    return x + y
