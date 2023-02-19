from flask import Flask, jsonify, render_template,request
from flask_cors import CORS, cross_origin
import requests
import json
import logging
import re

# logging.basicConfig(level=logging.INFO)

listBooks = [49345,56667,1,2,3,4,5,6,7]

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
                if book['id'] not in tableIndex[w]:
                    tableIndex[w] += [book['id']]
            else:
                tableIndex[w] = [book['id']]

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
def getBooksData(listBooks):
    booksData = []
    for book in listBooks:
        response_API = requests.get('https://gutendex.com/books/{}'.format(book))
        #print(response_API.status_code)
        data = response_API.text
        parse_json = json.loads(data)
        booksData.append(parse_json)
    return booksData

def getListBooks():
    data = getBooksData(listBooks)
    result = []
    for d in data:
        for t in d['formats'].keys():
            checkEnd = d['formats'][t].split('.').pop()
            if(checkEnd == 'txt'):
                result.append({
                    'id': d['id'],
                    'text_url': d['formats'][t]
                })
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
    listBooksData = getListBooks()
    tableIndexData, booksInfo = getTableIndex(listBooksData)
    

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
            bookData =  getBooksData(tableIndexData[word])
            return jsonify(bookData)
        else:
            return "NOT_FOUND"
        
    # get table index
    @app.route('/tableindex', methods=['GET'])
    def table_index():
        return jsonify(list(tableIndexData.keys()))
    
    # get table index for each book
    @app.route('/itbook', methods=['GET'])
    def itbook():
        return jsonify(booksInfo)
    
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

    # Use Jaccard to have list of book suggestion and order it
    @app.route('/rankingbooks', methods=['GET'])
    def ranking_books():
        booksData = []
        for book in booksInfo:
            count = 0
            frequence = 0
            for w in historyWords.keys():
                if w in book['words']:
                    # count number occurs in document
                    count += book['words'][w]
                    frequence += historyWords[w]
                    # count if have that word in ducument
                    # count += 1
            booksData.append({
                "bookId": book['bookId'],
                "jaccard": (count/book['totalWords'])*frequence
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
            
    return app

app = create_app(debug=True)
app.run()