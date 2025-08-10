# Importing The Libraries

import sys
import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from store.models import Product

def get_similar_products(product_pk: int):
    """
    Returns a list of top 6 similar Product objects based on text similarity.

    Args:
        product_pk (int): The pk of the product to find recommendations for.

    Returns:
        QuerySet: A queryset of similar Product instances.
    """

    # Fetch product data from the database
    products = Product.objects.all().values('pk', 'title', 'description')

    # Convert product data to DataFrame
    df = pd.DataFrame(list(products))

    # Combine title and description into one string per product
    df['features'] = df['title'] + " " + df['description']

    df['features'] = df['features'].fillna("")

    # Convert text to TF-IDF vectors
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(df['features'])

    # Checking if the given product_pk exists
    if product_pk not in df['pk'].values:
        return []

    # Finding index of the product
    idx = df[df['pk'] == product_pk].index[0]

    # Calculating cosine similarity of product_pk with all products
    similarity_score = cosine_similarity(tfidf_matrix[idx], tfidf_matrix)

    # Getting top 6 similar indices
    similar_indices = similarity_score.argsort()[0][-7:-1]

    #Getting top 6 similar Products
    similar_titles = df.iloc[similar_indices]['title'].tolist()

    return similar_titles

print(get_similar_products(6))
print(Product.objects.filter(pk = 6).values("title", "pk"))
