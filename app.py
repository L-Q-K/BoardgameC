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

class Role (Document):
    role_name = StringField()
    role_phe = StringField()
    role_ability = StringField()

def get_room_code():
    code = ""
    possible = "abcdefghijklmnopqrstuvwxyz";

    for char in range(6):
        code = code + possible[randint(0,len(possible)-1)]

    print(code)

    return code

room_details = Room_detail.objects()
roles = Role.objects()

app.config["SECRET_KEY"] = "43xf$=DLmQdhWVN*-Yg!s^NM-N&P8WedV"

@app.route("/room/<room_code>")
def room(room_code):
    #get room data from mlab in HTML
    session["room_code"] = room_code

    if "player_id" not in session:
        session["player_id"] = uuid.uuid4().hex

        #Roll roles:
        i = randint (0,16)
        r = roles[i] #Get role
        session["player_role"] = r["role_name"]
        session["player_phe"] = r["role_phe"]
        session["player_ability"] = r["role_ability"]


    pd = {
        "role_name" : session["player_role"],
        "role_phe" : session["player_phe"],
        "role_ability" : session["player_ability"]
    }

    return render_template('room_test.html',Room_detail = Room_detail.objects(acess_code= room_code).first(), pds = pd )

@app.route('/')
def index():

    if "room_code" not in session:
        if "Create" in request.args:
            #Add_player to room:
            nop = request.args["nop"]
            room_code = get_room_code()
            pn = []
            for i in range(int(nop)):
                pn.append("Player " + str(i+1))
            player_names = Room_detail(player_name = pn,
                                            acess_code = room_code)
            player_names.save()

            session["room_code"] = room_code

            return redirect("/room/" + room_code)
        elif "Join" in request.form:
             room_code = request.form["room_code"]

             return redirect("/room/" + room_code)

        return render_template("index.html")
    else:
        room_code = session['room_code']
        return redirect("/room/" + room_code)

if __name__ == '__main__':
  app.run(debug=True)
