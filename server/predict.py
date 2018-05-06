
import pandas as pd
from sklearn.externals import joblib


class Predict:
    # Prediction class and utility methods for the stimalert server application.

    def __init__(self):
        self.clf = joblib.load('./ml/stim_clf.pkl')

    def process_data(self, accel, gyro):
        """
        Return raw accel or gyro data in the form of a training sample for prediction
        :param accel: accel data for prediction
        :param gyro: gyro data for prediction
        :return: dataframe with one row ready for prediction via the 'predict' method below.
        """

        return pd.Dataframe()

    def predict(self, data):
        """
        :param data: dataframe containing data for prediction
        :return: list of predicted activity values for each row of data.
        """

        return pd.Dataframe()






