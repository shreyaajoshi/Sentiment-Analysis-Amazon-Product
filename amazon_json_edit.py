"""
amazon_json_edit.py

Script to convert JSON amazon review data into a usable format.

@author: Brody Kutt (bjk4704@rit.edu)
"""

import os, sys
import json
from random import shuffle


USAGE = """
    HOW TO RUN:

        python amazon_json_edit.py {1}

    WHERE:

        {1} = Directory that contains amazon reviews in original per-product format
        """


def extract_product_dict(json_file_dict):
    product_dict = {}

    productInfo = json_file_dict['ProductInfo']
    reviewInfo = json_file_dict['Reviews']
    if len(reviewInfo) == 0:
        return None, None
    productID = productInfo['ProductID']

    product_dict['Name'] = productInfo['Name']
    if product_dict['Name'] == None:
        return None, None
    product_dict['Price'] = productInfo['Price']
    product_dict['Features'] = productInfo['Features']
    product_dict['Reviews'] = reviewInfo

    return productID, product_dict



def main():

    if(len(sys.argv) != 2):
        print(USAGE)
        sys.exit(1)

    path = sys.argv[1]

    # Grab all file paths in directory
    print "\nDiscovering files...",
    all_json_files = []
    for (root, dirs, files) in os.walk(path):
        for name in files:
            all_json_files.append(os.path.join(root, name))
    shuffle(all_json_files)
    print str(len(all_json_files)) + " files grabbed"

    # # Iterate through each JSON and consolidate the files into one JSON format
    print "Reading files...",
    num_files = 0
    new_json_dict = {}
    for f in all_json_files:
        # Read JSON file
        json_file = open(f, 'r')
        json_file_text = json_file.read()
        json_file_dict = json.loads(json_file_text)

        # Extract relevant info and make new entry
        productID, product_dict = extract_product_dict(json_file_dict)
        if productID is None:
            continue
        new_json_dict[productID] = product_dict

        # Limit number of files total
        json_file.close()
        num_files += 1
        if(num_files > 250):
            break
    print str(num_files-1) + " files read"

    # Write results to new file
    print "Writing new JSON file...",
    new_json_string = json.dumps(new_json_dict, indent=4, sort_keys=True)
    out_file = open('new_dataset.json', 'w')
    out_file.write(new_json_string)
    out_file.close()
    print "Success!"



if __name__ == '__main__':
    main()
