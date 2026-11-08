import re
from collections.abc import Callable, Iterator


def generator_numbers(text: str) -> Iterator[float]:
    """Yield floating-point numbers found in the text."""

    # Match signed numbers separated by spaces or string boundaries.
    pattern = r"(?:^|(?<= ))[+-]?(?:\d+(?:\.\d+)?|\.\d+)(?= |$)"

    for match in re.finditer(pattern, text):
        yield float(match.group())


def sum_profit(text: str, func: Callable[[str], Iterator[float]]) -> float:
    """Calculate the sum of numbers yielded by the given function."""
    return sum(func(text))
