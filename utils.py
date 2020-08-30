#!/usr/bin/env python3
""" Functions for read-in data & processing dataframe. (Unfinished)

Author: WangZiyong
Date: 7/25/2020
Git: https://github.com/imporatore/AI-map
"""
import os
import pandas as pd
import numpy as np

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


def replace_chr(string):
    string_ = string.replace("\xe2\x80\x99", "'") #84 apostrophe
    string_ = string_.replace("\xc2\xa8\xc2\xa2", "a") #32 Spanish a
    string_ = string_.replace("\xc2\xa8", "") # 445 next character is an umlatts
    string_ = string_.replace("\xc3\xa8", "e") # 19 French e
    string_ = string_.replace("\xc3\xad", "i") # 73 Spanish i
    string_ = string_.replace("\xc3\xa4", "a") # 66 German a
    string_ = string_.replace("\xc3\xaa", "e") # 2 Portugese E
    string_ = string_.replace("\xc3\xa3", "a") # 17 Portugese A
    string_ = string_.replace("\xc3\xb3", "o") # 55 Portugese O
    string_ = string_.replace("\xc3\xb6", "o") # 127 Swedish O
    string_ = string_.replace("\xc3\x96", "o") # 13 Swedish o
    string_ = string_.replace("\xc3\xaf", "i") # 3 Catalonian I
    string_ = string_.replace("\xc3\xb8", "o") # 20 Icelandic O
    string_ = string_.replace("\xc3\xba", "u") # 18 Catalonian u
    string_ = string_.replace("\xc3\x85", "a") # 2 Norwegian A
    string_ = string_.replace("\xc3\x89", "e") # 6 Swiss e
    string_ = string_.replace("\xc3\xa9", "e") # 234 French e
    string_ = string_.replace("\xc3\x9c", "u") # 5 Turkish U
    string_ = string_.replace("\xc3\xbc", "u") # 109 German u
    string_ = string_.replace("\xc3\xb1", "n") # 22 Spanish N
    string_ = string_.replace("\xc3\xb4", "o") # 3 French O
    string_ = string_.replace("\xc3\xa1", "a") # 105 Hungarian a
    string_ = string_.replace("\xc3\xa7", "c") # 28 Portugese c
    string_ = string_.replace("\xc3\x9f", "b") # 15 German B
    string_ = string_.replace("\xc3\xb5", "o") # 16 Portugese o
    string_ = string_.replace("\xc3\xa5", "a") # 4 Some? a
    string_ = string_.replace("\xc3\xa0", "a") # 3 Some? a
    string_ = string_.replace("\xc3\xab", "e") # 4 Some? e
    string_ = string_.replace("\xc3\xb2", "o") # 1 Some? o
    string_ = string_.replace("\xc5\x81", "l") # 4 Slavic L
    string_ = string_.replace("\xc5\x82", "l") # 35 Slavic L
    string_ = string_.replace(" \xc2\xb4 ", "")
    string_ = string_.replace(" \xc2\xb4", "")
    string_ = string_.replace("\xc2\xb4", "")
    string_ = string_.replace("\xc2\xb8", "")
    string_ = string_.replace("\xc2\xa6", "e")
    string_ = string_.replace("\xc2\xaa", "i")
    string_ = string_.replace("\xc4\xb1", "i")
    string_ = string_.replace("\xc3\xb0", "d")
    string_ = string_.replace("\xef\xbf\xbd", "e")
    string_ = string_.replace("\xc3\x9a", "u")
    string_ = string_.replace("é", "e")
    string_ = string_.replace("ö", "o")
    string_ = string_.replace("ä", "a")
    string_ = string_.replace("á", "a")
    string_ = string_.replace("í", "i")
    string_ = string_.replace("ı", "i")
    string_ = string_.replace("ä", "a")
    string_ = string_.replace('ĵ', 'j')
    string_ = string_.replace('ß', 'b')
    string_ = string_.replace('ó', 'o')
    string_ = string_.replace('ó', 'o')
    string_ = string_.replace('ł', 'l')
    string_ = string_.replace('č', 'c')
    string_ = string_.replace('à', "a")
    string_ = string_.replace('â', "a")
    string_ = string_.replace('ã', "a")
    string_ = string_.replace('å', "a")
    string_ = string_.replace('æ', "a")
    string_ = string_.replace('ç', "c")
    string_ = string_.replace('è', "e")
    string_ = string_.replace('ê', 'e')
    string_ = string_.replace('ë', 'e')
    string_ = string_.replace('ì', 'i')
    string_ = string_.replace('î', 'i')
    string_ = string_.replace('ï', 'i')
    string_ = string_.replace('ñ', 'n')
    string_ = string_.replace('ò', "o")
    string_ = string_.replace('ô', "o")
    string_ = string_.replace('õ', "o")
    string_ = string_.replace('ø', "o")
    string_ = string_.replace('ú', "u")
    string_ = string_.replace('û', "u")
    string_ = string_.replace('ü', "u")
    string_ = string_.replace('ý', 'y')
    string_ = string_.replace('ā', 'a')
    string_ = string_.replace('ă', 'a')
    string_ = string_.replace('ą', 'a')
    string_ = string_.replace('ć', 'c')
    string_ = string_.replace('ę', 'e')
    string_ = string_.replace('ě', "e")
    string_ = string_.replace('ğ', "g")
    string_ = string_.replace('ī', "i")
    string_ = string_.replace('ń', "n")
    string_ = string_.replace('ň', "n")
    string_ = string_.replace('ō', "o")
    string_ = string_.replace('œ', "o")
    string_ = string_.replace('ř', 'r')
    string_ = string_.replace('ś', 's')
    string_ = string_.replace('ş', 's')
    string_ = string_.replace('š', 's')
    string_ = string_.replace('ţ', 't')
    string_ = string_.replace('ū', 'u')
    string_ = string_.replace('ŵ', "w")
    string_ = string_.replace('ź', "z")
    string_ = string_.replace('ż', "z")
    string_ = string_.replace('ž', 'z')
    string_ = string_.replace('ǎ', 'a')
    string_ = string_.replace('ǒ', 'o')
    string_ = string_.replace('ǧ', 'g')
    string_ = string_.replace('ș', 's')
    string_ = string_.replace('ȩ', 'e')
    string_ = string_.replace('ÿ', 'y')
    string_ = string_.replace('ũ', 'u')
    string_ = string_.replace('ḱ', 'k')
    string_ = string_.replace('м', 'm')
    string_ = string_.replace('ĩ', 'i')
    string_ = string_.replace('ư', 'u')
    string_ = string_.replace('ầ', 'a')
    string_ = string_.replace('ẽ', 'e')
    string_ = string_.replace('ố', 'o')
    string_ = string_.replace('ḡ', 'g')
    string_ = string_.replace('ǵ', 'g')
    string_ = string_.replace('ṙ', 'r')
    string_ = string_.replace('ŏ', 'o')
    string_ = string_.replace('ế', 'e')
    string_ = string_.replace('ª', 'a')
    string_ = string_.replace('ľ', 'l')
    string_ = string_.replace('к', 'k')
    string_ = string_.replace('т', 't')
    string_ = string_.replace('г', 'r')
    string_ = string_.replace('į', 'i')
    string_ = string_.replace('ď', 'd')
    string_ = string_.replace('ǐ', 'i')
    string_ = string_.replace('ϋ', 'u')
    string_ = string_.replace('ṅ', 'n')
    string_ = string_.replace('в', 'b')
    string_ = string_.replace('ї', 'i')
    string_ = string_.replace('ι', 'l')
    string_ = string_.replace('ē', 'e')
    string_ = string_.replace('ọ', 'o')
    string_ = string_.replace('ņ', 'n')
    string_ = string_.replace('ộ', 'o')
    string_ = string_.replace('ậ', 'a')
    string_ = string_.replace('ű', 'u')
    string_ = string_.replace('υ', 'u')
    string_ = string_.replace('i', 'i')
    string_ = string_.replace('ḿ', 'm')
    string_ = string_.replace('ả', 'a')
    string_ = string_.replace('ẑ', 'z')
    string_ = string_.replace('ȧ', 'a')
    string_ = string_.replace('ĕ', 'e')
    string_ = string_.replace('ṡ', 's')
    string_ = string_.replace('ė', 'e')
    string_ = string_.replace('ό', 'o')
    string_ = string_.replace('ệ', 'e')
    string_ = string_.replace('ŕ', 'r')
    string_ = string_.replace('ċ', 'c')
    string_ = string_.replace('ķ', 'k')
    string_ = string_.replace('ⅳ', '4')
    string_ = string_.replace('ő', 'o')
    string_ = string_.replace('ŭ', 'u')
    string_ = string_.replace('о', 'o')
    string_ = string_.replace('ŝ', 's')
    string_ = string_.replace('ļ', 'l')
    string_ = string_.replace('ṣ', 's')
    string_ = string_.replace('²', '2')
    string_ = string_.replace('κ', 'k')
    string_ = string_.replace('ĝ', 'g')
    string_ = string_.replace('κ', 'k')
    string_ = string_.replace('ỹ', 'y')
    string_ = string_.replace('ĭ', 'i')
    string_ = string_.replace('ț', 't')
    string_ = string_.replace('ĉ', 'c')
    string_ = string_.replace('ĺ', 'l')
    string_ = string_.replace('ạ', 'a')
    string_ = string_.replace('ȉ', 'i')
    string_ = string_.replace('ь', 'b')
    string_ = string_.replace('ồ', 'o')
    string_ = string_.replace('ů', 'u')
    string_ = string_.replace('ù', 'u')
    string_ = string_.replace('ủ', 'u')
    string_ = string_.replace('ṕ', 'p')
    string_ = string_.replace('②', '2')
    string_ = string_.replace('ẗ', 't')
    string_ = string_.replace('ǹ', 'n')

    string_ = string_.replace('˘', '')
    string_ = string_.replace('´', '')
    string_ = string_.replace('‘', '')
    string_ = string_.replace('®', 'o')
    string_ = string_.replace('˝', '')
    string_ = string_.replace('¨', '')
    string_ = string_.replace('¹', '')
    string_ = string_.replace('?', '')
    string_ = string_.replace('�', '')
    string_ = string_.replace('.', '')
    string_ = string_.replace('\\', '')
    string_ = string_.replace('\"', '')
    string_ = string_.replace('-', ' ')
    string_ = string_.replace('\'', '')
    string_ = string_.replace("~", "") # 24
    string_ = string_.replace("`", "") # 24
    string_ = string_.replace("|", "e") # 24
    string_ = string_.replace("_", "") # 24
    string_ = string_.replace("\\", "") # ??
    string_ = string_.replace(" \(\w+\)", "") # ??
    string_ = string_.replace(" \([a-z]+ [a-z]+\)", "") # ??
    string_ = string_.replace(" \([a-z]+ [a-z]+ [a-z]+ [a-z]+\)", "") # ??
    string_ = string_.replace("   ", "") # 35
    string_ = string_.replace("  ", " ") # 67
    string_ = string_.replace("'", "") #1258
    string_ = string_.replace("-", " ") # 15748
    string_ = string_.replace("+", " ") # 15748
    string_ = string_.replace(";", " ") # 15748
    string_ = string_.replace("\. ", " ") # 115748
    string_ = string_.replace("\.", " ") # 5281
    string_ = string_.replace("\?", " ") # 5281

    return string_


def replace_sim(string):
    string_ = string.replace('univ.', 'university')
    string_ = string_.replace('dept.', 'department')
    string_ = string_.replace('eng.', 'engineering')
    string_ = string_.replace('sci.', 'science')
    string_ = string_.replace('comput.', 'science')
    string_ = string_.replace('electr.', 'electrical')
    string_ = string_.replace('inst.', 'institute')
    string_ = string_.replace('tech.', 'technology')
    string_ = string_.replace('technol.', 'technology')
    string_ = string_.replace('lab.', 'laboratory')
    string_ = string_.replace('inf.', 'information')
    string_ = string_.replace('centre', 'center')
    string_ = string_.replace('sch.', 'school')
    string_ = string_.replace('res.', 'research')

    return string_


def multiprocess_str(data, col, n_jobs=N_JOBS):

    def process(df):
        return df[col].apply(lambda x: replace_chr(replace_sim(x))).values

    processed_str = Parallel(n_jobs=n_jobs)(delayed(process)(d) for d in tqdm(data))
    return np.hstack(processed_str)
