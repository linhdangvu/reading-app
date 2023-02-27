
import time, json, requests
from thread import baseThreadPool

# This function is to get a book from Gutendex
def getBooksThread(bookId, timeout=10):
    response_API = requests.get('https://gutendex.com/books/{}'.format(bookId), timeout=timeout)
    data = response_API.text
    parse_json = json.loads(data)
    if parse_json.get('detail') != None:
        # print(bookId)
        return 'NOT_FOUND'
    return parse_json 

def get30Books(booksList, timeout=10):
    booksIdList = ','.join(str(b) for b in booksList)
    response_API = requests.get('https://gutendex.com/books?ids={}'.format(booksIdList), timeout=timeout)
    data = response_API.text
    parse_json = json.loads(data)
    if parse_json.get('results') == None:
        # print(bookId)
        return 'NOT_FOUND'
    return parse_json['results']

# This function is to get a list of books from Gutendex by using Thread and function getBooksThread
def getBooksData(listBooks):
    print("RUNNING function getBooksData")
    books_30 = [listBooks[x:x+30] for x in range(0, len(listBooks), 30)]
    # test = get30Books(listBooks)
    threaded_start = time.time()
    # booksData = baseThreadPool(listBooks, getBooksThread, True)
    booksData = baseThreadPool(books_30, get30Books, True, 2)
    print("END function getBooksData -----> {}".format(time.time() - threaded_start))
    return booksData

# This function is to get text from book
def getListBooks(listBooks):
    print("RUNNING function getListBooks")
    threaded_start = time.time()
    def transformData(d):
        res = []
        # print(d)
        if d != 'NOT_FOUND':
            if d.get('formats')!=None:
                for t in d['formats'].keys():
                    checkEnd = d['formats'][t].split('.').pop()
                    if checkEnd == 'txt':  
                        res.append({
                            'id': d['id'],
                            'text_url': d['formats'][t]
                        })
        return res 
    allBooks = getBooksData(listBooks)    
    # print('Books total: ' + len(allBooks))
    result = baseThreadPool(allBooks, transformData, True, 2) 
    print("END function getListBooks -----> {}".format(time.time() - threaded_start))
    return result, allBooks