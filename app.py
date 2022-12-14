from flask import Flask, render_template, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
import getRank
import urllib.request
 
app = Flask(__name__)
 
UPLOAD_FOLDER = 'files'
 
app.secret_key = "raji"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
 
ALLOWED_EXTENSIONS = set(['pdf'])
 
def allowed_file(filename):
 return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
  
@app.route('/')
def upload():
 return render_template('upload.html')

@app.route('/rank')
def rank():
  rank = getRank.rank()
  return render_template('rank.html', len = len(rank), rankList = rank)
 
@app.route('/', methods=['POST'])
def upload_file():
 if request.method == 'POST':
        # check if the post request has the files part
  if 'files[]' not in request.files:
   flash('No file part')
   return redirect(request.url)
  files = request.files.getlist('files[]')
  uploadSuccess=True
  for file in files:
   if file and allowed_file(file.filename):
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
   else:
    uploadSuccess=False
  if uploadSuccess:
    flash('File(s) successfully uploaded')
  else:
    flash("Upload in PDF format")
  return redirect('/')
   
if __name__ == '__main__':
 app.run(debug=True)