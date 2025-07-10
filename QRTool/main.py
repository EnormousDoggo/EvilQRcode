from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from VirusTotalAPI.scanner import scan_url as VTscan
from SandBoxGenerator.tests.script import create_sandbox, display_result, kill_sandbox

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
def process_url_VT(url):
    # Placeholder for processing logic
    print(f"Processing URL: {url}")
    stats = VTscan(url)  # Call the scan_url function from scanner.py
    VTResult = {"malveillants": [stats['malicious']], "inoffensifs": [stats['harmless']]}
    return VTResult

async def process_url_sandbox(url):
    Sandbox = await create_sandbox(url)  # Call the create_sandbox function from script.py
    print(f"Sandbox created with ID: {Sandbox}")
    SandboxResult = await display_result(Sandbox)  # Call the display_result function from script.py
    print(f"Sandbox result: {SandboxResult}")
    # kill_sandbox()  # Call the kill_sandbox function from script.py
    return SandboxResult

# Endpoint to serve Scan QR code
@app.route('/')
def index():
    return render_template('index.html')

# Endpoint to handle POST requests to /url/vt
@app.route('/url/vt', methods=['POST'])
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

    result = process_url_VT(url)
    return jsonify(result), 200

@app.route('/url/sandbox', methods=['POST'])
def sandbox():
    data = request.json
    if not data or 'url' not in data:
        return jsonify({'error': 'Missing "url" parameter'}), 400

    url = data['url']
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Save to database
    new_url = URLData(url=url, timestamp=timestamp)
    db.session.add(new_url)
    db.session.commit()

    result = process_url_sandbox(url)
    print(f"\n\n\nSandbox result: {result}\n\n\n")
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
    app.run(host='0.0.0.0', port=50000, debug=True)