import pandas as pd
import json

import os
from utils import strprocess, multiprocess, split_data
from config import DATA_PATH

author_prefix_lst = ['#index', '#n', '#a', '#pc', '#cn', '#hi', '#pi', '#upi']
author_cols = ['author_id', 'author_name', 'affiliations', 'published count', 'citation num',
               'H-index', 'P-index of equal A', 'P-index of unequal A']

paper_prefix_lst = ['#index', '#*', '#@', '#t', '#c', '#%']  # , '#!'
paper_cols = ['id', 'title', 'authors_name', 'year', 'venue_name', 'references']  # , 'abstract'

JSON_KEYWORDS = ['id', 'authors', 'venue', 'year', 'keywords',
                 'references', 'n_citation', 'doc_type', 'fos']
JSON_COLUMNS = ['id', 'author_id', 'author_org', 'venue_id', ' venue_name',
                'year', 'keywords', 'references', 'n_cites', 'doc_type', 'fos_name', 'fos_weight']

""" JSON keywords mapping

Field name in JSON -- Processed key(columns) in Dataframe/SQL
JSON file at https://originalstatic.aminer.cn/misc/dblp.v12.7z.
For more information, reference http://aminer.cn/citation. (dblp v12)

id          - id
authors     - authors_id
            - authors_name
            - authors_org
venue       - venue_id
            - venue_name
year        - year
keywords    - keywords
references  - references
n_citation  - n_cites
doc_type    - doc_type
"""


def parsetxt2df(file, prefix_lst, columns):
    """ Parse & convert txt into Dataframe.

    Args:
        -- file: txt file address, encoding in utf-8.
            paper data: https://lfs.aminer.cn/lab-datasets/aminerdataset/AMiner-Paper.rar
            author data: https://lfs.aminer.cn/lab-datasets/aminerdataset/AMiner-Author.zip
        -- prefix_lst: prefix list, prefix indicates data type of lines.
        -- columns: column list, Dataframe columns, in same shape as prefix_lst.

    Return:
        Converted Dataframe, needs further process.

    ETA
        - 2min for author data
        - 15min for paper data
    """
    with open(file, encoding='utf-8') as f:
        data = f.readlines()
    # WE HAVE TO FILTER OUT EVERY ROW WITHOUT OCCURRENCE OF REQUIRED PREFIX SO THAT COLUMN LENGTH CAN MATCH
    data = [d for d in data if any(d.startswith(p) for p in prefix_lst)]

    def process(d):
        def parse(prefix):
            if prefix == '#%':
                processed_lst = list()
                for l in d:
                    if l.startswith('#index'):
                        processed_lst.append(list())
                    elif l.startswith('#%'):
                        processed_lst[-1].append(strprocess(l, '#%'))

                return [';'.join(lst) for lst in processed_lst]
            else:
                return [strprocess(s, prefix) for s in d if s.startswith(prefix)]
        return pd.DataFrame({col: parse(prefix) for col, prefix in zip(columns, prefix_lst)})

    size = 100000
    if '#%' in prefix_lst:
        return process(data)
    processed_df = multiprocess(process, split_data(data, size=size))
    return processed_df


def parsejson2df(file, col_lst=JSON_KEYWORDS):
    """ Parse & load json file to Dataframe.

    Data at https://originalstatic.aminer.cn/misc/dblp.v12.7z
    ** THIS FILE IS PRETTY LARGE (12GB when unzipped), the file is loaded by readline,
    HOWEVER THE JSON DATA IS CONVERTED TO A SINGLE DATAFRAME, MAY REQUIRE LARGE MEMORY.

    ETA 30min
    """

    def parse(js):
        processed_line = dict()
        for col in set(col_lst).intersection(set(js.keys())):
            # Only keywords in the list above are considered
            # If more keywords are required, according read_in code should be added
            if col == 'id':
                processed_line['id'] = js['id']
            elif col == 'authors':
                authors = js['authors']
                processed_line['authors_id'] = ';'.join([str(author.get('id', None))
                                                         for author in authors if author.get('id', None)])
                processed_line['authors_name'] = ';'.join([author.get('name', None)
                                                           for author in authors if author.get('name', None)])
                processed_line['authors_org'] = ';'.join([str(author.get('org', None))
                                                          for author in authors if author.get('org', None)])
            elif col == 'venue':
                venue = js['venue']
                processed_line['venue_id'] = venue.get('id', None)
                processed_line['venue_name'] = venue.get('raw', None)
            elif col == 'year':
                processed_line['year'] = js['year']
            elif col == 'keywords':
                processed_line['keywords'] = ';'.join(js['keywords'])
            elif col == 'references':
                processed_line['references'] = ';'.join([str(r) for r in js['references']])
            elif col == 'n_citation':
                processed_line['n_cites'] = js['n_citation']
            elif col == 'doc_type':
                processed_line['doc_type'] = js['doc_type']
            elif col == 'fos':
                fos = js['fos']
                processed_line['fos_name'] = ';'.join([str(f.get('name', None))
                                                       for f in fos if f.get('name', None)])
                processed_line['fos_weight'] = ';'.join([str(f.get('w', None))
                                                         for f in fos if f.get('w', None)])
        return processed_line

    with open(file, encoding='utf-8') as f:
        lines = f.readlines()

    def process(ls):
        df = pd.DataFrame()
        for line in ls:
            line = line.lstrip('[')
            line = line.lstrip(',')
            line = line.rstrip(']')
            line = line.rstrip('\n')
            js = json.loads(line)
            df = df.append(parse(js), ignore_index=True)
        return df

    parsed_df = multiprocess(process, split_data(lines[1: -1], size=2000))

    # Change data type
    parsed_df['id'] = parsed_df['id'].astype('int64')
    parsed_df['year'] = parsed_df['year'].astype('int')
    parsed_df['n_cites'] = parsed_df['n_cites'].astype('int')

    return parsed_df


def parse_coauthor(file):
    """ Parse & convert coauthor into Dataframe.

        Args:
            -- file: coauthor file address, encoding in utf-8.
                coauthor file: https://lfs.aminer.cn/lab-datasets/aminerdataset/AMiner-Coauthor.zip

        ETA 10min
        """
    with open(file, encoding='utf-8') as f:
        data = f.readlines()

    def process(d):
        df = pd.DataFrame(columns=['1st', '2nd', 'num'])
        for c in d:
            c = c.lstrip('#')
            c = c.rstrip('\n')
            df = df.append({col: val for col, val in zip(df.columns, c.split('\t'))}, ignore_index=True)
        return df

    coauthor_df = multiprocess(process, split_data(data, size=2000))
    coauthor_df['num'] = coauthor_df['num'].astype('int64')
    return coauthor_df


if __name__ == '__main__':
    dblp_paper_df = parsejson2df(os.path.join(DATA_PATH, 'dblp.v12.json'), col_lst=JSON_KEYWORDS)
    # asn_paper_df = parsetxt2df(os.path.join(DATA_PATH, 'AMiner-Paper.txt'), paper_prefix_lst, paper_cols)
    # author_df = parsetxt2df(os.path.join(DATA_PATH, 'AMiner-Author.txt'), author_prefix_lst, author_cols)
    # coauthor_df = parse_coauthor(os.path.join(DATA_PATH, 'AMiner-Coauthor.txt'))

    dblp_paper_df.to_csv(os.path.join(DATA_PATH, 'dblp_paper.csv'), index=False)
    # asn_paper_df.to_csv(os.path.join(DATA_PATH, 'asn_paper.csv'), index=False)
    # author_df.to_csv(os.path.join(DATA_PATH, 'author.csv'), index=False)
    # coauthor_df.to_csv(os.path.join(DATA_PATH, 'coauthor.csv'), index=False)
