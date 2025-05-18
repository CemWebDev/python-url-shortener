# URL Shortener

A simple URL shortener built with Python, Flask, and MongoDB.

## Features

- Shorten long URLs to easy-to-share links
- Set custom expiration times for links
- Track click statistics for each shortened URL
- Simple and responsive web interface

## Setup

1. Clone the repository
   ```bash
   git clone https://github.com/CemWebDev/python-url-shortener.git
   cd python-url-shortener
   ```

2. Create and activate a virtual environment
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies
   ```bash
   pip install flask pymongo python-dotenv
   pip freeze > requirements.txt
   ```

4. Set up MongoDB
   - Create a MongoDB Atlas account or use a local MongoDB instance
   - Copy `.env.example` to `.env` and add your MongoDB connection string

5. Run the application
   ```bash
    python app.py
   ```

6. Visit `http://localhost:5000` in your browser

## How It Works

1. The application generates a random 6-character code for each URL
2. The original URL is stored in MongoDB with the short code as the key
3. When a user visits the shortened URL, they are redirected to the original URL
4. URLs expire after the specified time (default: 1 hour)
5. Click statistics are tracked for each shortened URL

## Project Structure

```bash
   python-url-shortener/
   ├── venv/
   ├── .gitignore
   ├── requirements.txt
   ├── app.py
   ├── .env
   ├── README.md
   ├── templates/
   │   ├── index.html
   │   └── not_found.html
   └── static/
       └── styles.css
```

