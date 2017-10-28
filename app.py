from flask import *
import mlab
from mongoengine import *
from random import *


mlab.connect()

app = Flask(__name__)

class Room_detail(Document):
    player_name = ListField(StringField())

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

pn = []
for i in range(15):
    pn.append("Player " + str(i+1))
player_names = Room_detail(player_name = pn)

# player_names.save()


room_details = Room_detail.objects()
player_details = Player_detail.objects()
roles = Role.objects()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/1234')
def room():
    for j in range(20):
        for player in room_details[0]["player_name"][j]:
            i = randint(0,16)
            r = roles[i]
            p = Player_detail(name = player,
                            role = r["role_name"],
                            phe = r["role_phe"],
                            ability = r["role_ability"]).save()

    return render_template('test.html',Room_detail = Room_detail.objects(), Player_detail = Player_detail.objects())

if __name__ == '__main__':
  app.run(debug=True)
