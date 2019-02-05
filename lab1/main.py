from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import confusion_matrix
from sklearn.feature_extraction.text import CountVectorizer
from tokenizer import tokenize
from openpyxl import load_workbook


def read_training_data(file):
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
        text = ','.join(arr[1:-1])
        score = arr[-1]
        score = float(score)
        x_vector.append(text.lower())
        if score > 3:
            y_vector.append(1)
        else:
            y_vector.append(-1)
    return x_vector, y_vector

def read_data(file):
    workbook = load_workbook(file, data_only=True)
    worksheet = workbook.active
    first_colum = worksheet['A']

    x_vector = []
    for x in range(len(first_colum)):
        x_vector.append(first_colum[x].value)

    return x_vector



def train_model():
    x_train, y_train = read_training_data('lab_train.txt')

    vectorizer = CountVectorizer(tokenizer=tokenize)
    # create a matrix with rows as texts and columns as tokens,
    # each cell containst the number of times the token appears in the text
    x_train_fit = vectorizer.fit_transform(x_train)
    
    classifier = MultinomialNB()
    classifier.fit(x_train_fit, y_train)

    return classifier, vectorizer

def test_model(classifier, vectorizer):
    x_test, y_test = read_training_data('lab_test.txt')
    x_test_fit = vectorizer.transform(x_test)
    y_pred = classifier.predict(x_test_fit)

    error = 0.0
    for i in range(len(y_pred)):
        if y_pred[i] != y_test[i]:
            error += 1
    print("The model accuracy was: %.3f" % (1 - error/100))

    confusion = confusion_matrix(y_test, y_pred)
    print("pred-actual \n[[neg-neg pos-neg]\n[neg-pos pos-pos]]")
    print(confusion)
        

def main():
    classifier, vectorizer = train_model()
    test_model(classifier, vectorizer)
    x_eval = read_data('evaluation_dataset.xlsx')
    x_eval_fit = vectorizer.transform(x_eval)
    y_pred = classifier.predict(x_eval_fit)

    neg_count = (200 - sum(y_pred))/2
    print("Postitive booking comments: %d \nNegative booking comments: %d " % (200-neg_count, neg_count))
    

    print("\n\nFOR APPENDIX")
    for i in range(len(y_pred)):
        print()
        print(("POSITIVE: ".encode('utf-8') if y_pred[i] == 1 else "NEGATIVE: ".encode('utf-8')) + x_eval[i].encode('utf-8'))



if __name__ == '__main__':
    main()