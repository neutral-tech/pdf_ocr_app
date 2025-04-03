import os
import subprocess
import pytesseract
from flask import Flask, request, render_template
from pdf2image import convert_from_bytes

app = Flask(__name__)

# Install Tesseract and Poppler at runtime if not installed
try:
    subprocess.run(["tesseract", "--version"], check=True)
except FileNotFoundError:
    print("Installing Tesseract and Poppler...")
    subprocess.run(["apt-get", "update"])
    subprocess.run(["apt-get", "install", "-y", "tesseract-ocr", "poppler-utils"])

# Set the Tesseract path
pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"

@app.route("/", methods=["GET", "POST"])
def index():
    extracted_text = ""
    
    if request.method == "POST":
        if "pdf" not in request.files:
            return "No file part"
        
        file = request.files["pdf"]
        
        if file.filename == "":
            return "No selected file"
        
        if file:
            # Convert PDF to images
            images = convert_from_bytes(file.read())
            
            # Extract text from images using Tesseract OCR
            extracted_text = "\n".join([pytesseract.image_to_string(img) for img in images])

    return render_template("index.html", extracted_text=extracted_text)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
