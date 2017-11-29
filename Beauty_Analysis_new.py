
'''
Analyzing Beauty dataset for sentiment
'''

import pandas as pd
import gzip
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA

analyser = SIA()


def parse(path):
    '''
    Extract values from FILE which is in JSON format
    :param path: path to the file
    :return: None
    '''
    g = gzip.open(path, 'rb')
    for l in g:
        yield eval(l)

def getDF(path):
    '''
    Creates a dataframe from original dataset and integrates all the reviews in one DF
    :param path:
    :return: dataframe df
    '''
    i = 0
    df = {}
    count=0;       #uncomment to limit the number of reviews
    for d in parse(path):
        if count<1500 :           #uncomment to limit the number of reviews
            df[i] = d
            i += 1
            count+=1
        else:                  #uncomment to limit the number of reviews
            break

    return pd.DataFrame.from_dict(df, orient='index')

def getDict(path):
    '''
    Returns dictionary of product id and product title from metadata
    :param path:
    :return: dictionary with title and price.
    '''
    i = 0
    prdt_dict = []
    #delete unwanted columns
    keys=['description','imUrl','salesRank','categories','related','brand','bought_together']

    for d in parse(path):

        for k in keys:
            if k in d:
                del d[k]            #DELETE     unwanted columns

            prdt_dict.append(d)


    return prdt_dict

def print_sentiment_scores(sentence):
    '''
    calculate the sentiment of each sentence
    :param sentence:
    :return: sentiment_score
    '''
    ans = analyser.polarity_scores(sentence)
    return ans['compound']


def main():

    #****IF YOU WANT TO RUN THIS PROGRAM CHANGE download_dir****#
    #there is no limit both the dataset and metadata will be completely read
    print('Loading , please wait....')

    #changed name of storage file to avoid override
    #original data is in prdtReview.csv with 17k reviews
    download_dir = "prdtReview1.csv"  # where you want the file to be downloaded to

    csv1 = open(download_dir, "w")
    #"w" indicates that you're writing strings to the file

    columnTitleRow = "prdt_id, prdt_title, reviewerID, sentiment_score\n"
    csv1.write(columnTitleRow)

    df = getDF('/Users/shreyajoshi/Downloads/reviews_Beauty_5.json.gz')         #read main dataset
    prdt_dict_list=getDict('/Users/shreyajoshi/Documents/722-term paper/meta_Beauty.json.gz')   #read metadat



    #print(prdt_dict_list)

    i=0

    for sentence in df['reviewText']:

        senti_score=print_sentiment_scores(sentence)

       #match product id to product name from metadata
        this_list = next((item for item in prdt_dict_list if item["asin"] == df.loc[i,'asin']), None)
        rowline = df.loc[i, 'asin'] + "," + str(this_list['title']).replace(',', '') + "," + df.loc[
            i, 'reviewerID'] + "," + str(df.loc[i, 'overall']) + "," + str(df.loc[i, 'reviewTime']).replace(',','') + "," + str(senti_score) + "\n"
        #write to prdt_review.csv
        csv1.write(rowline)
        i+=1
        print(i)



main()
