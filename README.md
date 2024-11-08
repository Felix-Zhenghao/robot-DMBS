# Installation
- [Install](https://dev.mysql.com/doc/mysql-installation-excerpt/5.7/en/) MySQL and create local connection instance.
- Clone this repo
```
git clone https://github.com/Felix-Zhenghao/robotDB.git
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
- Set name of the submodules. `pip` won't install anything, it will just setup the name field.
```
cd robomimic
pip install -e .
cd ..

cd mimicgen
pip install -e .
cd ..
```
- Check your installation
```
TODO
```