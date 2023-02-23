import numpy as np
from keras.models import load_model
import pandas as pd
import argparse


class predict:

    def __init__():
        parser = argparse.ArgumentParser()
        parser.add_argument('--instance_path',
                            help='Relative path to the instance folder')
        parser.add_argument(
            '--model_path', help='Relative path to the model saving location')

    def PredictArrhythmia():
        args = parser.parse_args()
        model = load_model(args.model_path)

        instance = pd.read_csv(args.instance_path)
        instance = np.expand_dims(instance, axis=0)

        prediction = model.predict(instance)

        return prediction[0][1]
