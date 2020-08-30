#!/usr/bin/env python3
""" Functions for read-in data & processing dataframe. (Unfinished)

Author: WangZiyong
Date: 7/25/2020
Git: https://github.com/imporatore/AI-map
"""
import os
import pandas as pd

from joblib import Parallel, delayed
from config import N_JOBS
from tqdm import tqdm


def aff2region(aff):
    """ Affiliation to region, (city, province, country).

    For foreign city, province is Nan."""
    pass


def isA(venue):
    """ Determine if is A by publication venue."""
    pass


def impactfactor(venue):
    """ Calculate the impact factor by journal."""
    pass


def read_csv(dir, fname, **kwargs):
    return pd.read_csv(os.path.join(dir, fname), **kwargs)


def strprocess(string, prefix):
    return string.lstrip(prefix + ' ').rstrip('\n')


def process_paper(df):
    df["city"], df['province'], df["country"] = df["affiliations"].apply(aff2region)
    df["isA"] = df["venue"].apply(isA)
    df["IF"] = df["venue"].apply(impactfactor)
    return df


def multiprocess(func, data, n_jobs=N_JOBS):
    """ Apply func on data

    return merged Dataframe.
    Args:
        - func: function to apply on data
        - data: iterable data
            generated from i.e. dataframe.groupby()
        - n_jobs: int, default cpu cores num
            process num for multiprocess, set in config.py
    Returns:
        pd.Dataframe
        merged Dataframe
    """
    results = Parallel(n_jobs=n_jobs)(delayed(func)(d) for d in tqdm(data))
    return pd.concat(results, ignore_index=True)


def split_data(data, size=None, by=''):
    """ Split data for multiprocess

    used for array-like object, i.e. f.readlines().
    Args:
        - data: array-like object or pd.Dataframe
            generated from i.e. f.readlines()
        - size: int, default None
            size for every split of data, None stands for exactly n_jobs split of data.
        - by: string, column name of data
            data will be grouped by
    Returns:
        list of split data
    """
    if by:
        return [group.copy() for name, group in data.groupby(by)]
    if not size:
        size = (len(data) - 1)//N_JOBS + 1
    return [data[size*i: size*(i+1)] for i in range(len(data)//size)] + [data[size*(len(data)//size):]]
