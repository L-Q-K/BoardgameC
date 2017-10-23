from flask import *
import mlab
from mongoengine import *

mlab.connect()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', books=Book.objects())

if __name__ == '__main__':
  app.run(debug=True)
