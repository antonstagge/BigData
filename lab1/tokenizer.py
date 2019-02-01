import re
import string


re_tok = re.compile(r"([!\"#$%&'()*+,\-./:;<=>?@[\]^_`{|}~“”¨«»®´·º½¾¿¡§£₤‘’])")

def tokenize(text):
    """ Remove any type of punctuation
    and then split on whitespace
    """
    return re_tok.sub(' ',text).split()

if __name__ == '__main__':
    # for testing
    test = "Before I begin I'd just like point out that I am not reviewing this film as a work of \"\"art\"\" -- on that score, it seems just as good as most films, if not at least a little better -- but as a work of propaganda."
    print(test)
    print(tokenize(test))