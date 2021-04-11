import requests
import sys
import json
import yaml

#User Pref for the Proof Of Concept
Isbn = ['9-780439-136358', '9781496374929']


if sys.version_info[0] < 3 and sys.version_info[1] < 7:
    raise Exception("Must be using Python 3.7+ for script to run as it contains f-strings.\nMust also have \"requests\" library installed.")

def DictExits(VarToTest, Var):
    try:
        return [True, VarToTest[Var]]
    except:
        return [False, "None."]

def IsbnConvert(isbn):
    out = {
        'PastBooks': [],
        'CurrentBook': {}
    }

    isbn = int(isbn.replace("-", "").replace(".", ""))

    GoogleApi = requests.get(f'https://www.googleapis.com/books/v1/volumes?q=isbn%3D{isbn}').json()['items']



    #count = 0
    #Old code
    # for LoopVar in GoogleApi:
    #     if LoopVar == GoogleApi[len(GoogleApi)-1]:
    #
    #         out['CurrentBook'] = {
    #             'Title': LoopVar['volumeInfo']['title'],
    #             'Description': DictExits(LoopVar['volumeInfo'], 'description')[1],
    #             'Authors': LoopVar['volumeInfo']['authors'],
    #             'PublishingDate': LoopVar['volumeInfo']['publishedDate'],
    #             'ImgLink': LoopVar['volumeInfo']['imageLinks']['thumbnail'],
    #             'Img': requests.get(LoopVar['volumeInfo']['imageLinks']['thumbnail']).content,
    #             'Isbn': LoopVar['volumeInfo']['industryIdentifiers'],
    #             'Index': count
    #         }
    #     else:
    #         out['PastBooks'].append({
    #                 'Title': LoopVar['volumeInfo']['title'],
    #                 'Description': DictExits(LoopVar['volumeInfo'], 'description')[1],
    #                 'Authors': LoopVar['volumeInfo']['authors'],
    #                 'PublishingDate': LoopVar['volumeInfo']['publishedDate'],
    #                 'ImgLink': LoopVar['volumeInfo']['imageLinks']['thumbnail'],
    #                 'Img': requests.get(LoopVar['volumeInfo']['imageLinks']['thumbnail']).content,
    #                 'Isbn':LoopVar['volumeInfo']['industryIdentifiers'],
    #                 'Index':count
    #             })
    #     count = count+1
    return out




for currentisbn in Isbn:
    print(currentisbn)
    IsbnDict = IsbnConvert(currentisbn)
    try:
        ImgName = IsbnDict['CurrentBook']['Isbn'][1]['identifier']
    except:
        ImgName = IsbnDict['CurrentBook']['Isbn'][0]['identifier']

    with open(f'{ImgName}.jpg', 'wb') as f:
        f.write(IsbnDict['CurrentBook']['Img'])
        f.close()
    with open(f'{ImgName}.yml', 'w') as f:
        doc = yaml.dump(IsbnDict, f)
        f.close()