import os
import string
import random
from datetime import datetime, timedelta
from flask import Flask, request, redirect, jsonify, render_template
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

client = MongoClient(os.getenv('MONGODB_URI'))
db = client.get_database('url_shortener')
urls_collection = db.urls

CHARS = string.ascii_letters + string.digits
BASE_URL = "http://localhost:5000/"

def generate_short_code(length=6):
    return ''.join(random.choices(CHARS, k=length))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()
    original_url = data.get('url')
    expiration_seconds = int(data.get('expiration', 3600)) 
    
    if not original_url:
        return jsonify({'error': 'URL is required'}), 400
    
    short_code = generate_short_code()
    
    while urls_collection.find_one({'short_code': short_code}):
        short_code = generate_short_code()
    
    expiration_date = datetime.utcnow() + timedelta(seconds=expiration_seconds)
    
    urls_collection.insert_one({
        'short_code': short_code,
        'original_url': original_url,
        'created_at': datetime.utcnow(),
        'expires_at': expiration_date,
        'clicks': 0
    })
    
    short_url = BASE_URL + short_code
    return jsonify({'short_url': short_url})

@app.route('/<short_code>')
def redirect_to_url(short_code):
    url_doc = urls_collection.find_one({
        'short_code': short_code,
        'expires_at': {'$gt': datetime.utcnow()} 
    })
    
    if url_doc:
        urls_collection.update_one(
            {'short_code': short_code},
            {'$inc': {'clicks': 1}}
        )
        return redirect(url_doc['original_url'])
    else:
        return render_template('not_found.html'), 404

@app.route('/stats/<short_code>')
def url_stats(short_code):
    url_doc = urls_collection.find_one({'short_code': short_code})
    
    if url_doc:
        stats = {
            'original_url': url_doc['original_url'],
            'created_at': url_doc['created_at'],
            'expires_at': url_doc['expires_at'],
            'clicks': url_doc.get('clicks', 0)
        }
        return jsonify(stats)
    else:
        return jsonify({'error': 'URL not found'}), 404

if __name__ == '__main__':
    urls_collection.create_index('short_code')
    urls_collection.create_index('expires_at')
    
    app.run(debug=True)