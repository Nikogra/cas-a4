from __future__ import annotations

import random
from collections import deque
from dataclasses import dataclass
from typing import Deque

from shared.types import MatchResult, Observation


@dataclass
class _Mem:
    state: str
    last3: Deque[int]

# G2 Strategy:
# Uses the last 3 opponent bids to switch between two modes.
# Normally bids low (1–3) probabilistically, but switches to always bidding 1
# if the opponent repeatedly bids low.
class G2:
    name = "G2"

    def __init__(self) -> None:
        self.N = 0
        self.mem: _Mem | None = None

    def reset(self, *, N: int) -> None:
        self.N = N
        self.mem = _Mem(state="ZH", last3=deque(maxlen=3))

    def act(self, obs: Observation) -> int:
        assert self.mem is not None

        if self.mem.state == "ZD":
            return 1

        # sample from {1,2,3} with probs {0.15,0.50,0.35}
        x = random.random()
        if x < 0.15:
            a = 1
        elif x < 0.65:
            a = 2
        else:
            a = 3
        return min(a, obs.N)

    def on_result(self, result: MatchResult) -> None:
        assert self.mem is not None
        self.mem.last3.append(result.opp_action)

        if self.mem.state == "ZH":
            if len(self.mem.last3) == 3 and all(a <= 2 for a in self.mem.last3):
                self.mem.state = "ZD"
        else:
            if result.opp_action > 2:
                self.mem.state = "ZH"
