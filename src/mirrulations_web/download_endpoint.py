from flask import Flask, send_file
from flask import request, render_template
import mirrulations_web.download_processor as download_processor

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':  # this block is only entered when the form is submitted
        docid = request.form.get('DirId')
        return send_file(download_processor.download_zip(docid), attachment_filename=docid + '.zip', as_attachment=True)

    return render_template("index.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0')

