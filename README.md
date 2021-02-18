# Traning as you like

Extract this folder under ASFG root folder and you are ready to go.

## The training pipeline

1. **Collect data**. You can get any video/audio file and it's **corresponding** subtitle files under a same folder and name them properly (see *src* folder).
   - Better use Audio file, which can save you a lot of time for building the dataset.
   - Better check and clean the subtitle file a bit and remove events that do not contain human speeches.
2. **Run** *build-data.ipynb* **and wait the dataset to be ready**. You need to create the folder holding the dataset under *data* folder.
3. **Run** *train-xxx.ipynb*. Specify the dataset folder you want to use (Under *data* folder).

You can tune params in those files and use your settings as you like.

The final model will be stored under *train/logs/trainName/checkpoint*.

See dump-jupyter.py if you want to use python scipts instead.
