from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from VirusTotalAPI.scanner import scan_url

app = Flask(__name__)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the URL model
class URLData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(2048), nullable=False)
    timestamp = db.Column(db.String(100), nullable=False)

# Initialize the database
with app.app_context():
    db.create_all()

# Function to handle the URL (you can customize this)
def process_url(url):
    # Placeholder for processing logic
    print(f"Processing URL: {url}")
    VTresult = scan_url(url)  # Call the scan_url function from scanner.py
    return VTresult

# Endpoint to serve Scan QR code
@app.route('/')
def index():
    return render_template('index.html')

# Endpoint to handle POST requests to /url
@app.route('/url', methods=['POST'])
def url_endpoint():
    data = request.json
    if not data or 'url' not in data:
        return jsonify({'error': 'Missing "url" parameter'}), 400

    url = data['url']
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Save to database
    new_url = URLData(url=url, timestamp=timestamp)
    db.session.add(new_url)
    db.session.commit()

    result = process_url(url)
    print("URL received and processed")
    return jsonify(result), 200

# Endpoint to display the admin page
@app.route('/admin', methods=['GET'])
def admin_page():
    return render_template('admin.html')

# Endpoint to fetch URL data dynamically
@app.route('/api/urls', methods=['GET'])
def get_urls():
    urls = URLData.query.order_by(URLData.id.desc()).all()
    return jsonify([{'url': url.url, 'timestamp': url.timestamp} for url in urls])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=50000)