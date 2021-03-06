import pandas as pd
import numpy as np

__all__ = ['list_to_string', 'strip_columns', 'outlier_mask', 'trimean',
           'variance_coefficient', 'placehold_to_nan']


PLACEHOLDERS = [-1, -999, -9999, 'None', 'none', 'missing', 'Missing', 
                'Null', 'null', '?', 'inf', np.inf]


'''
Supporting functions for exploratory data analysis
'''


def outlier_mask(feature, inclusive=True):
    '''
    Creates a mask of the outliers using IQR

    Input:
    feature: Pandas Series object containing numeric values
    inclusive: bool, default is True, whether to include values that lie on the
              boundary of becoming an outlier. False will consider the edge
              cases as outliers.

    Output:
    Return a Pandas Series object of booleans where True values correspond
    to outliers in the original feature
    '''
    q1 = feature.quantile(.25)
    q3 = feature.quantile(.75)
    iqr = q3-q1
    mask = ~feature.between((q1-1.5*iqr), (q3+1.5*iqr), inclusive=inclusive)
    return mask


def trimean(feature):
    '''
    Calculate the trimean. Trimean is a measure of the
    center that combines the medians emphasis on center values with the
    midhinge's attention to the extremes.

    Input:
    feature: Pandas Series or DataFrame Object containing numeric values

    Output:
    Return the trimean as a float or an array of floats
    '''
    q1 = feature.quantile(.25)
    q2 = feature.median()
    q3 = feature.quantile(.75)

    return ((q1+2*q2+q3)/4)


def variance_coefficient(feature):
    '''
    Calculate the coefficient of variance

    Input:
    feature: Pandas Series or DataFrame Object containing numeric values

    Output:
    Return the coefficient of variance as a float or an array of floats
    '''

    return (feature.var()/feature.mean())


def _flatten_list(l):
    '''
    "Flatten" a nested list down to a single layer

    Input:
    l: A list

    Output:
    Return out, a list made of the values in nested list `l`
    '''
    out = []
    for item in l:
        if isinstance(item, (list, tuple)):
            out.extend(_flatten_list(item))
        else:
            out.append(item)
    return out


def list_to_string(l, separator=', '):
    '''
    Helper function to convert lists to string and keep clean code

    Input:
    list: a list
    separator: a string used as the separating value between items
               in the list, default = ', '

    Output:
    Return a string made from list with separator between values.
    '''
    l = _flatten_list(l)
    return separator.join(str(item) for item in l)


def strip_columns(df):
    '''
    Helper function to remove leading or trailing spaces from
    all values in a dataframe

    Input:
    df: Pandas DataFrame Object

    Output:
    Return a Pandas DataFrame object
    '''
    df = df.copy()

    for col in df.select_dtypes(exclude='number').columns:
        df[col] = df[col].str.strip()

    return df


def placehold_to_nan(df, placeholders=PLACEHOLDERS):
    '''
    Convert all values in df that are in placeholders to NaN

    Input:
    df: Pandas DataFrame or Series object
    placeholders: a list of values used as placeholders for NaN

    Output
    Return df with all placeholder values fill with NaN
    '''
    return df.replace(placeholders, np.NaN)
