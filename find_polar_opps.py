"""
find_polar_opps.py

Discovers the most negative and most positive review in a set of product reviews.

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


def get_vader_scores(title, content):
    """
    Returns overall VADER sentiment scores given a review composed of 
    a title and content.
    """
    title_scores = VADER.polarity_scores(title)
    
    # Filter out non-unicode or non-printable characters
    filtered_content = filter(lambda x: x in string.printable, content)

    pos_sent_scores = [title_scores['pos']]
    neg_sent_scores = [title_scores['neg']]
    neu_sent_scores = [title_scores['neu']]
    review_sents = sent_tokenize(filtered_content)
    for sent in review_sents:
        sent_score = VADER.polarity_scores(sent)
        pos_sent_scores.append(sent_score['pos'])
        neg_sent_scores.append(sent_score['neg'])
        neu_sent_scores.append(sent_score['neu'])

    return [np.mean(pos_sent_scores), np.mean(neg_sent_scores), np.mean(neu_sent_scores)]



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
    most_neg = [-1, "", ""]
    most_pos = [-1, "", ""]
    most_neu = [-1, "", ""]
    for productID in json_dict:
        entry = json_dict[productID]
        for review in entry['Reviews']:
            if review['Content'] is not None and review['Overall'] is not None:
                scores = get_vader_scores(review['Title'], review['Content'])

                if(scores[0] >= most_pos[0]):
                    most_pos = [scores[0], review['Title'], review['Content']]

                if(scores[1] >= most_neg[0]):
                    most_neg = [scores[1], review['Title'], review['Content']]

                if(scores[2] >= most_neu[0]):
                    most_neu = [scores[2], review['Title'], review['Content']]

        # If scores have been maxed out
        if(most_pos[0] == 1 and most_neu[0] == 1 and most_neg[0] == 1):
            break

    print 'Success!'

    # Write results

    # Filter out non-unicode or non-printable characters
    most_pos[2] = filter(lambda x: x in string.printable, most_pos[2])
    most_neg[2] = filter(lambda x: x in string.printable, most_neg[2])
    most_neu[2] = filter(lambda x: x in string.printable, most_neu[2])

    most_pos[1] = filter(lambda x: x in string.printable, most_pos[1])
    most_neg[1] = filter(lambda x: x in string.printable, most_neg[1])
    most_neu[1] = filter(lambda x: x in string.printable, most_neu[1])

    print "Writing most_pos file...",
    file_data = str(most_pos[0]) + ',' + str(most_pos[1]) + ',' + (most_pos[2])
    out_file = open('most_pos.csv', 'w')
    out_file.write(file_data)
    out_file.close()
    print "Success!"

    print "Writing most_neg file...",
    file_data = str(most_neg[0]) + ',' + str(most_neg[1]) + ',' + (most_neg[2])
    out_file = open('most_neg.csv', 'w')
    out_file.write(file_data)
    out_file.close()
    print "Success!"

    print "Writing most_neu file...",
    file_data = str(most_neu[0]) + ',' + str(most_neu[1]) + ',' + (most_neu[2])
    out_file = open('most_neu.csv', 'w')
    out_file.write(file_data)
    out_file.close()
    print "Success!"


if __name__ == '__main__':
    main()
