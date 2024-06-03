import time
import pandas as pd

from pyjedai.evaluation import Evaluation
from pyjedai.datamodel import Data
from pyjedai.vector_based_blocking import EmbeddingsNNBlockBuilding
from pyjedai.clustering import ConnectedComponentsClustering, UniqueMappingClustering

# hide warnings
import warnings
warnings.filterwarnings('ignore')

from pyjedai.utils import (
    text_cleaning_method,
    print_clusters,
    print_blocks,
    print_candidate_pairs
)

def print_pairs(pairs, d1, d2, df1name, df2name):
    print(pairs)

    for _, (id1,id2) in pairs.iterrows():
        print("--------------------")
        print(df1name+" Product")
        a = d1[d1['id'] == str(id1)]
        print("\tTitle: ", a['Title'].values[0])
        print("\tPrice: ", a['Price'].values[0])
        # print("\tLink: ", a['Link'].values[0])
        print("-- compared to --")
        print(df2name+" Product")
        e = d2[d2['id'] == str(id2)]
        print("\tTitle: ", e['Title'].values[0])
        print("\tPrice: ", e['Price'].values[0])
        # print("\tLink: ", e['Link'].values[0])
        print("--------------------\n\n")


import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--d1', type=str, help='df1name')
parser.add_argument('--d2', type=str, help='df2name')
args = parser.parse_args()

df1name = args.d1
df2name = args.d2

d1 = pd.read_csv(df1name)
d2 = pd.read_csv(df2name)

d1 = d1.astype(str)
d2 = d2.astype(str)
data = Data(dataset_1=d1,
            attributes_1=['Title'],
            id_column_name_1='id',
            dataset_name_1=df1name,
            dataset_2=d2,
            attributes_2=['Title'],
            id_column_name_2='id',
            dataset_name_2=df2name)
data.print_specs()

emb = EmbeddingsNNBlockBuilding(vectorizer='word2vec',
                            similarity_search='faiss')

blocks, g = emb.build_blocks(data,
                            top_k=50,
                            similarity_distance='euclidean',
                            load_embeddings_if_exist=False,
                            save_embeddings=False,
                            with_entity_matching=True)

# emb.evaluate(blocks, with_classification_report=True, with_stats=True)
# print_candidate_pairs(blocks)

ccc = UniqueMappingClustering()
clusters = ccc.process(g, data, similarity_threshold=0.75)

pairs = ccc.export_to_df(clusters)

print("Pairs: ", len(pairs))
print_pairs(pairs, d1, d2, df1name, df2name)