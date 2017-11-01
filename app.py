from flask import *
import mlab
from mongoengine import *
from random import *
import uuid

mlab.connect()

app = Flask(__name__)

class Room_detail(Document):
    acess_code = StringField()
    player_name = ListField(StringField())


# class Player_detail(Document):
#     #char_image = StringField ()
#     name = StringField ()
#     role = StringField ()
#     phe = StringField()
#     ability = StringField ()

class Role (Document):
    role_name = StringField()
    role_phe = StringField()
    role_ability = StringField()

def new_room(i):
    room_code = get_room_code ()
    pn = []
    for i in range(i):
        pn.append("Player " + str(i+1))
    player_names = Room_detail(player_name = pn,
                                acess_code = room_code)
    player_names.save()

    return room_code

def get_room_code():
    code = ""
    possible = "abcdefghijklmnopqrstuvwxyz";

    for char in range(6):
        code = code + possible[randint(0,len(possible)-1)]

    return code;

room_details = Room_detail.objects()
player_details = Player_detail.objects()
roles = Role.objects()


@app.route("room/<room_id>")
def room(room_id):
    #get room data from mlab in HTML
    session["room_id"] = room_id
    if "player_id" not in session:
        session["player_id"] = uuid.uuid4().hex

        #Roll roles:
        i = randint (0,16)
        r = roles[i] #Get role
        session["player_role"] = r


    pd = session["player_role"]

    return render_template('test.html',Room_detail = Room_detail.objects(), _ = pd )

@app.route('/')
def index():
    if "room_id" not in session:
        if request.args["action"] == "create":
            # Add_player to room"
            args = request.args
            nop = args["nop"]
            room_id = add_player(int(nop))

            redirect("/room/" + room_id)

        if request.args["action"] == "join":
            room_id = request.form["room_id"]
            redirect("/room/" + room_id)
        return render_template('index.html')
    else:
        room_id = session['room_id']
        redirect("/room/" + room_id)

if __name__ == '__main__':
  app.run(debug=True)
