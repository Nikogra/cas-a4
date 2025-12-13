from __future__ import annotations

from typing import Protocol

from .types import MatchResult, Observation


class Strategy(Protocol):
    """
    Every strategy MUST follow this interface.

    You do NOT need to inherit from this class.
    If your class has the same methods, it is a valid Strategy (duck typing).

    Required attributes / methods:
    - name: str
    - reset(N)
    - act(obs) -> int
    - on_result(result)
    """

    # Human-readable strategy name (used for printing)
    name: str

    def reset(self, *, N: int) -> None:
        """
        Called ONCE before the match starts.

        Parameters:
        - N: number of possible bids (actions are 1..N)

        Use this to:
        - initialize internal state
        - reset memory / learning variables
        """
        ...

    def act(self, obs: Observation) -> int:
        """
        Called EVERY round to choose a bid.

        Must return an integer in {1, 2, ..., N}.
        """
        ...

    def on_result(self, result: MatchResult) -> None:
        """
        Called AFTER each round.

        Use this to:
        - update memory
        - update learning statistics
        """
        ...
