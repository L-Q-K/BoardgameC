from flask import *
import mlab
from mongoengine import *
from random import *


mlab.connect()

app = Flask(__name__)

class Room_detail(Document):
    player_name = ListField()

class Player_detail(Document):
    #char_image = StringField ()
    name = StringField ()
    role = StringField ()
    phe = StringField()
    ability = StringField ()

class Role (Document):
    role_name = StringField()
    role_phe = StringField()
    role_ability = StringField()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/1234')
def room():
    return render_template('test.html',Room_detail = Room_detail.objects())#, Player_detail = Player_detail.objects())

if __name__ == '__main__':
  app.run(debug=True)
