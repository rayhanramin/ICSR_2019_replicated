from sklearn.feature_extraction.text import TfidfVectorizer

# Example documents
documents = ["This is the first document.",
              "This document is the second document.",
              "And this is the third one.",
              "Is this the first document?"]

# Create the TfidfVectorizer
tfidf_vectorizer = TfidfVectorizer()

# Fit and transform the documents
tfidf_matrix = tfidf_vectorizer.fit_transform(documents)

# Get the feature names (terms)
feature_names = tfidf_vectorizer.get_feature_names_out()

# Print the TF-IDF matrix
print(tfidf_matrix.toarray())

# Print the feature names
print(feature_names)


