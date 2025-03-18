from flask import Flask, render_template, request, send_file
from merger import merge_videos
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.environ.get('UPLOAD_FOLDER', 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB limit

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        original = request.files["original"]
        reaction = request.files["reaction"]
        
        # Save files
        original_path = os.path.join(app.config['UPLOAD_FOLDER'], original.filename)
        reaction_path = os.path.join(app.config['UPLOAD_FOLDER'], reaction.filename)
        original.save(original_path)
        reaction.save(reaction_path)

        # Process
        output_path = merge_videos(original_path, reaction_path)
        return send_file(output_path, as_attachment=True)
    
    return render_template("index.html")

if __name__ == "__main__":
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(host='0.0.0.0', port=10000)
