from flask import Flask, jsonify, render_template,request
from flask_cors import CORS, cross_origin
import  json
# import logging
from tableIndex import getTableIndex
from getBooksApi import getBooksData
from cosine import cosineSearchWord
from jaccard import jaccardSimilarity

# logging.basicConfig(level=logging.INFO)

listBooks = [49345,56667,1,2,3,4,5,6,7]
# listBooks = [l for l in range(1,20)]

def create_app(debug=True):

    # create and configure the app
    app = Flask(__name__)
    app.config.from_object(__name__)

    # enable CORS
    CORS(app, resources={r'/*': {'origins': '*'}})
    app.config['CORS_HEADERS'] = 'Content-Type'

    # Initial variable
    historyWords = dict()
    
    tableIndexData, booksInfo = getTableIndex(listBooks)
    

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
        res = cosineSearchWord(historyWords, tableIndexData)
        sortedBooks = dict(sorted(res.items(),key=lambda x:x[1], reverse=True))
        # return jsonify(sortedBooks)
        top5 = list(sortedBooks.keys())[0:5]  if len(list(sortedBooks.keys())) > 5 else list(sortedBooks.keys())
        ranking = getBooksData(top5)
        # return jsonify(ranking)
        return jsonify(sortedBooks)

    # Use Jaccard to have list of book suggestion and order it
    @app.route('/jaccard', methods=['GET'])
    def jaccard():
        booksData = jaccardSimilarity(historyWords,booksInfo)

        sortedBooks = sorted(booksData, key=lambda d: d['jaccard'], reverse=True) 
        sendBookId = []

        for sb in sortedBooks:
            if sb['jaccard'] > 0:
                sendBookId.append(sb['bookId'])
        top5 = sendBookId.slice(0,5)  if len(sendBookId) > 5 else sendBookId
        # ranking = getBooksData(top5)
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