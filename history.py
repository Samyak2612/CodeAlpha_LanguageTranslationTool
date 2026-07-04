import os
import pandas as pd
from datetime import datetime

FILE_NAME = "history.csv"


def create_history_file():
    if not os.path.exists(FILE_NAME):
        df = pd.DataFrame(
            columns=[
                "Date",
                "Source",
                "Target",
                "Original Text",
                "Translated Text"
            ]
        )
        df.to_csv(FILE_NAME, index=False)


def save_history(source, target, original, translated):

    create_history_file()

    df = pd.read_csv(FILE_NAME)

    new_row = {
        "Date": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        "Source": source,
        "Target": target,
        "Original Text": original,
        "Translated Text": translated
    }

    df.loc[len(df)] = new_row

    df.to_csv(FILE_NAME, index=False)


def load_history():

    create_history_file()

    return pd.read_csv(FILE_NAME)