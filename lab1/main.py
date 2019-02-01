from sklearn.feature_extraction.text import CountVectorizer
from tokenizer import tokenize
import numpy as np

# not used: 
# pattern = re.compile(',\"(?!\")|(?<!\")\",') # look for ," for start and ", for end but dont include "" for quotes within the review

def read_data(file):
    """ Convert file data to x and y vectors
    split each line into (first, text, score)
    x_vector - the vector of texts
    y_vector - the vector of scores
    """
    training_file = open(file, mode='r', encoding='utf-8')
    training_file.readline()
    x_vector = []
    y_vector = []
    for line in training_file:
        arr = line.split(',')
        first = arr[0]
        text = ','.join(arr[1:-1])
        score = arr[-1]
        score = float(score)
        x_vector.append(text.lower())
        y_vector.append(score)
    return x_vector, y_vector

def main():
    x_train, y_train = read_data('lab_train.txt')
    x_test, y_test = read_data('lab_test.txt')

    vect = CountVectorizer(tokenizer=tokenize)
    # create a matrix with rows as texts and columns as tokens,
    # each cell containst the number of times the token appears in the text
    tf_train = vect.fit_transform(x_train)

if __name__ == '__main__':
    main()