from flask import Flask, request, jsonify
from PIL import Image
import pytesseract
import io
import requests

app = Flask(__name__)

# Make sure tesseract is installed and in the path
pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"

@app.route('/process-image', methods=['POST'])
def process_image():
    try:
        # Get the image file from the request
        image_url = request.json.get("image")
        
        # If URL provided, fetch the image
        if image_url:
            response = requests.get(image_url)
            img = Image.open(io.BytesIO(response.content))
        else:
            return jsonify({'error': 'No image URL provided'}), 400
        
        # Perform OCR
        extracted_text = pytesseract.image_to_string(img)

        return jsonify({'text': extracted_text}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
