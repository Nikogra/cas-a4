# Random strategy: chooses a random bid every round

import random

from shared.types import MatchResult, Observation


class RandomBid:
    name = "RandomBid"

    def reset(self, *, N: int) -> None:
        self.N = N

    def act(self, obs: Observation) -> int:
        return random.randint(1, self.N)

    def on_result(self, result: MatchResult) -> None:
        pass
