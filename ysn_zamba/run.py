import os
from argparse import ArgumentParser

import pandas as pd
from zamba.models.model_manager import ModelManager

PATH_MODELS = "models"
PATH_VIDEOS = "videos"
PATH_RESULT = "result"
PATH_CONFIG = os.path.join(PATH_MODELS, "config")
PATH_CSV_FPS = os.path.join(PATH_RESULT, "video_filepaths.csv")
PATH_CSV_LABELS = os.path.join(PATH_RESULT, "zamba_predictions.csv")

MODEL_AFRICAN_SF = "african-slowfast"
MODEL_EUROPEAN = "european"

parser = ArgumentParser()
parser.add_argument(
    "-m",
    "--model",
    default=MODEL_AFRICAN_SF,
    choices=[MODEL_AFRICAN_SF, MODEL_EUROPEAN],
    dest="model",
    help="model type to run",
)


if __name__ == "__main__":
    args = parser.parse_args()
    print("Chosen model:", args.model)

    fps = list[str]()

    for subdir, dirs, files in os.walk(PATH_VIDEOS):
        for file in files:
            if not os.path.splitext(file)[1]:
                # ignores .gitkeep file, if any
                continue
            fps.append(os.path.join(subdir, file))

    df_fps = pd.DataFrame({"filepath": fps})
    df_fps.to_csv(PATH_CSV_FPS, index=False)

    manager = ModelManager.from_yaml(os.path.join(PATH_CONFIG, f"{args.model}.yml"))
    manager.predict()

    df_labels = pd.read_csv(PATH_CSV_LABELS)
    df_labels["label"] = df_labels.iloc[:, 1:].idxmax(axis=1)
    df_labels.to_csv(PATH_CSV_LABELS, index=False)

    print(f"\n{'*' * 10}\n")
    print("Done! Predictions can be found in", PATH_CSV_LABELS)
