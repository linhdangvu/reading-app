
import time, json, requests
from thread import baseThreadPool

# request to get books
def getBooksThread(bookId, timeout=10):
    response_API = requests.get('https://gutendex.com/books/{}'.format(bookId), timeout=timeout)
    data = response_API.text
    parse_json = json.loads(data)
    if parse_json.get('detail') != None:
        # print(bookId)
        return 'NOT_FOUND'
    return parse_json 

def getBooksData(listBooks):
    print("RUNNING function getBooksData")
    threaded_start = time.time()
    booksData = baseThreadPool(listBooks, getBooksThread, True)
    print("END function getBooksData -----> {}".format(time.time() - threaded_start))
    return booksData

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
    result = baseThreadPool(allBooks, transformData, True, 2) 
    print("END function getListBooks -----> {}".format(time.time() - threaded_start))
    return result, allBooks