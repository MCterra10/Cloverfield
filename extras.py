import helpers
import sqlalchemy
import neodb as db
import collections
from neodb import Session, Player
from flask import request, Blueprint, jsonify

api_extras = Blueprint('extras', __name__)

@api_extras.route('/playerInfo/getIPs/')
def get_player_ip_history():
    """
    Get the player's previous IP Addresses.
    """
    #This was actually extremely nice and clean.
    helpers.check_allowed(True)
    session: sqlalchemy.orm.Session = Session()
    #If a player gets passed to this and doesn't exist, just crash.
    player: Player = db.Player.from_ckey(request.args.get('ckey'), session)

    #TODO this code can probably be made a helper or deduped in some way
    #to be reused for the GetCIDs call.
    ip_list = list()
    for y in list(player.get_historic_inetaddr(session)):
        ip_list.append(helpers.ip_getstr(y.ip))
    ctr = collections.Counter(ip_list)
    frequency_list = list()
    for entry in list(ctr):
        frequency_list.append({"ip":entry, "times":ctr[entry]})

    frequency_list.insert(0,{"last_seen":helpers.ip_getstr(player.last_ip)})
    return jsonify(frequency_list)

@api_extras.route('/versions/add/') #VOID
def track_version():
    """
    Track user version data for analytics purposes.
    Logs to feedback-version
    """
    helpers.check_allowed(True)
    # db.conn.feedback_version()
    # db.conn.log_statement('versions/add', json.dumps(request.args))
    return jsonify('OK')
