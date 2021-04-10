import requests
import sys

#User Pref for the Proof Of Concept
Isbn = '9-780439-136358'


if sys.version_info[0] < 3 and sys.version_info[1] < 7:
    raise Exception("Must be using Python 3.7+ for script to run as it contains f-strings.\nMust also have \"requests\" library installed.")


def IsbnConvert(isbn):
    out = {
        'PastBooks': [],
        'CurrentBook': {}
    }
    isbn = int(isbn.replace("-", "").replace(".", ""))

    GoogleApi = requests.get(f'https://www.googleapis.com/books/v1/volumes?q=isbn%3D{isbn}').json()['items']

    # If you have api key, replace link below with: https://www.googleapis.com/books/v1/volumes?q=isbn%3D{isbn}?key={YOUR_KEY}

    count = 0
    for LoopVar in GoogleApi:
        if LoopVar == GoogleApi[len(GoogleApi)-1]:
            out['CurrentBook'] = {
                'Title': LoopVar['volumeInfo']['title'],
                'Description': LoopVar['volumeInfo']['description'],
                'Authors': LoopVar['volumeInfo']['authors'],
                'PublishingDate': LoopVar['volumeInfo']['publishedDate'],
                'ImgLink': LoopVar['volumeInfo']['imageLinks']['thumbnail'],
                'Img': requests.get(LoopVar['volumeInfo']['imageLinks']['thumbnail']).content,
                'Isbn': LoopVar['volumeInfo']['industryIdentifiers'],
                'Index': count
            }
        else:
            out['PastBooks'].append({
                    'Title': LoopVar['volumeInfo']['title'],
                    'Description': LoopVar['volumeInfo']['description'],
                    'Authors': LoopVar['volumeInfo']['authors'],
                    'PublishingDate': LoopVar['volumeInfo']['publishedDate'],
                    'ImgLink': LoopVar['volumeInfo']['imageLinks']['thumbnail'],
                    'Img': requests.get(LoopVar['volumeInfo']['imageLinks']['thumbnail']).content,
                    'Isbn':LoopVar['volumeInfo']['industryIdentifiers'],
                    'Index':count
                })
        count = count+1
    return out



conv = IsbnConvert(Isbn)
print(conv)
try:
    ImgName = conv['CurrentBook']['Isbn'][1]['identifier']
except:
    ImgName = conv['CurrentBook']['Isbn'][0]['identifier']

with open(ImgName+'.jpg', 'wb') as f:
    #print(IsbnConvert(Isbn)['CurrentBook']['Img'])
    f.write(conv['CurrentBook']['Img'])
    f.close()





#return requests.get(GoogleApiRefined).content#image
    #want to
    # return
    # {
    # 'PastBooks': [
    # {'Title':"str", 'SubTitle':"str", 'Description':"str", 'Authors':[list], 'PublishingDate':"str", 'img':(img)}
    # {'Title':"str", 'SubTitle':"str", 'Description':"str", 'Authors':[list], 'PublishingDate':"str", 'img':(img)} ],
    # 'CurrentBook': {'Title':"str", 'SubTitle':"str", 'Description':"str", 'Authors':[list], 'PublishingDate':"str"}
    # }

#Old code to save img to files
        #print(LoopVar['volumeInfo']['imageLinks']['thumbnail'])
        #with open(f'{count}.jpg', 'wb') as f:
            #print(f"Saving: {LoopVar['volumeInfo']['imageLinks']['thumbnail']} as {count}.jpg")
            #f.write(requests.get(LoopVar['volumeInfo']['imageLinks']['thumbnail']).content)
            #f.close()

#with open('tiny.jpg', 'wb') as f:
    #f.write(IsbnConvert('9-780439-136358'))
#Harry Potter Prisoner of Azkaban
#0-439-13635-0
#9-780439-136358