from flask import Flask, request, send_file, send_from_directory
import pandas as pd
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
CLEANED_FOLDER = "cleaned"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CLEANED_FOLDER, exist_ok=True)

# Serve CSS
@app.route('/style.css')
def css():
    return send_from_directory('.', 'style.css')

# Home
@app.route("/")
def home():
    with open("index.html") as f:
        return f.read()

# Upload & Clean
@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["file"]

    if file:
        path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(path)

        # Read file
        if file.filename.endswith(".csv"):
            df = pd.read_csv(path)
        else:
            df = pd.read_excel(path)

        # Cleaning
        df = df.drop_duplicates()
        df = df.dropna()

        cleaned_name = "cleaned_" + file.filename
        cleaned_path = os.path.join(CLEANED_FOLDER, cleaned_name)

        df.to_csv(cleaned_path, index=False)

        table = df.head().to_html()

        with open("result.html") as f:
            html = f.read()

        html = html.replace("{{table}}", table)
        html = html.replace("{{file}}", cleaned_name)

        return html

# Download
@app.route("/download/<filename>")
def download(filename):
    return send_file(os.path.join(CLEANED_FOLDER, filename), as_attachment=True)

# Render port fix
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)