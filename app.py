from flask import Flask, jsonify
from celery import Celery
from celery.result import AsyncResult
from celery.exceptions import TimeoutError

app = Flask(__name__)

# Configure Celery
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

# Define a task


@celery.task
def start_isolation(x, y):
    result = x + y
    task_id = start_isolation.request.id
    async_result = AsyncResult(task_id, app=app)
    async_result.result = result
    return result

# Route to trigger the task


@app.route('/isolate')
def trigger_isolation():
    task = start_isolation.delay('example@example.com',
                                 'Hello', 'This is a test email')
    return jsonify({'task_id': task.id}), 202

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
    app.run()
