from flask import Flask
from api import upload_pdf

app = Flask(__name__)

# Register the upload_pdf route
app.add_url_rule('/upload', 'upload_pdf', upload_pdf, methods=['POST'])

if __name__ == '__main__':
    app.run(debug=True)