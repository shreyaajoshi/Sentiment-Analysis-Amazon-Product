import re
import csv

def ifmore(name_set):
    print 'Which one did you mean?? please provide more info....'
    print name_set
    #new_set=[]
    test()

def test():
    #print new_set
    new_set=[]
    prdt_name = raw_input("Which product would you like to know about ==> ").lower()

    prdt_list_name=re.findall(r'\w+',prdt_name)

    overall_count=0
    positive_count=0
    negative_count=0
    neutral_count=0
    total_sentiment_value=0
    avg_sentiment_value=0
    prdt_title=''

    with open('prdtReview.csv') as f:
        csvReader = csv.reader(f)
        for row in csvReader:
            #print row
            if all(subs in row[1].lower() for subs in prdt_list_name):
                prdt_title=row[1]
                new_set.append(row[1])
                name_set = set(new_set)
                #print len(name_set)
                if len(name_set)>1:

                    ifmore(name_set)


                else:
                    overall_count+=1
                    if float(row[-1])>0.00:
                        positive_count+=1
                    elif float(row[-1])==0.00:
                        neutral_count+=1
                    else:
                        negative_count+=1

                    total_sentiment_value+=float(row[-1])

    avg_sentiment_value=total_sentiment_value/overall_count

    print '\n'
    print '******PRODUCT REPORT*******'
    print '\n'
    print prdt_title
    print '\n'
    print 'Total number of reviewers = ',overall_count
    print 'Number of positive reviews = ',positive_count
    print 'Number of neutral reviews = ', neutral_count
    print 'Number of negative reviews = ',negative_count
    print 'Mean sentiment score = ',round(avg_sentiment_value,2)
    exit()

def main():
    #new_set = []
    test()


main()