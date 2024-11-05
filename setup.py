from setuptools import setup, find_packages

setup(
    name="robotDB",  # The name of your package
    version="0.1",   # Version number
    packages=[package for package in find_packages(where='./mimicgen') if package.startswith("mimicgen")] + 
             [package for package in find_packages(where='./robomimic') if package.startswith("robomimc")], 
             # This will include all subdirs with __init__.py
    include_package_data=True,
    install_requires=[
        # List any other dependencies here
    ],
    # Other configuration options like author, description, etc.
)
