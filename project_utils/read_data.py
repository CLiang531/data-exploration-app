import os
import shutil

import kagglehub
import pandas as pd

from project_utils.data_helpers import convert_id


def kaggle_download(download_link, input_folder):
    input_folder = "../" + input_folder
    file_name = download_link.split("/")[-1].replace("-", "_") + '.csv'
    target_path = os.path.join(input_folder, file_name)
    if not os.path.exists(input_folder + "/" + file_name):
        src_path = kagglehub.dataset_download(download_link)
        for f in os.listdir(src_path):
            if f.endswith(".csv"):
                shutil.copy(os.path.join(src_path, f), target_path)
    return file_name, csv_to_df(target_path)


def csv_to_df(file):
    try:
        df = pd.read_csv(file)
        convert_id(df)
        return df
    except Exception as e:
        print("Failed to convert csv file:", str(e))
        return None


def excel_to_df(file):
    try:
        df = pd.read_excel(file)
        convert_id(df)
        return df
    except Exception as e:
        print("Failed to convert xlsx file:", str(e))
        return None


def load_file(file):
    extension = file.name.split(".")[-1].lower()
    if extension == "csv":
        return csv_to_df(file)
    elif extension in ["xls", "xlsx"]:
        return excel_to_df(file)
    else:
        return extension
