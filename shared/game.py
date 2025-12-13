from __future__ import annotations

from typing import Tuple


def payoff(i: int, j: int) -> Tuple[int, int]:
    """
    Game payoff rules:

    - if i < j: player i wins and gets payoff = i
    - if i = j: tie -> (0, 0)
    - if i > j: player j wins and gets payoff = j
    """
    if i < j:
        return (i, 0)
    if i == j:
        return (0, 0)
    return (0, j)


def validate_action(a: int, N: int) -> None:
    """
    Safety check to ensure strategies return valid bids.
    """
    if not isinstance(a, int):
        raise TypeError(f"Action must be int, got {type(a)}")
    if a < 1 or a > N:
        raise ValueError(f"Action {a} out of bounds (1..{N})")
