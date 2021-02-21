# Training as you like

Extract this project folder to ASFG root folder and you are ready to go (the ipynb files should be at the same level as those py files under ASFG root folder). It's OK to cover the original files if this is the first time you do it.

## The training pipeline

1. **Collect data**. You can get any video/audio file and it's **corresponding** subtitle files under a same folder and name them properly (see *src* folder).
   - Better use Audio file, which can save you a lot of time for building the dataset.
   - Better check and clean the subtitle file a bit and remove events that do not contain human speeches.
2. **Run** *build-data.ipynb* **and wait the dataset to be ready**. You need to create the folder holding the dataset under *data* folder.
3. **Run** *train-xxx.ipynb*. Specify the dataset folder you want to use (Under *data* folder).

You can tune params in those files and use your settings as you like.

The final model will be stored under *train/logs/trainName/checkpoint*.

See *dump-jupyter.py* if you prefer python scripts.
