from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple

from .game import payoff, validate_action
from .strategy_base import Strategy
from .types import MatchResult, Observation


@dataclass
class MatchConfig:
    """
    Configuration for a 1v1 match.
    """
    N: int           # number of possible bids
    rounds: int      # how many times the game is repeated
    verbose: bool    # print each round if True


class IteratedMatch:
    """
    Runs a repeated 1v1 bidding game between two strategies.
    """

    def __init__(self, A: Strategy, B: Strategy, cfg: MatchConfig):
        self.A = A
        self.B = B
        self.cfg = cfg

        # Store full action history
        self.A_actions: List[int] = []
        self.B_actions: List[int] = []

        # Cumulative scores
        self.scoreA = 0
        self.scoreB = 0

    def _print_round(self, t: int, a: int, b: int, pa: int, pb: int) -> None:
        """
        Helper to print one round's result.
        """
        print(
            f"Round {t:3d} | "
            f"{self.A.name}: bid={a:2d}, payoff={pa:2d}, total={self.scoreA:4d} || "
            f"{self.B.name}: bid={b:2d}, payoff={pb:2d}, total={self.scoreB:4d}"
        )

    def run(self) -> Tuple[int, int]:
        """
        Main loop:
        - reset both strategies
        - repeat bidding for cfg.rounds
        - return final scores
        """
        self.A.reset(N=self.cfg.N)
        self.B.reset(N=self.cfg.N)

        for t in range(1, self.cfg.rounds + 1):
            # Build observations
            obsA = Observation(
                N=self.cfg.N, t=t,
                self_name=self.A.name, opponent_name=self.B.name,
                opp_action_history=tuple(self.B_actions),
                self_action_history=tuple(self.A_actions),
            )
            obsB = Observation(
                N=self.cfg.N, t=t,
                self_name=self.B.name, opponent_name=self.A.name,
                opp_action_history=tuple(self.A_actions),
                self_action_history=tuple(self.B_actions),
            )

            # Strategies choose bids
            a = self.A.act(obsA)
            b = self.B.act(obsB)
            validate_action(a, self.cfg.N)
            validate_action(b, self.cfg.N)

            # Compute payoff
            pa, pb = payoff(a, b)
            self.scoreA += pa
            self.scoreB += pb

            # Record history
            self.A_actions.append(a)
            self.B_actions.append(b)

            if self.cfg.verbose:
                self._print_round(t, a, b, pa, pb)

            # Notify strategies of result
            self.A.on_result(MatchResult(
                N=self.cfg.N, t=t,
                self_name=self.A.name, opponent_name=self.B.name,
                self_action=a, opp_action=b,
                self_payoff=pa, opp_payoff=pb,
            ))
            self.B.on_result(MatchResult(
                N=self.cfg.N, t=t,
                self_name=self.B.name, opponent_name=self.A.name,
                self_action=b, opp_action=a,
                self_payoff=pb, opp_payoff=pa,
            ))

        return self.scoreA, self.scoreB