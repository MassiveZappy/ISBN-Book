import requests
import sys
import json
import yaml

#User Pref for the Proof Of Concept
#IDK IF THIS WORKS!!!
#UCSD:[id] for ucsd isbns
#ISBN MUST BE IN LIST FORMAT
Isbns = ['9781975173449','9781608316571','9780781778718']
#extra isbn '9780781778718'


if not sys.version_info[0] <= 3 and sys.version_info[1] > 6:
    raise Exception("Must be using Python 3.7+ for script to run as it contains f-strings.\nMust also have \"requests\" library installed.")

def DictExits(VarToTest, Var):
    try:
        return [True, VarToTest[Var]]
    except:
        return [False, "None."]

def IsbnConvert(isbn):
    TempOut = {
        'TheBook': {},
        'RelatedBooks': []
    }
    out = {}
    for CurrentIsbn in isbn:
        CurrentIsbn = CurrentIsbn.replace("-", "").replace(".", "")
        print("Fetching Cold Call for isbn:"+CurrentIsbn)
        GoogleApi = requests.get(f'https://www.googleapis.com/books/v1/volumes?q=isbn%3D{CurrentIsbn}').json()['items']
        count = 0
        for LoopVar in GoogleApi:
            print(LoopVar['volumeInfo']['industryIdentifiers'][0]['identifier'])
            try:
                if LoopVar['volumeInfo']['industryIdentifiers'][1]['identifier'] == CurrentIsbn:
                    print(f"Match:{LoopVar['volumeInfo']['industryIdentifiers'][1]['identifier']}")
                    TempOut['TheBook'] ={
                        'Title': LoopVar['volumeInfo']['title'],
                        'Description': DictExits(LoopVar['volumeInfo'], 'description')[1],
                        'PublishingDate': LoopVar['volumeInfo']['publishedDate'],
                        'GoogleImg': requests.get(LoopVar['volumeInfo']['imageLinks']['thumbnail']).content,
                        'Isbn': LoopVar['volumeInfo']['industryIdentifiers'],
                        'Index': count
                    }
                    if not DictExits(LoopVar['volumeInfo'], 'imageLinks')[0]:
                        TempOut['TheBook']['GoogleImg'] = False
                    elif DictExits(LoopVar['volumeInfo'], 'imageLinks')[0]:
                        TempOut['TheBook']['GoogleImg'] = requests.get(LoopVar['volumeInfo']['imageLinks']['thumbnail']).content
                        #TODO
                        with open(f'{CurrentIsbn}-google.jpg', 'wb') as f:
                            f.write(TempOut['TheBook']['GoogleImg'])
                            f.close()
                    if not DictExits(LoopVar['volumeInfo'], 'authors')[0]:
                        TempOut['TheBook']['Authors'] = False
                    elif DictExits(LoopVar['volumeInfo'], 'authors')[0]:
                        TempOut['TheBook']['Authors'] = LoopVar['volumeInfo']['authors']

                else:
                    TempOut['RelatedBooks'].append({
                        'Title': LoopVar['volumeInfo']['title'],
                        'Description': DictExits(LoopVar['volumeInfo'], 'description')[1],
                        'PublishingDate': LoopVar['volumeInfo']['publishedDate'],
                        'ImgLink': LoopVar['volumeInfo']['imageLinks']['thumbnail'],
                        'Isbn': LoopVar['volumeInfo']['industryIdentifiers'],
                        'Index': count
                    })
                    if not DictExits(LoopVar['volumeInfo'], 'imageLinks')[0]:
                        TempOut['RelatedBooks'][len(TempOut) - 1]['GoogleImg'] = False
                    elif DictExits(LoopVar['volumeInfo'], 'imageLinks')[0]:
                        TempOut['RelatedBooks'][len(TempOut) - 1]['GoogleImg'] = requests.get(LoopVar['volumeInfo']['imageLinks']['thumbnail']).content
                    if not DictExits(LoopVar['volumeInfo'], 'authors')[0]:
                        TempOut['RelatedBooks'][len(TempOut) - 1]['Authors'] = False
                    elif DictExits(LoopVar['volumeInfo'], 'authors')[0]:
                        TempOut['RelatedBooks'][len(TempOut) - 1]['Authors'] = LoopVar['volumeInfo']['authors']

            except:
                if LoopVar['volumeInfo']['industryIdentifiers'][0]['identifier'] == CurrentIsbn:
                    print(f"Match:{LoopVar['volumeInfo']['industryIdentifiers'][0]['identifier']}")
                    TempOut['TheBook'] = {
                        'Title': LoopVar['volumeInfo']['title'],
                        'Description': DictExits(LoopVar['volumeInfo'], 'description')[1],
                        'Authors': LoopVar['volumeInfo']['authors'],
                        'PublishingDate': LoopVar['volumeInfo']['publishedDate'],
                        'ImgLink': LoopVar['volumeInfo']['imageLinks']['thumbnail'],
                        'Isbn': LoopVar['volumeInfo']['industryIdentifiers'],
                        'Index': count
                    }
                    if not DictExits(LoopVar['volumeInfo'], 'imageLinks')[0]:
                        TempOut['TheBook']['GoogleImg'] = False
                    elif DictExits(LoopVar['volumeInfo'], 'imageLinks')[0]:
                        TempOut['TheBook']['GoogleImg'] = requests.get(LoopVar['volumeInfo']['imageLinks']['thumbnail']).content
                        #TODO
                        with open(f'{CurrentIsbn}.jpg', 'wb') as f:
                            f.write(TempOut['TheBook']['GoogleImg'])
                            f.close()
                    if not DictExits(LoopVar['volumeInfo'], 'authors')[0]:
                        TempOut['TheBook']['Authors'] = False
                    elif DictExits(LoopVar['volumeInfo'], 'authors')[0]:
                        TempOut['TheBook']['Authors'] = LoopVar['volumeInfo']['authors']

                else:
                    TempOut['RelatedBooks'].append({
                        'Title': LoopVar['volumeInfo']['title'],
                        'Description': DictExits(LoopVar['volumeInfo'], 'description')[1],
                        'PublishingDate': LoopVar['volumeInfo']['publishedDate'],
                        'ImgLink': DictExits(LoopVar['volumeInfo'], 'imageLinks')[1],
                        'Isbn': LoopVar['volumeInfo']['industryIdentifiers'],
                        'Index': count
                    })
                    if not DictExits(LoopVar['volumeInfo'], 'imageLinks')[0]:
                        TempOut['RelatedBooks'][len(TempOut)-1]['GoogleImg'] = False
                    elif DictExits(LoopVar['volumeInfo'], 'imageLinks')[0]:
                        TempOut['RelatedBooks'][len(TempOut) - 1]['GoogleImg'] = requests.get(LoopVar['volumeInfo']['imageLinks']['thumbnail']).content
                    if not DictExits(LoopVar['volumeInfo'], 'authors')[0]:
                        TempOut['RelatedBooks'][len(TempOut) - 1]['Authors'] = False
                    elif DictExits(LoopVar['volumeInfo'], 'authors')[0]:
                        TempOut['RelatedBooks'][len(TempOut) - 1]['Authors'] = LoopVar['volumeInfo']['authors']




            count = count + 1
        out[CurrentIsbn]=TempOut

        if  len(TempOut['TheBook']) == 0:
            TempOut['TheBook']['FoundAMatch'] = False

        else:
            TempOut['TheBook']['FoundAMatch'] = True

        TempOut = {
            'TheBook': {},
            'RelatedBooks': []
        }



    return out

    #count = 0
    #Old code
    # for LoopVar in GoogleApi:
    #     if LoopVar == GoogleApi[len(GoogleApi)-1]:
    #
    #         TempOut['CurrentBook'] = {
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
    #         TempOut['PastBooks'].append({
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




ImgName = "out"
IsbnsConv = IsbnConvert(Isbns)
print(IsbnsConv)
with open(f'{ImgName}.json', 'w') as f:
    f.write(json.dump(IsbnsConv, f))
    f.close()


# IsbnDict = IsbnConvert(currentisbn)
# try:
#     ImgName = IsbnDict['TheBook']['Isbn'][1]['identifier']
# except:
#     ImgName = IsbnDict['TheBook']['Isbn'][0]['identifier']
#
# with open(f'{ImgName}.yml', 'w') as f:
#     doc = yaml.dump(IsbnDict, f)
#     f.close()
# print(IsbnConvert(Isbns))