import wfdb
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier


class Classifier:

    def __init__(self, arrhythmia_classes=None):
        if arrhythmia_classes is None:
            arrhythmia_classes = ['N', 'S', 'V', 'F', 'Q']
        self.arrhythmia_classes = arrhythmia_classes
        self.label_encoder = LabelEncoder()
        self.rfc = RandomForestClassifier(n_estimators=100, random_state=42)

    def load_data(self, record_name):
        record = wfdb.rdrecord(record_name)
        annotations = wfdb.rdann(record_name, 'atr')
        signal = record.p_signal[:, 0]
        labels = annotations.symbol
        return signal, labels

    def fit(self, X, y):
        y_encoded = self.label_encoder.fit_transform(y)
        self.rfc.fit(X, y_encoded)

    def predict(self, X):
        y_pred_encoded = self.rfc.predict(X)
        y_pred = self.label_encoder.inverse_transform(y_pred_encoded)
        return y_pred

    def _prepare_data(self, X, y):
        y_encoded = self.label_encoder.transform(y)
        mask = np.isin(y_encoded, np.arange(len(self.arrhythmia_classes)))
        X_filtered = X[mask]
        y_filtered_encoded = y_encoded[mask]
        y_filtered_onehot = np.zeros(
            (len(y_filtered_encoded), len(self.arrhythmia_classes)))
        y_filtered_onehot[np.arange(
            len(y_filtered_encoded)), y_filtered_encoded] = 1
        return X_filtered, y_filtered_onehot

    def fit_filtered(self, X, y):
        X_filtered, y_filtered = self._prepare_data(X, y)
        self.rfc.fit(X_filtered, y_filtered)

    def predict_filtered(self, X):
        y_pred = self.rfc.predict(X)
        y_pred_filtered = np.zeros(len(y_pred), dtype=np.int32)
        for i in range(len(y_pred)):
            if np.max(y_pred[i]) > 0:
                y_pred_filtered[i] = np.argmax(y_pred[i])
        y_pred_filtered = self.label_encoder.inverse_transform(y_pred_filtered)
        return y_pred_filtered
