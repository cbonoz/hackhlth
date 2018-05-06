
import pandas as pd
from sklearn.externals import joblib
from simplestatistics import *
from colorama import Fore, Back, Style

# Mean	mean([1, 2, 3])
# Median	median([10, 2, -5, -1])
# Mode	mode([2, 1, 3, 2, 1])
# Geometric mean	geometric_mean([1, 10])
# Harmonic mean	harmonic_mean([1, 2, 4])
# Root mean square	root_mean_square([1, -1, 1, -1])
# Add to mean	add_to_mean(40, 4, (10, 12))
# Skewness	skew([1, 2, 5])
# Kurtosis	kurtosis([1, 2, 3, 4, 5])
# Sample and population variance	variance([1, 2, 3], sample = True)
# Sample and population Standard deviation	standard_deviation([1, 2, 3], sample = True)
# Sample and population Coefficient of variation	coefficient_of_variation([1, 2, 3], sample = True)
# Interquartile range	interquartile_range([1, 3, 5, 7])
# Sum of Nth power deviations	sum_nth_power_deviations([-1, 0, 2, 4], 3)
# Sample and population Standard scores (z-scores)	z_scores([-2, -1, 0, 1, 2], sample = True)
def process_data(accel_data, gyro_data):
    """
    Return raw accel or gyro data in the form of a training sample for prediction
    :param accel: accel data for prediction
    :param gyro: gyro data for prediction
    :return: dataframe with one row ready for prediction via the 'predict' method below.
    """

    df = {}
    for col in ['x', 'y', 'z']:
        accel = list(map(lambda val: val[col], accel_data))
        gyro = list(map(lambda val: val[col], gyro_data))
        #         print(accel, len(gyro))
        df['accel-mean-%s' % col] = mean(accel)
        df['accel-median-%s' % col] = median(accel)
        #         df['accel-mode-%s' % col] = mode(accel)
        #         df['accel-skew-%s' % col] = skew(accel)
        #         df['accel-kurt-%s' % col] = kurtosis(accel)
        df['accel-rms-%s' % col] = root_mean_square(accel)
        df['accel-std-%s' % col] = standard_deviation(accel)
        #         df['accel-zscore-%s' % col] = z_scores(accel)
        df['accel-min-%s' % col] = min(accel)
        df['accel-max-%s' % col] = max(accel)

        df['gyro-mean-%s' % col] = mean(gyro)
        df['gyro-median-%s' % col] = median(gyro)
        #         df['gyro-mode-%s' % col] = mode(gyro)
        #         df['gyro-skew-%s' % col] = skew(gyro)
        #         df['gyro-kurt-%s' % col] = kurtosis(gyro)
        df['gyro-rms-%s' % col] = root_mean_square(gyro)
        df['gyro-std-%s' % col] = standard_deviation(gyro)
        #         df['gyro-zscore-%s' % col] = z_scores(gyro)
        df['gyro-min-%s' % col] = min(gyro)
        df['gyro-max-%s' % col] = max(gyro)

    #     return pd.Series(df).to_frame()
    return df

class Predict:
    # Prediction class and utility methods for the stimalert server application.

    def __init__(self):
        self.clf = joblib.load('./ml/stim_clf.pkl')
        self.last_prediction = {}

    # Mean	mean([1, 2, 3])
    # Median	median([10, 2, -5, -1])
    # Mode	mode([2, 1, 3, 2, 1])
    # Geometric mean	geometric_mean([1, 10])
    # Harmonic mean	harmonic_mean([1, 2, 4])
    # Root mean square	root_mean_square([1, -1, 1, -1])
    # Add to mean	add_to_mean(40, 4, (10, 12))
    # Skewness	skew([1, 2, 5])
    # Kurtosis	kurtosis([1, 2, 3, 4, 5])
    # Sample and population variance	variance([1, 2, 3], sample = True)
    # Sample and population Standard deviation	standard_deviation([1, 2, 3], sample = True)
    # Sample and population Coefficient of variation	coefficient_of_variation([1, 2, 3], sample = True)
    # Interquartile range	interquartile_range([1, 3, 5, 7])
    # Sum of Nth power deviations	sum_nth_power_deviations([-1, 0, 2, 4], 3)
    # Sample and population Standard scores (z-scores)	z_scores([-2, -1, 0, 1, 2], sample = True)
    def process_data(self, accel_data, gyro_data):
        """
        Return raw accel or gyro data in the form of a training sample for prediction
        :param accel: accel data for prediction
        :param gyro: gyro data for prediction
        :return: dataframe with one row ready for prediction via the 'predict' method below.
        """
        # print(accel, gyro)
        df = {}
        for col in ['x', 'y', 'z']:
            accel = list(map(lambda val: val[col], accel_data))
            gyro = list(map(lambda val: val[col], gyro_data))
            df['accel-mean-%s' % col] = mean(accel)
            df['accel-median-%s' % col] = median(accel)
            df['accel-rms-%s' % col] = root_mean_square(accel)
            df['accel-std-%s' % col] = standard_deviation(accel)
            df['accel-min-%s' % col] = min(accel)
            df['accel-max-%s' % col] = max(accel)

            df['gyro-mean-%s' % col] = mean(gyro)
            df['gyro-median-%s' % col] = median(gyro)
            df['gyro-rms-%s' % col] = root_mean_square(gyro)
            df['gyro-std-%s' % col] = standard_deviation(gyro)
            df['gyro-min-%s' % col] = min(gyro)
            df['gyro-max-%s' % col] = max(gyro)

        res = pd.Series(df).to_frame()
        return res.T

    def is_new_stim(self, userId):
        if userId in self.last_prediction:
            # return True if the last_prediction was negative.
            return not self.last_prediction[userId]
        # not present is a new stim
        return True

    def predict_stim(self, userId, test_data):
        """
        :param accel: array of {x: .., y: .., z: ..} accel values.
        :param gyro: array of {x: .., y: .., z: ..} gyro values.
        :return: prediction of stimming or not stimming
        """
        # print(test_data)
        prediction = self.clf.predict(test_data)
        print(test_data.shape, prediction)
        pred = int(prediction[0])
        if pred:
            color = Fore.RED
            text = "Stimming Detected"
        else:
            color = Fore.GREEN
            text = "Ok"
        print('Current Stimming Status: ' + color + '%s' % text)
        if pred:
            print(Fore.RED + "Stimming detected for user (%s)\nEntry created in softheon DB." % userId)

        print(Style.RESET_ALL)
        self.last_prediction[userId] = pred
        return pred






