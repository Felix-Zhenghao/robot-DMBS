from robosuite.environments.manipulation.nut_assembly import NutAssembly

import mimicgen.utils.robomimic_utils as RobomimicUtils
from robomimic.envs.env_base import EnvType

import numpy as np

# register the environment Hello by inheriting from any MujocoEnv
class Hello(NutAssembly):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

# set env_meta
# IMPORTANT: args given in create_env() will override the args in env_meta
# for example, if you set has_renderer=False in env_meta, but set has_renderer=True in create_env(),
# the env will have renderer and will render the scene
env_meta = {"env_name": "Hello",
            "type": EnvType.ROBOSUITE_TYPE,
            "env_kwargs": {"robots": "Panda",
                           "has_renderer": False}}
env = RobomimicUtils.create_env(env_meta = env_meta,
                                camera_names=["frontview"],
                                camera_height=84,
                                camera_width=84,
                                use_image_obs=True,
                                use_depth_obs=False,
                                render=True)
print(type(env)) # EnvRobosuite


env.reset()
for i in range(100):
    result = env.step(np.random.randn(8))
    env.render(mode='human',camera_name='frontview')

    # this is a unique method of EnvRobosuite
    # if directly use NutAssembly, this method is not available
    # methods like this will be used in MimicGen data generation loop
    # so initialize the env with RobomimicUtils.create_env() is essential
    print(env.get_observation())
