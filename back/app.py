from flask import Flask, jsonify, render_template,request
from flask_cors import CORS, cross_origin
from sklearn.metrics.pairwise import cosine_similarity, cosine_distances
import pandas as pd
import requests, json, logging, re, time, concurrent.futures


# logging.basicConfig(level=logging.INFO)

listBooks = [49345,56667,1,2,3,4,5,6,7]
listBooks = [l for l in range(1,100)]

# get table index for all book and each book
def getTableIndex(listBooksData):
    # counts = dict()
    # word2letters = dict()
    # word3letters = dict()
    tableIndex = dict()
    booksInfo = []

    for book in listBooksData:
        response_API = requests.get(book['text_url'])
        data = response_API.text
        #### Option 1: Prendre seulement des mots avec carateres de 4 à 10
        words = re.findall(r"[A-Za-z]{4,10}\w+", data)
        occurentCounts = dict()

        for word in words:
            w = word.lower()

            # Count for table index all books
            if w in tableIndex:
                if book['id'] in tableIndex[w]:
                    tableIndex[w][book['id']] += 1
                else:
                    tableIndex[w][book['id']] = 1
            else:
                tableIndex[w] = dict({book['id']: 1})

            # Count for table index for each book
            if w in occurentCounts:
                occurentCounts[w] += 1
            else:
                occurentCounts[w] = 1

        booksInfo.append({
            "bookId": book['id'],
            "words": occurentCounts,
            "totalWords": len(words),
            "totalWordsWithOccur": len(occurentCounts)
        })

        #### Option 2: Prendre tous les caracteres mais distingué des mots de 2 et de 3 caracteres 
        # words = re.findall(r"[A-Za-z]+", data) 
        # if len(w) <= 2:
        #     if w in word2letters:
        #         word2letters[w] += 1
        #     else:
        #         word2letters[w] = 1
        # elif len(w) == 3:
        #     if w in word3letters:
        #         word3letters[w] += 1
        #     else:
        #         word3letters[w] = 1
        # else:
        #     if w in counts:
        #         counts[w] += 1
        #     else:
        #         counts[w] = 1
        #     if w in tableIndex:
        #         if book not in tableIndex[w]:
        #             tableIndex[w] += [book]
        #     else:
        #         tableIndex[w] = [book]
            
    return tableIndex, booksInfo



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
    print("Running threaded:")
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
    print("Threaded time:", time.time() - threaded_start)
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
    return result

def cosineSimilarity(historyWords, tableIndexData):
    booksData = dict({'history':historyWords})
    result = dict()

    for word in historyWords.keys():
        if word in tableIndexData:
            for b in tableIndexData[word].keys(): 
                if b in booksData:
                    booksData[b].update(dict({word:tableIndexData[word][b]}))
                else:
                    booksData.update(dict({b: dict({word:tableIndexData[word][b]})}))

    bookDF = pd.DataFrame(booksData.values(),
        index=booksData.keys()).fillna(0)

    # print(bookDF)

    for cs in list(booksData.keys())[1:]:
        result[cs] = cosine_similarity(bookDF.loc["history":"history"],bookDF.loc[cs:cs])[0][0]
    return result

def create_app(debug=True):

    # create and configure the app
    app = Flask(__name__)
    app.config.from_object(__name__)

    # enable CORS
    CORS(app, resources={r'/*': {'origins': '*'}})
    app.config['CORS_HEADERS'] = 'Content-Type'

    # Initial variable
    historyWords = dict()
    listBooksData = getListBooks(listBooks)
    tableIndexData, booksInfo = getTableIndex(listBooksData)
    

    #### GET
    @app.route("/")
    def index():
        return render_template("index.html")

    # try to get only 10 book
    @app.route('/getbooks', methods=['GET'])
    def get_books():
        data = getBooksData(listBooks)
        return jsonify(data)

    # find book with keyword
    @app.route('/searchbook/<word>', methods=['GET'])
    def search_books(word):
        # tableIndexData = getTableIndex(listBooks)
        if tableIndexData.get(word)!=None:
            print(jsonify(tableIndexData[word]))
            sortedBooks = dict(sorted(tableIndexData[word].items(),key=lambda x:x[1], reverse=True))
            bookData =  getBooksData(sortedBooks.keys())
            return jsonify(bookData)
        else:
            return "NOT_FOUND"
        
    # get table index
    @app.route('/tableindex', methods=['GET'])
    def table_index():
        return jsonify(list(tableIndexData.keys()))
    
    # Use Cosine to have recommend
    @app.route('/cosine', methods=['GET'])
    def cosine():
        res = cosineSimilarity(historyWords, tableIndexData)
        sortedBooks = dict(sorted(res.items(),key=lambda x:x[1], reverse=True))
        # return jsonify(sortedBooks)
        top5 = list(sortedBooks.keys())[0:5]  if len(list(sortedBooks.keys())) > 5 else list(sortedBooks.keys())
        ranking = getBooksData(top5)
        return jsonify(ranking)

    # Use Jaccard to have list of book suggestion and order it
    @app.route('/rankingbooks', methods=['GET'])
    def ranking_books():
        booksData = []
        for book in booksInfo:
            count = 0
            for w in historyWords.keys():
                if w in book['words']:
                    # count number occurs in document
                    # count += book['words'][w]
                    # count if have that word in ducument
                    count += historyWords[w]
            booksData.append({
                "bookId": book['bookId'],
                "jaccard": (count/book['totalWordsWithOccur'])
            })

        sortedBooks = sorted(booksData, key=lambda d: d['jaccard'], reverse=True) 
        sendBookId = []

        for sb in sortedBooks:
            if sb['jaccard'] > 0:
                sendBookId.append(sb['bookId'])
        top5 = sendBookId.slice(0,5)  if len(sendBookId) > 5 else sendBookId
        ranking = getBooksData(top5)
        return jsonify(ranking)
        # return jsonify(sendBookId, sortedBooks, historyWords)
    
    # Use Jaccard to have list of book suggestion and order it
    @app.route('/checkranking', methods=['GET'])
    def check_ranking():
        booksData = []
        for book in booksInfo:
            count = 0
            for w in historyWords.keys():
                if w in book['words']:
                    # count number occurs in document
                    # count += book['words'][w]
                    # count if have that word in ducument
                    count += historyWords[w]
            booksData.append({
                "bookId": book['bookId'],
                "jaccard": (count/book['totalWordsWithOccur'])
            })

        sortedBooks = sorted(booksData, key=lambda d: d['jaccard'], reverse=True) 
        sendBookId = []

        for sb in sortedBooks:
            if sb['jaccard'] > 0:
                sendBookId.append(sb['bookId'])
        top5 = sendBookId.slice(0,5)  if len(sendBookId) > 5 else sendBookId
        ranking = getBooksData(top5)
        # return jsonify(ranking)
        return jsonify(sendBookId, sortedBooks, historyWords)

    #### POST
    # send search data
    @app.route('/searchdata', methods=['POST'])
    @cross_origin(origin='*',headers=['content-type'])
    def search_data():
        word = request.json['word']
        lowerWord = word.lower()
        if lowerWord in historyWords:
            historyWords[word] += 1
        else:
            historyWords[word] = 1

        return jsonify(historyWords)
    
    ### TEST
    # get table index for each book
    @app.route('/itbook', methods=['GET'])
    def itbook():
        return jsonify(booksInfo)
    
    @app.route('/tindex', methods=['GET'])
    def tindex():
        return jsonify(tableIndexData)
            
    return app

app = create_app(debug=True)
app.run()