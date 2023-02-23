from __future__ import print_function

import argparse
import numpy as np
import keras
import os
import load
import util


class Predict:
    def __init__():
        pass

    def predict(data_json, model_path):
        preproc = util.load(os.path.dirname(model_path))
        dataset = load.load_dataset(data_json)
        x, y = preproc.process(*dataset)

        model = keras.models.load_model(model_path)
        probs = model.predict(x, verbose=1)

        return probs
