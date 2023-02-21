from flask import Flask, jsonify, render_template,request
from flask_cors import CORS, cross_origin
# import logging
from tableIndex import getTableIndex
from getBooksApi import getBooksData
from cosine import cosineSearchWord, getMatrixCloseness
from jaccard import jaccardSimilarity
import time, concurrent.futures, json, requests
from threading import Lock


# logging.basicConfig(level=logging.INFO)

# listBooks = [49345,56667,1,2,3,4,5,6,7]
listBooks = [l for l in range(1,20)]

# Initial variable
historyWords = dict()
lastSearchWord = dict({"word": ""})
tableIndexData, booksInfo, allBooks = getTableIndex(listBooks)

def create_app(debug=True):

    # create and configure the app
    app = Flask(__name__)
    app.config.from_object(__name__)

    # enable CORS
    CORS(app, resources={r'/*': {'origins': '*'}})
    app.config['CORS_HEADERS'] = 'Content-Type'
    app.config['JSON_SORT_KEYS'] = False



    #### GET
    @app.route("/")
    def index():
        return render_template("index.html")

    # try to get only 10 book
    @app.route('/getbooks', methods=['GET'])
    def get_books():
        print("Running get_books")
        # data = getBooksData(listBooks)
        return jsonify(allBooks)

    # find book with keyword
    @app.route('/searchbook/<word>', methods=['GET'])
    def search_books(word):
        print("Running search_books POST")
        # tableIndexData, booksInfo = getTableIndex(listBooks)
        if tableIndexData.get(word)!=None:
            # print(jsonify(tableIndexData[word]))
            sortedBooks = dict(sorted(tableIndexData[word].items(),key=lambda x:x[1], reverse=True))
            bookData =  getBooksData(sortedBooks.keys())
            return jsonify(bookData)
        else:
            return "NOT_FOUND"
        
    # get table index
    @app.route('/tableindex', methods=['GET'])
    def table_index():
        return jsonify(list(tableIndexData.keys()))
    
    # Use Cosine to have suggestion & ranking
    @app.route('/cosine', methods=['GET'])
    def cosine():
        print("Running cosine")
        booksData = cosineSearchWord(historyWords, tableIndexData)
        top5 = list(booksData.keys())[0:5]  if len(list(booksData.keys())) > 5 else list(booksData.keys())
        ranking = getBooksData(top5)
        return jsonify(ranking)

    # Use Jaccard to have list of book suggestion and order it
    @app.route('/jaccard', methods=['GET'])
    def jaccard():
        booksData = jaccardSimilarity(historyWords,booksInfo)

        # sortedBooks = sorted(booksData, key=lambda d: d['jaccard'], reverse=True) 
        sendBookId = []
        for sb in booksData:
            if sb['jaccard'] > 0:
                sendBookId.append(sb['bookId'])
        top5 = sendBookId.slice(0,5)  if len(sendBookId) > 5 else sendBookId
        ranking = getBooksData(top5)
        # print(booksData)
        return jsonify(ranking)
        # return jsonify(sendBookId, booksData, historyWords)

    @app.route('/lastsearch', methods=['GET'])
    def last_search():
        print('Running last search')
        lastSearch = lastSearchWord["word"]
        sortedBooks = dict()
        if tableIndexData.get(lastSearch)!=None and lastSearch != "":
            # print(jsonify(tableIndexData[word]))
            sortedBooks = dict(sorted(tableIndexData[lastSearch].items(),key=lambda x:x[1], reverse=True))
        lastSearchList = getBooksData(list(sortedBooks.keys()))
        return jsonify(lastSearchList)

    @app.route('/suggestion', methods=['GET'])
    def suggestion():
        print('Running suggestion')

        # Init variable
        lastSearch = lastSearchWord["word"]
        sortedBooks = dict()
        suggestionBooks = []
        lock = Lock()
        
        print("Last search" , lastSearch)
        if tableIndexData.get(lastSearch)!=None and lastSearch != "":
            # print(jsonify(tableIndexData[word]))
            sortedBooks = dict(sorted(tableIndexData[lastSearch].items(),key=lambda x:x[1], reverse=True))
        closenessData = getMatrixCloseness(tableIndexData)

        def getSuggestion(id,closeData):
            lock.acquire()
            if closeData['bookId'] in list(sortedBooks.keys()):
                if id==0:
                    if closenessData[id+1]['bookId'] not in suggestionBooks and closenessData[id+1]['bookId'] not in list(sortedBooks.keys()):
                        suggestionBooks.append(closenessData[id+1]['bookId']) 
                elif id==len(closenessData)-1:
                    if closenessData[id-1]['bookId'] not in suggestionBooks and closenessData[id-1]['bookId'] not in list(sortedBooks.keys()):
                        suggestionBooks.append(closenessData[id-1]['bookId']) 
                else:
                    if closenessData[id+1]['bookId'] not in suggestionBooks and closenessData[id+1]['bookId'] not in list(sortedBooks.keys()):
                        suggestionBooks.append(closenessData[id+1]['bookId']) 
                    if closenessData[id-1]['bookId'] not in suggestionBooks and closenessData[id-1]['bookId'] not in list(sortedBooks.keys()):
                        suggestionBooks.append(closenessData[id-1]['bookId']) 
            lock.release()

        print("Running thread suggestion:")
        threaded_start = time.time()
        # booksData = []
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for id,closeData in enumerate(closenessData):
                futures.append(executor.submit(getSuggestion, id,closeData))
        print("Threaded suggestion", time.time() - threaded_start)

        suggestionList = getBooksData(suggestionBooks)      
        return jsonify(suggestionList)

    #### POST
    # send search data
    @app.route('/searchdata', methods=['POST'])
    @cross_origin(origin='*',headers=['content-type'])
    def search_data():
        print("Running search_data with keyword")
        word = request.json['word']
        lowerWord = word.lower()
        lastSearchWord["word"] = lowerWord
        if lowerWord in historyWords:
            historyWords[lowerWord] += 1
        else:
            historyWords[lowerWord] = 1
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