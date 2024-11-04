# read the contents of your README file
from os import path

from setuptools import find_packages, setup

setup(
    name="db-pj",
    packages=[package for package in find_packages() if package.startswith("robosuite")],
    install_requires=[
        "numpy>=1.13.3",
        "numba>=0.49.1",
        "scipy>=1.2.3",
        "mujoco>=3.2.3",
        "mink>=0.0.5",
        "Pillow",
        "opencv-python",
        "pynput",
        "termcolor",
        "pytest",
        "h5py", # mimicgen dependencies start here
        "tqdm",
        "huggingface_hub",
        "mysql",
        "imageio",
        "imageio-ffmpeg",
        "gdown",
        "chardet"
    ],
    eager_resources=["*"],
    include_package_data=True,
    python_requires=">=3",
    description="Final Project of Uchicago Databases Course",
    author="Zhenghao Chi",
    author_email="felix020422@uchicago.edu",
    version="0.0.1",
)