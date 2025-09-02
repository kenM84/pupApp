import os
import asyncio
import sys
from flask import (Flask, redirect, render_template, request,
                   send_from_directory, url_for)



app = Flask(__name__)

@app.route('/greyscale_demo')
def greyscale_demo():
    return render_template('greyscale_index.html')

@app.route('/')
def index():
    print('Request for index page received')
    #key_agent = KeyVaultService()

    # Run async methods in a new event loop
    #loop = asyncio.new_event_loop()
    #asyncio.set_event_loop(loop)
    #try:
    #    loop.run_until_complete(key_agent.configure())
    #    dbserver = loop.run_until_complete(
    #        key_agent.get_secret("sqlDBServer"))
    #finally:
    #    loop.close()
#
    return render_template('greyscale_index.html')


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, 'static'),
        'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/hello', methods=['POST'])
def hello():
    name = request.form.get('name')

    if name:
        print('Request for hello page received with name=%s' % name)
        return render_template('hello.html', name=name)
    else:
        print('Request for hello page received with no name or blank name '
              '-- redirecting')
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
