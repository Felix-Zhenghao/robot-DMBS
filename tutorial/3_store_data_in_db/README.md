# [WIP]

# DOC VERSION: 1.0

> The first two part should be done when INSERT a new task and subtask. Convenient interfaces bridging the relational database and simulation framworks like MimicGen should be provided to do that. It may be faster to rewrite the simulation framework so that interfaces are more intuitive to connect to DB.

This document describes what may be done to use the data generation code of MimicGen, and connect the robotDB with the simulation framework.

# Use the original environment launch code
In mimicgen, the simulation environment is launched by [this](https://github.com/NVlabs/mimicgen/blob/main/mimicgen/scripts/generate_dataset.py#L230-L243).

The most important stuff is `env_meta`. The other parameter can be easily resolved and queried. Documentation of `env_meta` can be found [here](https://robomimic.github.io/docs/modules/environments.html#environments). My paraphrase:

- `env_meta` is a dictionary like this: `env_meta = {"env_name": str, "type": EnvType, "env_kwargs": dict}`
    - `env_name` is just a string and should be the same as `env_name`.
    - `type` is a enum can be found [here](https://github.com/Felix-Zhenghao/robomimic/blob/master/robomimic/envs/env_base.py#L9-L16).
    - `env_kwargs` is a long dict, example can be found [here](https://robomimic.github.io/docs/modules/environments.html#initialize-an-environment-from-a-dataset).

Now that we have the metadata of the environment. But we actually need to put robot and objects into the environment. This is pretty complicated. The inheritation path is for a task `Square_D0` is, for instance, `robosuite.environments.base.MujocoEnv` -> `robosuite.environments.robot_env.RobotEnv` -> `robosuite.environments.manipulation.manipulation_env.ManipulationEnv` -> `robosuite.environments.manipulation.single_arm_env.SingleArmEnv` -> `mimicgen.envs.robosuite.single_arm_env_mg.SingleArmEnv_MG` -> `mimicgen.envs.robosuite.nut_assembly.NutAssembly_D0 & Square_D0`. In this case, the env_name should be `Square_D0`. The implementation of [`SingleArmEnv_MG`](https://github.com/NVlabs/mimicgen/blob/main/mimicgen/envs/robosuite/single_arm_env_mg.py#L20) and [`Square_D0`](https://github.com/NVlabs/mimicgen/blob/main/mimicgen/envs/robosuite/nut_assembly.py#L62) can be referenced.

This is the most complicated part of connecting robotDB with MimicGen or Robosuite.