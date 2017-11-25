
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sklearn.metrics import accuracy_score

vader = SentimentIntensityAnalyzer()


def vader_polarity(text):
    """ Transform the output to a binary 0/1 result """
    score = vader.polarity_scores(text)
    return 1 if score['pos'] > score['neg'] else 0


print vader_polarity(train_X[0]), train_y[0]  # 0 1
print vader_polarity(train_X[1]), train_y[1]  # 0 0
print vader_polarity(train_X[2]), train_y[2]  # 1 1
print vader_polarity(train_X[3]), train_y[3]  # 0 1
print vader_polarity(train_X[4]), train_y[4]  # 0 0

pred_y = [vader_polarity(text) for text in test_X]
print accuracy_score(test_y, pred_y)