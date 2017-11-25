"""
sentiment_score.py

Contains functionality to return the overall sentiment of
arbitrarily long segments of text. Uses NLTK.

@author: Brody Kutt (bjk4704@rit.edu)
"""

from nltk import tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA

analyser = SIA()

def print_sentiment_scores(sentence):
    ans = analyser.polarity_scores(sentence)
    for t in ans:
        print "%s: %0.2f" % (t, ans[t])

def main():
    sentence = "I woke up early this morning and I feel very refreshed! :)"
    print_sentiment_scores(sentence)

main()