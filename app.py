import os
from flask import Flask, request, render_template
import pytesseract
from pdf2image import convert_from_path

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    extracted_text = None
    if request.method == "POST":
        if "pdf" not in request.files:
            return "No file part"
        
        file = request.files["pdf"]
        if file.filename == "":
            return "No selected file"
        
        if file:
            filepath = os.path.join("uploads", file.filename)
            file.save(filepath)

            images = convert_from_path(filepath)
            extracted_text = "\n".join([pytesseract.image_to_string(img) for img in images])

    return render_template("index.html", text=extracted_text)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Use PORT from environment for deployment
    app.run(host="0.0.0.0", port=port)
