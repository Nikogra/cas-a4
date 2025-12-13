from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class Observation:
    """
    Information available to a strategy BEFORE choosing a bid.
    """
    N: int                 # number of possible bids (1..N)
    t: int                 # current round (1..rounds)
    self_name: str
    opponent_name: str

    # Full history against this opponent (chronological)
    opp_action_history: Tuple[int, ...]
    self_action_history: Tuple[int, ...]


@dataclass(frozen=True)
class MatchResult:
    """
    Information available to a strategy AFTER a round is played.
    """
    N: int
    t: int
    self_name: str
    opponent_name: str

    # Actions played in this round
    self_action: int
    opp_action: int

    # Payoffs from THIS round only
    self_payoff: int
    opp_payoff: int