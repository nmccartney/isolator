import os
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
from celery import Celery
from celery.result import AsyncResult
from celery.exceptions import TimeoutError
from celery.decorators import task, periodic_task
from datetime import datetime
import json
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Sample(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    filename = db.Column(db.String(32), nullable=False)
    task = db.Column(db.String(64), nullable=False)
    files = db.Column(db.JSON(), nullable=True)
    date_joined = db.Column(db.DateTime(), default=datetime.utcnow)

    def __repr__(self):
        return f"Sample {self.filename}"

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as err:
            print('Error: ', err)

    def  remove(self):
        Sample.query.filter_by(id = self.id).delete()
        db.session.commit()

    def update_filename(self, new_filename):
        self.filename = new_filename

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)

    @classmethod
    def get_by_filename(cls, filename):
        return cls.query.filter_by(filename=filename).first()

    @classmethod
    def get_by_task(cls, task):
        return cls.query.filter_by(task=task).first()

    def toDICT(self):

        cls_dict = {}
        cls_dict['_id'] = self.id
        cls_dict['filename'] = self.filename
        cls_dict['task'] = self.task
        cls_dict['files'] = self.files

        return cls_dict

    def toJSON(self):

        return self.toDICT()

from spleeter.separator import Separator
# Use audio loader explicitly for loading audio waveform :
from spleeter.audio.adapter import AudioAdapter
import scipy.io.wavfile as wavfile

# Using embedded configuration.
separator = Separator('spleeter:2stems')

# Using custom configuration file.
# separator = Separator('/path/to/config.json')

app = Flask(__name__)


# File  upload   config
app.config['UPLOAD_FOLDER'] = '/musicFiles/'
ALLOWED_EXTENSIONS = {'mp3', 'wav'}
# app.config['MAX_CONTENT_PATH']
app.config['MAX_CONTENT_LENGTH'] = 50 * 1000 * 1000  # 50MB

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')
SQLALCHEMY_TRACK_MODIFICATIONS = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS

db.init_app(app)
# Setup database
@app.before_first_request
def initialize_database():
    try:
        db.create_all()
    except Exception as e:

        print('> Error: DBMS Exception: ' + str(e) )

        # fallback to SQLite
        BASE_DIR = os.path.abspath(os.path.dirname(__file__))
        app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')

        print('> Fallback to SQLite ')
        db.create_all()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)

@app.route('/v1/samples/<sample_id>', methods=['GET', 'DELETE'])
def req_sample(sample_id):
    if request.method == 'GET':
        return  jsonify({'ok': True}), 202
    if request.method == 'DELETE':
        try:
            remove_sample =  Sample.get_by_id(sample_id)
            remove_sample.remove()
            # remove_sample.save()
        except Exception as err:
            print ('error: ', err)
            return  jsonify({'ok': False}), 202
        return  jsonify({'ok': True}), 202

@app.route('/v1/samples', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'GET':
        samples = Sample.query.all()
        sample_list = []
        for sample in samples:
            sample_dict = sample.toJSON()
            sample_list.append(sample_dict)
        return  jsonify({'ok': True, 'results': sample_list}), 202
    if request.method == 'POST':
        print('files ', request.files.get('file'))
        # check if the post request has the file part
        if 'file' not in request.files:
            return jsonify({'ok': False, 'file': request.url, 'msg': 'No file part'}), 202
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            return jsonify({'ok': False, 'file': request.url, 'msg': 'no selected  file'}), 202
        if file and allowed_file(file.filename):
            try:
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                # return jsonify({'ok': True, 'file': filename}), 202
            except Exception as  err:
                return   {'ok':false,'msg':err}
            # return redirect(url_for('download_file', name=filename))
            print('got  saved file')
            try:
                filename = secure_filename(file.filename)

                task = start_isolation.delay(filename, 1)

                print('....isolating ',  task.id)

                new_sample = Sample()
                new_sample.filename = filename
                new_sample.task = task.id
                new_sample.save()
                return jsonify({'ok':True,'file': filename, 'sample':new_sample.id})
            except Exception as  err:
                return   jsonify({'ok':False,'msg':err})
            except KeyError  as err:
                return  jsonify({'ok':False,'msg':err})
            except TypeError  as err:
                return  jsonify({'ok':False,'msg':err})
            # finally:
            #     return  jsonify({'ok':False,'msg':'didnt save'})

# Configure Celery
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

celery = Celery(
    app.name, broker=app.config['CELERY_BROKER_URL'], backend=app.config['CELERY_RESULT_BACKEND'])
celery.conf.update(app.config)

# from api.api.models import db

#  healthcheck


@app.route('/health')
def health():
    return jsonify({'ok': True}), 202


# (typing=False, bind=True, throws=(KeyError, Exception, TimeoutError))
@celery.task
def start_isolation(filename, sample_id):
    print('test ', filename, sample_id)
    # result = 1+2
    task_id = start_isolation.request.id
    # pass
    audio_loader = AudioAdapter.default()
    sample_rate = 44100
    waveform, _ = audio_loader.load(
        '/musicFiles/'+filename, sample_rate=sample_rate)

    # Perform the separation :
    try:
        prediction = separator.separate(waveform)
    except Exception as err:
        print('prediction  error ', err)
        return 0
    # prediction = separator.separate_to_file(
    # '/musicFiles/audio_example.mp3', '/musicFiles/success')
    print('prediction - ',  prediction)
    vocals = '/musicFiles/success/'+os.path.splitext(filename)[0]+'_vocals.wav'
    accompaniment = '/musicFiles/success/'+os.path.splitext(filename)[0]+'_accompaniment.wav'
    wavfile.write(vocals,  sample_rate, prediction['vocals'])
    wavfile.write(accompaniment, sample_rate, prediction['accompaniment'])
    # async_result = AsyncResult(task_id, app=app)
    # async_result.result = prediction
    # try:
    #     new_sample  = Sample.get_by_task(task_id)
    #     if new_sample:
    #         new_sample.files =  [vocals,accompaniment]
    #         new_sample.save()
    # except Exception as err:
    #     print('worker err - ',err)
    print('files - ', sample_id, [vocals,accompaniment])
    return {'ok': True, 'files':[vocals,accompaniment]}  # 'helloworld'

# Route to trigger the task


@ app.route('/isolate')
def trigger_isolation():
    print('...testing  route isolate...')
    # return jsonify({'ok': False})
    try:
        print('test---')
        # return jsonify({'ok': False})
        task = start_isolation.delay(1, 1)

        print('....isolating ',  task.id)

        return jsonify({'task_id': task.id})

    except Exception as e:  # work on python 3.x
        print('Failed to run isolator: ' + str(e))

        return jsonify({'ok': False})
    # finally:
    #     return jsonify({'ok': False})
    # pass


# Route to check the status of a task


@app.route('/task/<task_id>')
def check_task_status(task_id):
    task = AsyncResult(task_id, app=celery)
    if task.state == 'SUCCESS':
        return jsonify({'status': task.state, 'result': task.result})
    elif task.state == 'PENDING':
        return jsonify({'status': task.state})
    elif task.state == 'FAILURE':
        return jsonify({'status': task.state, 'error': str(task.result)})
    else:
        return jsonify({'status': task.state})

CORS(app)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
