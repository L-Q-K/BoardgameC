from flask import *
import mlab
from mongoengine import *
from random import *
# from image import *
import uuid

mlab.connect()

app = Flask(__name__)

class Room_detail(Document):
    acess_code = StringField()
    current_player = IntField()
    max_player = IntField()
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

        room_details = Room_detail.objects(acess_code = room_code).first()
        if room_details is not None:
            if room_details["current_player"] + 1 <= room_details["max_player"]: # Nếu còn slot
                new_current_player = room_details["current_player"] + 1
                new_player_names = room_details["player_name"]
                new_player_names.append("Player" + str(new_current_player))
                print(new_player_names)
                room_details.update(set__current_player = new_current_player,set__player_name = new_player_names )

                return redirect("/room/" + room_code)
            else:
                return "Room does not exist"



    pd = {
        "role_name" : session["player_role"],
        "role_phe" : session["player_phe"],
        "role_ability" : session["player_ability"]
    }
    if "Out" in request.args or "Index" in request.args:
        session.clear()
        #Delete player:
        room_details = Room_detail.objects(acess_code = room_code).first()
        if room_details is not None:
            if room_details["current_player"] - 1 != 0: # Nếu k phải người cuối cùng
                new_current_player = room_details["current_player"] - 1
                new_player_names = room_details["player_name"]
                new_player_names.remove("Player" + str(new_current_player + 1))
                room_details.update(set__current_player = new_current_player,set__player_name = new_player_names )
            else:
                room_details.delete()

        return redirect('/')

    return render_template('new_room.html',Room_detail = Room_detail.objects(acess_code= room_code).first(), pds = pd )

@app.route('/')
def index():
    if "room_code" not in session:
        if "Create" in request.args:
            #Add_player to room:
            nop = request.args["nop"]
            room_code = get_room_code()

            if int(nop) > 0:
                #Add this player:
                pn = []
                pn.append("Player 1 ")
                player_names = Room_detail(player_name = pn,
                                            current_player = 1,
                                            max_player = nop,
                                            acess_code = room_code)
                player_names.save()

                session["room_code"] = room_code

                return redirect("/room/" + room_code)
            else:
                abort(400)
        elif "join" in request.args:
            room_code = request.args["room_code"]
            if room_code == "":
                abort(400)
            else:
                session["room_code"] = room_code

                #Add new player:
                room_details = Room_detail.objects(acess_code = room_code).first()
                if room_details is not None:
                    if room_details["current_player"] + 1 <= room_details["max_player"]: # Nếu còn slot
                        new_current_player = room_details["current_player"] + 1
                        new_player_names = room_details["player_name"]
                        new_player_names.append("Player" + str(new_current_player))
                        room_details.update(set__current_player = new_current_player,set__player_name = new_player_names )

                    return redirect("/room/" + room_code)
                else:
                    return "Room doesn't exist"

        return render_template("homepage.html")
    else:
        room_code = session['room_code']
        return redirect("/room/" + room_code)

@app.route('/homepage')
def homepage():
    return render_template('homepage.html')

if __name__ == '__main__':
  app.run(debug=True)
