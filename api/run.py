# -*- encoding: utf-8 -*-

"""
new app
"""

from api import app, ioServer


@app.shell_context_processor
def make_shell_context():
    return {"app": app}

if __name__ == '__main__':
    # app.run(debug=False, host="0.0.0.0")
    ioServer.run(app, debug=False, host="0.0.0.0")

