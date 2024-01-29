import numpy as np
import os
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt

with open(os.path.join(os.getcwd(), 'clean', 'clean-antivirus-features.txt')) as f:
    all_features = f.readlines()


cosine_sim_scores = []
new_requirements = []
cutoff = float(input("What is the cutoff similarity value for the newly generated requirements? "))

#[:500]
tfidf_vectorizer = TfidfVectorizer()
with open(os.path.join(os.getcwd(), 'requirement','antivirus-requirements.txt')) as f:
    for generated_feature in f.readlines()[:500]:
        appended_features = [generated_feature] + all_features
        #[generated_feature] + (should be added at the beginning of the previous line)
        tfidf_matrix = tfidf_vectorizer.fit_transform(appended_features)
        sim_scores = np.array(cosine_similarity(tfidf_matrix[0:1],tfidf_matrix))
        #print(cosine_similarity(tfidf_matrix[0:1],tfidf_matrix))
        #print(tfidf_matrix) 
        print(sim_scores)  
        all_less = np.all(sim_scores[1:] < cutoff)

        if all_less:   
            cosine_sim_scores.append(np.mean(cosine_similarity(tfidf_matrix[0:1], tfidf_matrix)))
            generated_feature = generated_feature.rstrip()
            new_requirements.append(generated_feature)


X = np.arange(len(cosine_sim_scores))

# fig,ax = plt.subplots(1)
#print(cosine_sim_scores)
#print(new_requirements)

req_and_sim_scores = list(zip(new_requirements,cosine_sim_scores))

df = pd.DataFrame(req_and_sim_scores, columns=['New Requirements','Similarity Scores'])

#print(df)
df = df.sort_values('Similarity Scores')
n = int(input("How many new requierments do you want to see?"))
pd.set_option('display.max_colwidth', None) 
print(df.head(n))

plt.figure(figsize=(8,4))
plt.bar(X, cosine_sim_scores, width=0.3, color='#4286f4')
plt.xlabel("generated requirement id")
plt.ylabel("cosine similarity td-idf score")
# plt.gca().axes.get_xaxis().set_visible(False)

cosine_sim_scores.sort()

plt.axhline(y=cosine_sim_scores[400], color='r', linestyle='-', linewidth=0.5)
plt.tight_layout()
plt.show()

print('Finished!')

