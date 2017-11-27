"""
sent_rate_compare.py

Runs experiment to calculate average sentiment score versus average rating.

@author: Brody Kutt (bjk4704@rit.edu)
"""

import os, sys
import json
import string

from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import sent_tokenize

import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

VADER = SentimentIntensityAnalyzer()
USAGE = """
    HOW TO RUN:

        python sent_rate_compare.py {1}

    WHERE:

        {1} = Path to JSON file containing review data.
        """


def get_vader_score(title, content):
    """
    Returns an overall VADER sentiment score given a review composed of 
    a title and content.
    """
    title_scores = VADER.polarity_scores(title)
    title_score = title_scores['compound']
    
    # Filter out non-unicode or non-printable characters
    filtered_content = filter(lambda x: x in string.printable, content)

    review_sents = sent_tokenize(filtered_content)
    sent_scores = []
    for sent in review_sents:
        sent_score = VADER.polarity_scores(sent)
        sent_scores.append(sent_score['compound'])

    sent_scores.append(title_score)
    return np.mean(sent_scores)


def normalize(l):
    """
    Normalizes list to have min 0 and max 1. Returns numpy array.
    """
    l = np.array(l, dtype='float64')
    l = l - np.min(l)
    l = l / np.max(l)
    return l


def quantize(l):
    """
    Quantizes a numpy array to 5 bins
    """
    bins = np.linspace(np.min(l), np.max(l), 5)
    quant_l = np.digitize(l, bins)
    quant_norm_l = normalize(quant_l)
    return quant_norm_l


def main():

    if(len(sys.argv) != 2):
        print(USAGE)
        sys.exit(1)

    f_path = sys.argv[1]

    # Read JSON file
    print "\nReading file...",
    json_file = open(f_path, 'r')
    json_text = json_file.read()
    json_dict = json.loads(json_text)
    print 'Success!'

    # Iterate through each product entry
    print 'Analyzing reviews...',
    all_vader = []
    all_ratings = []
    for productID in json_dict:
        entry = json_dict[productID]
        for review in entry['Reviews']:
            if review['Content'] is not None and review['Overall'] is not None:
                all_ratings.append(review['Overall'])
                all_vader.append(get_vader_score(review['Title'], 
                    review['Content']))
    print 'Success!'

    # Normalize all results to be between 0 and 1
    print 'Normalizing scores...',
    all_ratings = normalize(all_ratings)
    all_vader = normalize(all_vader)
    print 'Success!'

    # Plot results
    print 'Generating plots...',
    vader_quantized = quantize(all_vader)
    vader_quant_normal = normalize(vader_quantized)

    # Histogram of the ratings data
    plt.figure(figsize=(8, 6))
    n, bins, patches = plt.hist(all_ratings, 5, rwidth=0.85, facecolor='green')
    plt.xlabel('Rating Score')
    plt.ylabel('Frequency')
    plt.title(r'Histogram of Normalized Ratings')
    plt.grid(True)
    plt.savefig('ratings_hist.png')

    # Histogram of the VADER data
    plt.figure(figsize=(8, 6))
    n, bins, patches = plt.hist(all_vader, 25, rwidth=0.85, facecolor='green')
    plt.xlabel('VADER Compound Sentiment Score')
    plt.ylabel('Frequency')
    plt.title(r'Histogram of Normalized VADER Compound Sentiment Score')
    plt.grid(True)
    plt.savefig('vader_hist.png')

    # Histogram of the quantized VADER data
    plt.figure(figsize=(8, 6))
    n, bins, patches = plt.hist(vader_quant_normal, 5, rwidth=0.85, facecolor='green')
    plt.xlabel('Binned VADER Compound Sentiment Score')
    plt.ylabel('Frequency')
    plt.title(r'Histogram of Quantized & Normalized VADER Compound Sentiment Score')
    plt.grid(True)
    plt.savefig('quant_vader_hist.png')

    # Histogram of differences
    all_diff = sorted(np.absolute(all_ratings - vader_quant_normal))
    plt.figure(figsize=(8, 6))
    n, bins, patches = plt.hist(all_diff, 5, rwidth=0.85, facecolor='green')
    plt.xlabel('Absolute Magnitude of Difference')
    plt.ylabel('Frequency')
    plt.title(r'Histogram of Differences')
    plt.grid(True)
    plt.savefig('diff_hist.png')
    print 'Success!'


if __name__ == '__main__':
    main()
