import os
from os import listdir
from os.path import isfile, join
from flask import Flask, request, redirect, url_for, render_template, flash, send_from_directory
from werkzeug.utils import secure_filename
import detector


UPLOAD_FOLDER = 'static/uploads/'
PROCESS_FOLDER = 'static/processed/'

STATS_EXTENSION = '.stats'

ALLOWED_EXTENSIONS = set(['jpg','jpeg','png','gif','bmp', 'tif','webp'])
threshold = 50

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESS_FOLDER'] = PROCESS_FOLDER
app.config['STATS_EXTENSION']=STATS_EXTENSION
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.secret_key = 'my secret malaria key'
app.config['DEBUG'] = False
tolerance = 50

@app.route('/', methods=['GET','POST'])
def index():
	if request.method == 'POST':
		if 'file' not in request.files:
			flash('No file part')
			return redirect(request.url)
		file = request.files['file']
		if file.filename == '':
			flash('No selected file')
			return redirect(request.url)
		else :
			filename = secure_filename(file.filename)
			inpath = app.config['UPLOAD_FOLDER']
			outpath = app.config['PROCESS_FOLDER']
			infile = os.path.join(app.config['UPLOAD_FOLDER'], filename)
			outfile = os.path.join(app.config['PROCESS_FOLDER'], filename)
			file.save(infile)
			detector.process(infile, outfile, str(threshold))
			red, malaria = get_stats(outpath, filename)
			return render_template('result.html', input_file=inpath, output_file=outpath, filename=filename,red=red,malaria=malaria)
	else:
		return render_template('index.html')

def get_stats(outpath,filename):
        statsfile = outpath+'/'+filename+app.config['STATS_EXTENSION']
        red=0
        malaria=0
        with open(statsfile,mode='r') as f:
                  red=f.readline()
                  malaria=f.readline()
        return red,malaria

if __name__ =="__main__":
	app.run()
