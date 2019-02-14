import numpy as np
import re
import string
from sklearn.feature_extraction.text import CountVectorizer

number_of_common_words = 10
common_words = []
punctuation_string = r"[!\"#$%&'()*+,\-./:;<=>?@[\]^_`{|}~“”¨«»®´·º½¾¿¡§£₤‘’]"


def set_common_words(x_train):
    """ Count the number of times each word appears and then
    place the top number_of_common_words in the 
    global variable common_words
    """
    vectorizer = CountVectorizer(tokenizer=simple_tokenizer)
    x_train_fit = vectorizer.fit_transform(x_train)
    
    words= vectorizer.get_feature_names()

    word_count = []
    for i in range(x_train_fit.shape[1]):
        count = np.sum(x_train_fit.getcol(i))
        tup = (count, words[i])
        word_count.append(tup)

    def comparator(tupEl):
        # sort on the count
        return tupEl[0]

    word_count.sort(key=comparator)
    for i in range(1,number_of_common_words):
        common_words.append(word_count[-i][1])


def simple_tokenizer(text):
    """ Remove any type of punctuation and the words 
    and then split on whitespace
    """
    re_tok = re.compile(punctuation_string)
    return re_tok.sub(' ', text).split()


def tokenize(text):
    """ Remove any type of punctuation and the words 
    contained in the global variable common_words
    and then split on whitespace
    """
    common_words_string = " | ".join(common_words)
    re_tok = re.compile(punctuation_string + "| " + common_words_string + " ")
    words = re_tok.sub(' ',re_tok.sub(' ',text)).split()

    tokens = []
    for i in range(len(words)-1):
        first = words[i]
        second = words[i+1]
        # third = words[i+2]
        tokens.append(' '.join([first, second]))
    return tokens

if __name__ == '__main__':
    # For testing
    test = "Before I begin I'd just like point out that I am not reviewing this film as a work of \"\"art\"\" -- on that score, it seems just as good as most films, if not at least a little better -- but as a work of propaganda."
    test = test.lower()
    print(test)
    print(tokenize(test))