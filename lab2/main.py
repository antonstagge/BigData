from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix
from sklearn.metrics import roc_auc_score
from sklearn.feature_extraction.text import CountVectorizer
from bag_vectorizer import BagVectorizer
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
            y_vector.append(0)
    return x_vector, y_vector

def read_data(file):
    """ Read data from an xlsx file
    """
    workbook = load_workbook(file, data_only=True)
    worksheet = workbook.active
    first_colum = worksheet['A']

    x_vector = []
    for x in range(len(first_colum)):
        x_vector.append(first_colum[x].value)

    return x_vector



def train_model(x_train, y_train, bag_vectorizer):
    """ Train the model
    """
    # create a matrix with rows as texts and columns as tokens,
    # each cell containst the number of times the token appears in the text
    x_train_fit = bag_vectorizer.fit_transform()
    
    classifier = MultinomialNB()
    classifier.fit(x_train_fit, y_train)

    return classifier

def test_model(classifier, bag_vectorizer, x_test, y_test):
    """ Test the model accuracy by counting the 
    number of wrong predictions. Also prints the
    confusion matrix. 
    """
    x_test_fit = bag_vectorizer.transform(x_test)
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
    x_train, y_train = read_training_data('lab_train.txt')
    x_test, y_test = read_training_data('lab_test.txt')
    x_eval = read_data('evaluation_dataset.xlsx')

    # models = []
    # for bag_size in range(1,4):
    #     for num_words in range(9,12):
    #         bag_vectorizer = BagVectorizer(num_words, num_words, bag_size, x_train)
    #         classifier = train_model(x_train, y_train, bag_vectorizer)
    #         models.append((classifier, bag_vectorizer))

    # for classifier, bag_vectorizer in models:
    #     print("MODEL WITH BAG SIZE: %d and WORDS %d:" % (bag_vectorizer.bag_size, bag_vectorizer.n_common_words))
    #     test_model(classifier, bag_vectorizer, x_test, y_test)
    #     print()

    bag_vectorizer_eval = BagVectorizer(10, 10, 2, x_train)
    classifier_eval = train_model(x_train, y_train, bag_vectorizer_eval)

    # Multinomial
    y_score = classifier_eval.predict_proba(bag_vectorizer_eval.transform(x_test))[:,1]

    # y_score = classifier_eval.decision_function(bag_vectorizer_eval.transform(x_test))
    auc = roc_auc_score(y_test, y_score)
    print("THE AREA UNDER ROC IS: %.3f" % auc)

    x_eval_fit = bag_vectorizer_eval.transform(x_eval)
    y_pred_eval = classifier_eval.predict(x_eval_fit)

    neg_count = (200 - sum(y_pred_eval))/2
    print("Postitive booking comments: %d \nNegative booking comments: %d " % (200-neg_count, neg_count))
    

    # print("\n\nFOR APPENDIX")
    # for i in range(len(y_pred)):
    #     print()
    #     print(("POSITIVE: ".encode('utf-8') if y_pred[i] == 1 else "NEGATIVE: ".encode('utf-8')) + x_eval[i].encode('utf-8'))



if __name__ == '__main__':
    main()