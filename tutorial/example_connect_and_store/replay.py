import argparse
import robosuite as suite
import numpy as np
import imageio

from robosuite import load_controller_config

def replay_episode(npz_file_path,
                   gif_path="assets/video.mp4",
                   camera="agentview"):

    dic = np.load(npz_file_path, allow_pickle=True)

    config = {
        "env_name": "Lift",
        "robots": "Panda",
        "controller_configs": load_controller_config(default_controller="OSC_POSE"),
    }
    env = suite.make(
        **config,
        has_renderer=True,
        has_offscreen_renderer=True,
        ignore_done=True,
        use_camera_obs=True,
        reward_shaping=True,
        control_freq=20,
    )
    env.sim.set_state_from_flattened(dic["initial_state"])


    writer = imageio.get_writer(gif_path, fps=20)

    actions = dic["action_infos"]
    for action in actions:
        obs, _, _, _ = env.step(action["actions"])
        frame = obs[camera + "_image"]
        writer.append_data(frame)
        env.render()
    
    writer.close()
    print(f"Video saved at {gif_path}")

    env.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--npz_file_path",
        type=str,
        help="Abosolute path to the npz file, for example: 1731195902_593687/ep_1731195903_172489/state_1731195918_370972.npz",
    )
    parser.add_argument(
        "--gif_path",
        default="assets/video.mp4",
        help="Path to save the video",
    )
    parser.add_argument(
        "--camera",
        default="agentview",
        help="Which camera view to take the video from",
    )
    args = parser.parse_args()
    replay_episode(args.npz_file_path, args.gif_path, args.camera)