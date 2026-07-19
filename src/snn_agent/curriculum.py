"""
Symmetric 6-Goal Curriculum
---------------------------
Phase 1: Present ONLY Goal 0 to force WTA attractor depth (create dead neurons).
Phase 2: Gradually increase the pool of possible goals.
Phase 3: All 6 goals are possible.
"""

import numpy as np
from collections import deque
from typing import Deque, List, Optional, Tuple

N_GOALS = 6

class GoalCurriculum:
    def __init__(
        self,
        total_episodes: int = 1000,
        n_hint_goals: int = 1, # Unused, just for compatibility
        max_gap: int = 50,     # Unused, just for compatibility
        phase1_frac: float = 0.40,
        phase2_frac: float = 0.30,
        fixed_goals: Optional[List[int]] = None,
        anchor_goal: Optional[int] = None,
        seed: int = 42,
    ):
        self.total = total_episodes
        self.fixed_goals = fixed_goals
        self.anchor_goal = anchor_goal

        p1 = int(total_episodes * phase1_frac)
        p2 = p1 + int(total_episodes * phase2_frac)
        self.phase1_end = p1
        self.phase2_end = p2

        self.rng = np.random.default_rng(seed)
        self._episode = 0

    def _current_phase(self) -> int:
        e = self._episode
        if e < self.phase1_end:
            return 1
        elif e < self.phase2_end:
            return 2
        else:
            return 3

    def next_episode_goals(self) -> Tuple[List[int], int]:
        phase = self._current_phase()

        if phase == 1:
            # Force target to be 0 to build massive attractor
            target = 0
        elif phase == 2:
            # Gradually expand pool size across Phase 2
            phase2_len = max(1, self.phase2_end - self.phase1_end)
            progress = (self._episode - self.phase1_end) / phase2_len
            # From 2 choices (0,1) up to 5 choices (0,1,2,3,4)
            pool_size = max(2, int(2 + progress * 4))
            pool_size = min(pool_size, N_GOALS - 1)
            target = int(self.rng.choice(range(pool_size)))
        else:
            # All 6 goals
            target = int(self.rng.choice(range(N_GOALS)))
            
        cues = [target]
        self._episode += 1
        return cues, target

    @property
    def episode(self) -> int:
        return self._episode

    @property
    def phase(self) -> int:
        return self._current_phase()

    def phase_description(self) -> str:
        p = self._current_phase()
        if p == 1:
            return f"Phase1(Target 0 ONLY, ep {self._episode}/{self.phase1_end})"
        elif p == 2:
            return f"Phase2(Expanding Pool, ep {self._episode}/{self.phase2_end})"
        else:
            return f"Phase3(All 6 goals, ep {self._episode})"
