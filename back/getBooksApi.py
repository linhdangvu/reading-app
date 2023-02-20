
import time, concurrent.futures, json, requests

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
    print("Running get books threads:")
    threaded_start = time.time()
    booksData = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for bookId in listBooks:
            futures.append(executor.submit(getBooksThread, bookId))
        for future in concurrent.futures.as_completed(futures):
            if future.result() != 'NOT_FOUND':
                booksData.append(future.result())
            # print(future.result())
    print("Threaded get books", time.time() - threaded_start)
    return booksData



def getListBooks(listBooks):
    def transformData(d):
        res = []
        if d.get('formats')!=None:
            for t in d['formats'].keys():
                checkEnd = d['formats'][t].split('.').pop()
                if checkEnd == 'txt':
                    res.append({
                        'id': d['id'],
                        'text_url': d['formats'][t]
                    })
        return res
    
    data = getBooksData(listBooks)
    result = []
    
    print("Running get list books:")
    threaded_start = time.time()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for d in data:
            futures.append(executor.submit(transformData, d))
        for future in concurrent.futures.as_completed(futures):
            result += future.result()
    print("Threaded get list books time:", time.time() - threaded_start)
    return result, 