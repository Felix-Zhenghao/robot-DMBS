# DOC VERSION 1.0

This file will give an example of the data generator pipeline of MimicGen. All code is only in one file to avoid complicated import relationship. Understanding this tutorial, you can easily connect MimicGen datagen pipeline with database query and storage pipeline.

# Five key steps:
- Define task_spec and register the use using MG_EnvInterface.
- Instantiate an environment for the task.
- Mimic `mimicgen.utils.file_utils.parse_source_dataset()` to get info needed for datagen.
- Instantiate `DataGenerator` class and rewrite specific part of the class.
- Use things above and code in `generate_dataset.py` to generate data.

