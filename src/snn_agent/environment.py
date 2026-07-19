"""
Six-Arm Symmetric Maze Environment
----------------------------------
A flat, symmetric task with 6 goals where the agent chooses one action (0-5)
after a cue presentation phase.
All goals have equal cost (1 step) and equal reward structure (+1.0 / -1.0).

Observation:
  - One-hot cue for each candidate goal (N_GOALS bits)
  - A "hint active" flag (1 bit): 1 during cue phase, 0 during navigation

Action: 0 to 5 (corresponding to picking one of the 6 goals)
"""

import numpy as np
from typing import List, Optional, Tuple

N_GOALS = 6
CUE_STEPS = 5            # timesteps the cue is shown before navigation starts

class MultipleTMaze:
    """
    Symmetric 6-Goal Maze (Renamed internally to avoid changing imports).
    
    Parameters
    ----------
    n_goals : int
        Total number of goal locations (default 6).
    fixed_goals : Optional[List[int]]
        If provided, always use these goals every episode (no curriculum).
    """

    OBS_DIM = N_GOALS + 1   # goal cues + hint flag
    ACT_DIM = N_GOALS       # 6 actions for 6 goals

    def __init__(
        self,
        n_goals: int = N_GOALS,
        fixed_goals: Optional[List[int]] = None,
    ):
        self.n_goals = n_goals
        self.fixed_goals = fixed_goals

        self.cue_step = 0
        self.in_cue_phase = True
        self.active_goals: List[int] = []
        self.target_goal: int = 0
        self.done = False
        self.n_active_junctions = 1  # Dummy variable to satisfy trainer.py references
        self.rng = np.random.default_rng()

    # ------------------------------------------------------------------
    def set_active_goals(self, goals: List[int]) -> None:
        """Override the active goal list (used by the curriculum)."""
        self.active_goals = list(goals)

    # ------------------------------------------------------------------
    def reset(self, active_goals: Optional[List[int]] = None) -> np.ndarray:
        """
        Start a new episode.
        """
        self.cue_step = 0
        self.in_cue_phase = True
        self.done = False

        if self.fixed_goals is not None:
            self.active_goals = list(self.fixed_goals)
        elif active_goals is not None:
            self.active_goals = list(active_goals)

        # Pick which goal the agent must reach this episode
        self.target_goal = int(self.rng.choice(self.active_goals))
        return self._observe()

    # ------------------------------------------------------------------
    def step(self, action: int) -> Tuple[np.ndarray, float, bool, dict]:
        """
        Apply action and advance one timestep.
        """
        if self.done:
            raise RuntimeError("Call reset() before step() after episode end.")

        info: dict = {}

        if self.in_cue_phase:
            self.cue_step += 1
            if self.cue_step >= CUE_STEPS:
                self.in_cue_phase = False
            obs = self._observe()
            return obs, 0.0, False, info

        # Navigation phase: 1-step decision
        if action == self.target_goal:
            reward = 1.0
            info["outcome"] = "success"
        else:
            reward = -1.0
            info["outcome"] = "wrong_turn"
            
        self.done = True
        return self._observe(), reward, True, info

    # ------------------------------------------------------------------
    def _observe(self) -> np.ndarray:
        obs = np.zeros(self.OBS_DIM, dtype=np.float32)
        # Goal cues (one-hot over ALL N_GOALS positions; only active goals lit)
        for g in self.active_goals:
            obs[g] = 1.0
        # Hint flag
        obs[-1] = 1.0 if self.in_cue_phase else 0.0
        return obs

    # ------------------------------------------------------------------
    @property
    def obs_dim(self) -> int:
        return self.OBS_DIM

    @property
    def act_dim(self) -> int:
        return self.ACT_DIM
