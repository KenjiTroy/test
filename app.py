from flask import Flask
from PIL import Image
import pytesseract

app = Flask(__name__)

@app.route('/process-image', methods=['POST'])
def process_image():
    try:
        data = request.json
       
        # Check if an image file or URL is provided in the request
        image_url = data.get("image")
        if image_url:
            response = requests.get(image_url)
            if response.status_code != 200:
                return jsonify({'error': 'Unable to fetch image from URL'}), 400
            img = Image.open(io.BytesIO(response.content))
       
        # Apply image processing
        img = img.convert('L')  # Convert to grayscale
        img = img.filter(ImageFilter.MedianFilter())  # Apply median filter
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(2)  # Enhance contrast
       
        # Perform OCR
        extracted_text = pytesseract.image_to_string(img)
       
        # Tokenize text: Split into words (ignores punctuation and splits on spaces)
        tokens = re.findall(r'\b\w+\b', extracted_text)
       
        return jsonify({'text': extracted_text, 'tokens': tokens}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

@app.route('/')
def ocr():
    # test.png from the pytesseract project: https://github.com/madmaze/pytesseract/tree/master/tests/data
    return pytesseract.image_to_string(Image.open('test.png'))