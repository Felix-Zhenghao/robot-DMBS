# DOC VERSION: 1.0
> See [`tutorial/example_connect_robosuite_and_mimicgen.py`](https://github.com/Felix-Zhenghao/robotDB/blob/main/tutorial/example_connect_robosuite_and_mimicgen.py) to see the code example of this doc.

The key take away is: **MimicGen use some env interfaces only provided in env instances of robomimic, so if you initialize the env directly from robosuite env, you can't use data generation pipeline of MimicGen.**

# Robosuite env single step return value
When we call `step(action)` of an MujocoEnv, the return value will be a 4-element tuple: `return observations, reward, done, info`. An example output of running `env = NutAssembly(robots = 'Panda', has_renderer=True)` is as follows. The (reward, done, info) is `(0.0, True, {})`, which is fairly simple.  
```
(OrderedDict([('robot0_joint_pos_cos', array([ 0.98452707,  0.98368445,  0.87087543, -0.55853277,  0.99127572,
       -0.31348286,  0.81896914])), ('robot0_joint_pos_sin', array([ 0.17523253, -0.17990248,  0.4915038 , -0.82948246, -0.13180457,
        0.94959386, -0.57383756])), ('robot0_joint_vel', array([-0.05168522, -0.22064078,  0.04784381,  0.03584339,  0.16332346,
       -0.13361397, -0.00621624])), ('robot0_eef_pos', array([-0.1759141 ,  0.28746571,  1.27380365])), ('robot0_eef_quat', array([ 0.4835664 ,  0.86693492, -0.09200673,  0.07824415])), ('robot0_gripper_qpos', array([ 0.01811937, -0.01786578])), ('robot0_gripper_qvel', array([ 0.02636029, -0.0260703 ])), 
       ('agentview_image', array(
        [[[249, 247, 242],
        [247, 247, 240],
        [247, 247, 240],
        ...,
        [252, 250, 247],
        [252, 251, 248],
        [252, 251, 248]],

       ...,

       [[115, 113, 110],
        [115, 112, 109],
        [114, 112, 109],
        ...,
        [116, 114, 111],
        [117, 115, 111],
        [116, 114, 111]]], dtype=uint8)), ('SquareNut_pos', array([-0.11035299,  0.16765171,  0.82997895])), ('SquareNut_quat', array([-9.17026749e-08,  1.10729461e-06,  8.25343182e-02,  9.96588223e-01])), ('SquareNut_to_robot0_eef_pos', array([-0.03312483,  0.03137835,  0.46211693])), ('SquareNut_to_robot0_eef_quat', array([-0.5534685 , -0.82406634,  0.09815004,  0.07038441], dtype=float32)), ('RoundNut_pos', array([-0.11372572, -0.20251221,  0.82998846])), ('RoundNut_quat', array([-6.11823444e-06, -1.10261564e-05,  4.85193947e-01, -8.74406561e-01])), ('RoundNut_to_robot0_eef_pos', array([-0.33640393, -0.16228006,  0.54901284])), ('RoundNut_to_robot0_eef_quat', array([-0.00220262, -0.99267554,  0.04248767,  0.11307085], dtype=float32)), ('robot0_proprio-state', array([ 0.98452707,  0.98368445,  0.87087543, -0.55853277,  0.99127572,
       -0.31348286,  0.81896914,  0.17523253, -0.17990248,  0.4915038 ,
       -0.82948246, -0.13180457,  0.94959386, -0.57383756, -0.05168522,
       -0.22064078,  0.04784381,  0.03584339,  0.16332346, -0.13361397,
       -0.00621624, -0.1759141 ,  0.28746571,  1.27380365,  0.4835664 ,
        0.86693492, -0.09200673,  0.07824415,  0.01811937, -0.01786578,
        0.02636029, -0.0260703 ])), ('object-state', array([-1.10352991e-01,  1.67651708e-01,  8.29978946e-01, -9.17026749e-08,
        1.10729461e-06,  8.25343182e-02,  9.96588223e-01, -3.31248346e-02,
        3.13783489e-02,  4.62116925e-01, -5.53468525e-01, -8.24066341e-01,
        9.81500372e-02,  7.03844056e-02, -1.13725715e-01, -2.02512207e-01,
        8.29988457e-01, -6.11823444e-06, -1.10261564e-05,  4.85193947e-01,
       -8.74406561e-01, -3.36403926e-01, -1.62280062e-01,  5.49012835e-01,
       -2.20261887e-03, -9.92675543e-01,  4.24876660e-02,  1.13070846e-01]))]), 0.0, True, {})
```

# Method to initialize the environment properly
The key take away is: **MimicGen use some env interfaces only provided in env instances of robomimic, so if you initialize the env directly from robosuite env, you can't use data generation pipeline of MimicGen.**

There are three steps, see [here]((https://github.com/Felix-Zhenghao/robotDB/blob/main/tutorial/example_connect_robosuite_and_mimicgen.py)) for code:
- Register the environment my inheriting from any class inherited from `MujocoEnv` of robosuite.
- Prepare `env_meta`
- Use `RobomimicUtils.create_env()` to instantiate the environment