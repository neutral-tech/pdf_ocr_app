import os
import pytesseract
from flask import Flask, request, render_template
from pdf2image import convert_from_bytes

app = Flask(__name__)

# Set the explicit path for Tesseract on Render
pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"

@app.route("/", methods=["GET", "POST"])
def index():
    extracted_text = ""
    
    if request.method == "POST":
        if "pdf_file" not in request.files:
            return "No file part"
        
        file = request.files["pdf_file"]
        
        if file.filename == "":
            return "No selected file"
        
        if file:
            # Convert PDF to images
            images = convert_from_bytes(file.read())
            
            # Extract text from images using Tesseract OCR
            extracted_text = "\n".join([pytesseract.image_to_string(img) for img in images])

    return render_template("index.html", extracted_text=extracted_text)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Use correct port for deployment
    app.run(host="0.0.0.0", port=port, debug=True)
