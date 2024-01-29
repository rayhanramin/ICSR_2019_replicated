'''
Generate new requirements
'''

from utils import tokenize, make_requirements
from cluster import cluster_requirements

import spacy
import pandas as pd
import numpy as np
import os
import math

nlp = spacy.load('en_core_web_sm')

# path
feature_paths = [os.path.join(os.getcwd(), 'clean', p) for p in ['clean-file-sharing-features.txt', 'clean-antivirus-features.txt', 'clean-browser-features.txt']]
model_file_paths = [os.path.join(os.getcwd(), 'model', m) for m in ['model_file_sharing', 'model_antivirus', 'model_browser']]
requirement_paths = [os.path.join(os.getcwd(), 'requirement', r) for r in ['file-sharing-requirements.txt', 'antivirus-requirements.txt', 'browser-requirements.txt']]

boilerplates = [os.path.join(os.getcwd(), 'boilerplate', b) for b in ['boilerplate-file-sharing.csv', 'boilerplate-antivirus.csv', 'boilerplate-browser.csv']]

cluster_fit = []
for model_path, feature_path, bl, requirement_path in zip(model_file_paths, feature_paths, boilerplates, requirement_paths):
    print('START GENERATING REQUIREMENTS FOR {}\n'.format(model_path))
    #features = tokenize(feature_path)
    
    init_cluster_size = 3
    while init_cluster_size < 10:
        cluster_arr, score = cluster_requirements(model_path, feature_path, init_cluster_size)
        
        #print(score)
        if score > 0.3:
            cluster_fit.append(init_cluster_size)
        init_cluster_size += 1
     
        
print(cluster_fit)

a = min(cluster_fit)
b = max(cluster_fit)


print(a,b)



NUM_CLUSTERS = 5

while True:
    NUM_CLUSTERS = int(input("Enter a value between {} and {} to set as cluster size. Press 0 to exit".format(a,b)))
    if NUM_CLUSTERS == 0:
        exit()
    elif NUM_CLUSTERS in range(a,b+1):
        for model_path, feature_path, bl, requirement_path in zip(model_file_paths, feature_paths, boilerplates, requirement_paths):
            print('START GENERATING REQUIREMENTS FOR {}\n'.format(model_path))
            features = tokenize(feature_path)

            cluster_arr, score = cluster_requirements(model_path, feature_path, NUM_CLUSTERS)
            # print(cluster_arr)

            df = pd.read_csv(os.path.join(os.getcwd(), 'boilerplate', bl), sep=',')
            # indexes[i] contains indices of all requirements belong to cluster (i+1)
            indices = [np.where(cluster_arr == i) for i in range(NUM_CLUSTERS)]
            # print(cluster_1)
            #print(indices[0])

            with open(requirement_path, 'w') as writer:
                # randomly pick 3 requirements from each cluster for 10 times to make 100 x 6 = 60 requirements
                for i in range(5):
                    cluster1,cluster2,cluster3 = np.random.choice(range(0,NUM_CLUSTERS),size= 3)
                    #print(cluster1,cluster2, cluster3)
                    for cl in range(NUM_CLUSTERS):
                        req_from_cluster_a = np.random.choice(indices[cluster1][0])
                        req_from_cluster_b = np.random.choice(indices[cluster2][0])
                        req_from_cluster_c = np.random.choice(indices[cluster3][0])
                        bl_1 = df[df.id == req_from_cluster_a].head(1)
                        bl_2 = df[df.id == req_from_cluster_b].head(1)
                        bl_3 = df[df.id == req_from_cluster_c].head(1)

                        print(bl_1,bl_2,bl_3)

                        requirements = make_requirements([bl_1, bl_2, bl_3])
                        writer.writelines('%s\n' % r for r in requirements)
                        
                    #for ind in indices:
                        #print(ind)
                        #triple = np.random.choice(ind[0], 3)
                        #bl_1 = df[df.id == triple[0]].head(1)
                        #bl_2 = df[df.id == triple[1]].head(1)
                        #bl_3 = df[df.id == triple[2]].head(1)
                        #print(bl_1,bl_2,bl_3)

                        #requirements = make_requirements([bl_1, bl_2, bl_3])
                        #writer.writelines('%s\n' % r for r in requirements)
            print('----------------END-----------------\n\n\n')
        exit()
    else:
        print("Invalid Input")







    # generate new requirements by swapping parts in pair files
    # generate 10 requirement x 10 times x total number of combination = 100 requirements
    # df = pd.read_csv(os.path.join(os.getcwd(), 'boilerplate', bl), sep=',')
    # print('START GENERATING REQUIREMENTS FOR {}\n'.format(model_path))
    # id = randint(0, len(features) - 1)
    # original = df[df.id == id]
    # vector = model.infer_vector(features[id])
    # print('selected feature = {}\n'.format(str(features[id])))
    # for (ix, matched_percentage) in model.docvecs.most_similar([vector]):
    #     similar = df[df.id == ix]
    #     # create two new requirements from combining each pair of similar requirements
    #     # print(original['verb'])
    #     # print(original['object'])
    #     # print(original['detail'])
    #     for _, row1 in original.iterrows():
    #         for _, row2 in similar.iterrows():
    #             print(BOILERPLATE.format(row1['verb'], row2['object'], row2['detail']))
    #             print(BOILERPLATE.format(row2['verb'], row1['object'], row1['detail']))
            # for v, s in zip(original[], similar):
            #     print(v, s)
            # print(ix, matched_percentage, features[ix])


# vector = model.infer_vector(features[0])
# for (ix, percentage) in model.docvecs.most_similar([vector]):
#     print(ix, features[ix])
#
#
# print('-------------------------')
#
# vector = model.infer_vector(features[1])
# for (ix, percentage) in model.docvecs.most_similar([vector]):
#     print(ix, features[ix])