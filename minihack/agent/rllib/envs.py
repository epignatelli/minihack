# Copyright (c) Facebook, Inc. and its affiliates.

from __future__ import annotations

from collections import OrderedDict
from typing import Tuple, Union

import gym
import numpy as np

from minihack.agent.common.envs.tasks import create_env
from minihack.base import MiniHack


class RLLibNLEEnv(gym.Env):
    def __init__(self, env_config: dict) -> None:
        # We sort the observation keys so we can create the OrderedDict output
        # in a consistent order
        self._observation_keys = sorted(
            env_config.get("observation_keys", ("blstats", "glyphs"))
        )
        self.gym_env = create_env(env_config["flags"])

    @property
    def action_space(self) -> gym.Space:
        return self.gym_env.action_space

    @property
    def observation_space(self) -> gym.Space:
        return self.gym_env.observation_space

    def reset(
        self, seed: int | None = None, options: dict = {}
    ) -> Tuple[dict, dict]:
        # this is tricky because `create_env` can return either
        # a MiniHack env or a NLE env, which now have different interfaces
        obs, info = self.gym_env.reset(seed, options)
        return self._process_obs(obs), info

    def _process_obs(self, obs: dict) -> dict:
        return OrderedDict({key: obs[key] for key in self._observation_keys})

    def step(
        self, action: Union[int, np.int64]
    ) -> Tuple[
        dict,
        Union[np.number, int],
        Union[np.bool_, bool],
        Union[np.bool_, bool],
        dict,
    ]:
        obs, reward, terminated, truncated, info = self.gym_env.step(action)
        return self._process_obs(obs), reward, terminated, truncated, info

    def render(self):
        return self.gym_env.render()

    def close(self):
        return self.gym_env.close()
