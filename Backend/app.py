from flask import Flask
from api import upload_pdf
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)


app = Flask(__name__)

# Register API routes
app.add_url_rule('/upload', 'upload_pdf', upload_pdf, methods=['POST'])

if __name__ == '__main__':
    app.run(debug=True)