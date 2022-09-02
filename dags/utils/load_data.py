import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from utils.files_util import save_files, load_files


def load_data():

    # load data from local file
    producrec_ds = load_files(['raw_data'])[0]
    producrec_data = producrec_ds.iloc[:, :-2]
    producrec_labels = producrec_ds.iloc[:, -2]
    df = producrec_data
    df['labels'] = producrec_labels

    # label encoding for categorical fields
    le = LabelEncoder()
    df['producrec_dataset_acq.site_id'] = le.fit_transform(
        df['producrec_dataset_acq.site_id'])
    df['producrec_dataset_acq.category'] = le.fit_transform(
        df['producrec_dataset_acq.category'])

    # save dataset
    df.name = 'df'
    save_files([df])
