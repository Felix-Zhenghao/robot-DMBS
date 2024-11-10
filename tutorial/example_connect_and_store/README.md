# DOC VERSION 1.0
TODO: write code the put data into database rather than only in `.npz` file.

# Data flushing
Robosuite human demo collection can be ran in the standalone mode of file `robosuite.scripts.collect_human_demonstrations.py`. It does two things:
- collect human demo data and flush it into an `.npz` file;
- convert `.npz` file into `hdf5` file.

Therefore, we shall delete the `hdf5` convertion part, and store information from the `.npz` file into our database, and discard the `.npz` file.

The data flushing code is [here](https://github.com/Felix-Zhenghao/robosuite/blob/master/robosuite/wrappers/data_collection_wrapper.py#L119-L138). Also pay attention that there will be mutiple files flushed because there's a [flush_frequency](https://github.com/Felix-Zhenghao/robosuite/blob/master/robosuite/wrappers/data_collection_wrapper.py#L193-L194). If we want to store data per-frame, then use `flush_freq=1`; if we want to store per-demo, then make `flush_freq` very big. Pay attention that if the task is too long-horizon, we may run out of RAM!!! We only need to modify `_flush()` and `flush_freq`, and we can have our data organized in the database!

Note that the state data is [flattened](https://github.com/Felix-Zhenghao/robosuite/blob/master/robosuite/wrappers/data_collection_wrapper.py#L175). Only position, velocity is in the state data. To convert state data into, say, camera observation, robomimic will replay the episode according to state. There is a trade-off here: if we only store state data, we will have less I/O overhead when reading data and less disk storage and RAM demand, but we will need more compute to restore other observation. Else, if we store the whole `OrderedDict` the env returns, we will use less compute but more disk storage space, RAM and I/O overhead.

**Here, for simplicity, we directly flush all observation data. This will make the code much cleaner. Another modification is we choose to flush data once for one demo. This will cause more RAM demand during data collection.**

Directly run `example_collect_and_store.py` to try data collection.

# Replay episode
To replay the episode you collected, please directly run `replay.py` by giving argument `--npz_file_path`, which should be the direct path of your `.npz` file collected by running `example_collect_and_store.py`. For example, on my computer, if I run this cmd, I will get a video as follows.
```
python tutorial/example_connect_and_store/replay.py --npz_file_path 1731195902_593687/ep_1731195903_172489/state_1731195918_370972.npz
```

The replay can be split into following steps:
- create an identical environment as where the demo happened
- set the env state to the initial state of the demo
- feed demo actions and step the environment

`replay.py` will also save the video record of the replay as `assets/video.mp4`.