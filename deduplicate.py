import os
import sys
import pandas as pd
import networkx
from networkx import draw, Graph

import pyjedai
from pyjedai.utils import (
    text_cleaning_method,
    print_clusters,
    print_blocks,
    print_candidate_pairs
)
from pyjedai.evaluation import Evaluation

from pyjedai.datamodel import Data
from pyjedai.evaluation import Evaluation
from pyjedai.block_building import (
    StandardBlocking,
    QGramsBlocking,
    ExtendedQGramsBlocking,
    SuffixArraysBlocking,
    ExtendedSuffixArraysBlocking,
)
from pyjedai.block_cleaning import BlockPurging
from pyjedai.block_cleaning import BlockFiltering
from pyjedai.comparison_cleaning import (
    WeightedEdgePruning,
    WeightedNodePruning,
    CardinalityEdgePruning,
    CardinalityNodePruning,
    BLAST,
    ReciprocalCardinalityNodePruning,
    ReciprocalWeightedNodePruning,
    ComparisonPropagation
)
from pyjedai.matching import EntityMatching
from pyjedai.clustering import ConnectedComponentsClustering, UniqueMappingClustering

# from pyjedai.utils import print_clusters, print_blocks, print_candidate_pairs

def print_pairs(pairs, d1, d2, df1name, df2name):
    print(pairs)

    for _, (id1,id2) in pairs.iterrows():
        print("--------------------")
        print(df1name+" Product")
        a = d1[d1['id'] == str(id1)]
        print("\tTitle: ", a['Title'].values[0])
        print("\tPrice: ", a['Price'].values[0])
        # print("\tLink: ", a['Link'].values[0])
        print("-- - --")
        print(df2name+" Product")
        e = d2[d2['id'] == str(id2)]
        print("\tTitle: ", e['Title'].values[0])
        print("\tPrice: ", e['Price'].values[0])
        # print("\tLink: ", e['Link'].values[0])        
        print("--------------------\n\n")
    
    name = df1name.split("/")[-1].split(".")[0]

    # make dir predictions
    dir = "predictions"
    if not os.path.exists(dir):
        os.makedirs(dir)

    # change column names

    # retailer is like ./amazon/gaming_laptop.csv_id
    ret1 = df1name.split("/")[-2]
    ret2 = df2name.split("/")[-2]
    
    pairs.columns = [ret1+'_id', ret2+'_id']
    

    pairs.to_csv(dir+"/"+name+"_duplicates.csv", index=False, header=True)
    print("Predictions saved in predictions/"+name+"_duplicates.csv")


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

bb = StandardBlocking()
blocks = bb.build_blocks(data)

# print_blocks(blocks, data.is_dirty_er)

bp = BlockPurging()
cleaned_blocks = bp.process(blocks, data, tqdm_disable=False)

bf = BlockFiltering(ratio=0.8)
filtered_blocks = bf.process(cleaned_blocks, data, tqdm_disable=False)

mb = WeightedEdgePruning(weighting_scheme='EJS')
candidate_pairs_blocks = mb.process(filtered_blocks, data, tqdm_disable=False)

# pairs_df=mb.export_to_df(candidate_pairs_blocks)

# print("Candidate Pairs: ", len(pairs_df))

# print_pairs(pairs_df.head(20), d1, d2)


em = EntityMatching(
    metric='cosine',
    tokenizer='char_tokenizer',
    vectorizer='tf',
    qgram=5,
    similarity_threshold=0.0
)

pairs_graph = em.predict(candidate_pairs_blocks, data, tqdm_disable=False)
em.plot_distribution_of_all_weights()

# draw(pairs_graph, with_labels=True)
# pairs = em.export_to_df(pairs_graph)

# print("Pairs: ", len(pairs))
# print_pairs(pairs, d1, d2)
# print graph size

print("Graph size: ", len(pairs_graph.nodes))
print("Graph edges: ", len(pairs_graph.edges))

avg = em.get_weights_avg()
std = em.get_weights_standard_deviation()
median = em.get_weights_median()

ccc = UniqueMappingClustering()
clusters = ccc.process(pairs_graph, data, similarity_threshold=avg)

pairs = ccc.export_to_df(clusters)

print("Pairs: ", len(pairs))
print_pairs(pairs, d1, d2, df1name, df2name)
