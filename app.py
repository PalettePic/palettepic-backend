from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
from colorthief import ColorThief
import io

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part in the request'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected for uploading'}), 400
        
        image_bytes = file.read()
        image_file = io.BytesIO(image_bytes)
        
        color_thief = ColorThief(image_file)
        palette = color_thief.get_palette(color_count=5)
        
        hex_palette = ['#%02x%02x%02x' % rgb for rgb in palette]
        
        return jsonify({'palette': hex_palette}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)