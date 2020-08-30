import os
from utils import read_csv, multiprocess, split_data
from config import DATA_PATH
from temp import aff2country, aff2city


def process(df, orgs_col):
    df['affiliation'] = df[orgs_col].apply(lambda s: s.split(';')[0] if s else None)
    df['city'] = df['affiliation'].apply(aff2city)
    df['country'] = df['affiliation'].apply(aff2country)
    return df


if __name__ == '__main__':
    dblp_paper_df = read_csv(DATA_PATH, 'dblp_paper.csv')
    # asn_paper_df = read_csv(DATA_PATH, 'asn_paper.csv')
    author_df = read_csv(DATA_PATH, 'author.csv')
    # coauthor_df = read_csv(DATA_PATH, 'coauthor.csv')

    # PROCESSED DBLP PAPER DATAFRAME, DROPPED AUTHOR ORG, CALCULATE CITY & COUNTRY
    processed_paper_df = dblp_paper_df.dropna(subset=['authors_org']).copy().reset_index(drop=True)
    processed_dblp_paper_df = multiprocess(lambda df: process(df, orgs_col='authors_org'),
                                           split_data(processed_paper_df, size=1000), n_jobs=12)
    processed_dblp_paper_df.to_csv(os.path.join(DATA_PATH, 'processed_dblp_paper.csv'), index=False)

    # PROCESSED AUHTOR DATAFRAME, DROPPED AFFILIATIONS, CALCULATE CITY & COUNTRY
    processed_author_df_ = author_df.dropna(subset=['affiliations']).copy().reset_index(drop=True)
    processed_author_df = multiprocess(lambda df: process(df, orgs_col='affiliations'),
                                       split_data(processed_author_df_, size=1000), n_jobs=12)
    processed_author_df.to_csv(os.path.join(DATA_PATH, 'processed_author.csv'), index=False)
