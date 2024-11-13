# Installation
- [Install](https://dev.mysql.com/doc/mysql-installation-excerpt/5.7/en/) MySQL and create local connection instance.
- Clone this repo and its submodules
```
git clone --recurse-submodules -j8 https://github.com/Felix-Zhenghao/robotDB.git
cd robotDB
```
- Setup the virtual environment
```
python -m venv .venv
source .venv/bin/activate
```
- Install python package dependencies
```
pip install -r requirements.txt
```
- Set name of the submodules.

`pip` won't install anything, it will just setup the name field.
```
cd robomimic
pip install -e .
cd ..

cd mimicgen
pip install -e .
cd ..
```
- Check your installation

If you run the following commands and see a simulation scene on your computer, congratulations!
```
cd tutorial/1_example_connect_robosuite_and_mimicgen/
python3 main.py
```

# ER V1.0
![ER Diagram of robotDB](assets/ER_robotDB.png)