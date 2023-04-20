from flask import Flask, jsonify
from celery import Celery
from celery.result import AsyncResult
from celery.exceptions import TimeoutError
from celery.decorators import task, periodic_task
from spleeter.separator import Separator
# Use audio loader explicitly for loading audio waveform :
from spleeter.audio.adapter import AudioAdapter

# Using embedded configuration.
separator = Separator('spleeter:2stems')

# Using custom configuration file.
# separator = Separator('/path/to/config.json')

app = Flask(__name__)

# Configure Celery
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
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
        '/musicFiles/AM-02-01_Riot_Van.wav', sample_rate=sample_rate)

    # Perform the separation :
    prediction = separator.separate(waveform)

    async_result = AsyncResult(task_id, app=app)
    async_result.result = prediction
    return result  # 'helloworld'

# Route to trigger the task


@app.route('/isolate')
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


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
