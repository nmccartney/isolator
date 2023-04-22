import os
from flask import Flask, jsonify, request, send_from_directory
from werkzeug.utils import secure_filename
from celery import Celery
from celery.result import AsyncResult
from celery.exceptions import TimeoutError
from celery.decorators import task, periodic_task
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
app.config['UPLOAD_FOLDER'] = '/musicFiles/uploads/'
ALLOWED_EXTENSIONS = {'mp3', 'wav'}
# app.config['MAX_CONTENT_PATH']
app.config['MAX_CONTENT_LENGTH'] = 50 * 1000 * 1000  # 50MB


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)


@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return jsonify({'ok': False, 'file': request.url, 'msg': 'No file part'}), 202
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            # flash('No selected file')
            # return redirect(request.url)
            return jsonify({'ok': False, 'file': request.url, 'msg': 'no selected  file'}), 202
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return jsonify({'ok': True, 'file': filename}), 202
            # return redirect(url_for('download_file', name=filename))


# Configure Celery
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

celery = Celery(
    app.name, broker=app.config['CELERY_BROKER_URL'], backend=app.config['CELERY_RESULT_BACKEND'])
celery.conf.update(app.config)

# Define a task

#  healthcheck


@app.route('/health')
def health():
    return jsonify({'ok': True}), 202


# (typing=False, bind=True, throws=(KeyError, Exception, TimeoutError))
@celery.task
def start_isolation(x, y):
    print('test ', x, y)
    result = 1+2
    task_id = start_isolation.request.id
    # pass
    audio_loader = AudioAdapter.default()
    sample_rate = 44100
    waveform, _ = audio_loader.load(
        '/musicFiles/06-Karma_Police.mp3', sample_rate=sample_rate)

    # Perform the separation :
    try:
        prediction = separator.separate(waveform)
    except Exception as err:
        print('prediction  error ', err)
        return 0
    # prediction = separator.separate_to_file(
    # '/musicFiles/audio_example.mp3', '/musicFiles/success')
    print('prediction - ',  prediction)

    wavfile.write('/musicFiles/success/audio_example-v.wav',
                  sample_rate, prediction['vocals'])
    wavfile.write('/musicFiles/success/audio_example-a.wav',
                  sample_rate, prediction['accompaniment'])
    # async_result = AsyncResult(task_id, app=app)
    # async_result.result = prediction
    return {'ok': True}  # 'helloworld'

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


@ app.route('/task/<task_id>')
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


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
