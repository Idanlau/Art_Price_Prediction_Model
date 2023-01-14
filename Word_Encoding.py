import string
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import nltk

nltk.download("stopwords")

from nltk.corpus import stopwords

stopword = stopwords.words('english')


def clean_string(text):
    text = ''.join([word.replace('_', ' ') for word in text if word not in string.punctuation or word == '_'])
    text = text.lower()
    text = ' '.join([word for word in text.split() if word not in stopword])
    return text


def cosine_sim_vectors(v1, v2):
    v1 = v1.reshape(1, -1)
    v2 = v2.reshape(1, -1)
    return cosine_similarity(v1, v2)[0][0]


def retrieve_key(text1, text2):
    text1 = clean_string(text1)
    text2 = clean_string(text2)
    vector = CountVectorizer().fit_transform([text1, text2])
    raw_vector = vector.toarray()
    return raw_vector
    # Compares similarity between vectors by calculating cosine distance
    """
    score_max=0.9
    ind=-1
    for i in range(len(vector)-1):
        score = cosine_sim_vectors(vector[0], vector[i+1])
        if score>score_max:
            score_max=score
            ind=i
    if ind==-1:
        responds=False
    else:
        responds=List[ind]
    return responds
    """


print(retrieve_key("The signature is on lower-right", "Signed on lower-left corner"))
