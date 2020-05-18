import numpy as np
import pandas as pd
from nltk.corpus import stopwords
from nltk import download
from nltk import word_tokenize

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

class EdgeWordNgarmTfidfVectorizer(TfidfVectorizer):
    def __init__(self, edge_ngrams_range, **kwargs):
        super().__init__(**kwargs)
        self.edge_ngrams_range = edge_ngrams_range
            
    
    def _word_ngrams(self, tokens, stop_words=None):
        # First get tokens without stop words       
        tokens = super()._word_ngrams(tokens, None)        
       
        space_join = " ".join
        ln = len(tokens)-1
        new_tokens=[]
        for i in range(ln):              
            new_tokens.append(space_join(tokens[:-ln+i]))            
        new_tokens.append(space_join(tokens))
       
        return new_tokens

def preprocess(doc):
    doc = doc.lower()  # Lower the text.
    doc = word_tokenize(doc)  # Split into words.
    #doc = [w for w in doc if not w in stop_words]  # Remove stopwords.
    doc = [w for w in doc if w.isalpha()]  # Remove numbers and punctuation.
    return doc

def get_clean_text(list_strings):
    clean_text = []
    space_join = ' '.join
    for s in list_strings:
        clean_text.append(space_join(preprocess(s)))
    return clean_text


def similarity_rank(query, vectorizer, text_list):
    q_text = ' '.join(preprocess(q))
    q_vz = vectorizer.transform([' '.join(preprocess(q))])
    cosine_similarities = linear_kernel(q_vz, vz).flatten()
    related_docs_indices = cosine_similarities.argsort()[:-5:-1]
    for idx in related_docs_indices:
        print(f'{text_list[idx]}, \t  {cosine_similarities[idx]}')


if __name__=='__main__':
  
    names = ['DHL', 	  
            'DHL', 	  
            'DHL DANZAS', 	
            'DHL DANZAS', 	  
            'DHL  FORWARDING', 	 
            'DHL GLOBAL FORWARDING', 	  
            'DHL GLOBAL FORWARDING',
            'AGILITY LOGISTICS', 	  
            'AGILITY LOGISTICS',
            'ADVANCED CARGO', 	  
            'ADVANCED CARGO TRANSPORTATION', 	  
            'ADVANCED ENGINEERING', 	  
            'ADVANCED SEED']
    clean_text = get_clean_text(names)
    for s in clean_text:
        print(s)
    vectorizer = EdgeWordNgarmTfidfVectorizer(edge_ngrams_range=(1,2), token_pattern=r'\S+')
    vz = vectorizer.fit_transform(clean_text)
    print()
    print(vz.shape)
    print(vectorizer.get_feature_names())

    print("****************")
    q = 'DHL'
    similarity_rank(q, vectorizer, clean_text)

    print("****************")
    q = 'DHL GLOBAL'
    similarity_rank(q, vectorizer, clean_text)

    print("****************")
    q = 'ADVANCED CARGO'
    similarity_rank(q, vectorizer, clean_text)