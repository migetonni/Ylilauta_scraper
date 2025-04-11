
import scraper
from flask import Flask, request, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)
matched_posts = {}

@app.route('/get_all_posts', methods=['GET'])
def scrape_posts():
    global matched_posts
    global keyword
    keyword = request.args.get('keyword', '')
    URL = "https://ylilauta.org/satunnainen/"
    msg_limit = 1000
    all_posts = scraper.get_all_posts(URL, keyword)  
    matched_posts = scraper.get_matching_posts(all_posts, keyword)
    

    

    
    return jsonify(matched_posts)

@app.route('/add_to_db', methods=['POST'])
def add_to_db():
    global matched_posts
    global keyword
    if len(matched_posts) == 0:
        return jsonify({"error": "no posts so save"}), 400
    
    else:
        scraper.add_to_db(matched_posts, keyword)
        return jsonify({"success": "posts saved"}), 200
    
@app.route('/get_keywords', methods=['GET'])
def get_keyw():
    
    keywords = scraper.extract_keyword()
    return json.dumps(keywords, ensure_ascii=False)


@app.route('/get_sentiment', methods=['GET'])
def get_sent():
    global matched_posts
    if not matched_posts:
        return jsonify({"error": "no matched posts"}), 400
    sentiment = scraper.sentiments_analysis(matched_posts)
    return jsonify(sentiment)

    


    






if __name__ == '__main__':
    app.run()

