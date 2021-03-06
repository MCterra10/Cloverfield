from cloverfield.util.orm_serializers import JSON_Goon
from cloverfield.extensions import sqlalchemy_ext
from cloverfield.settings import cfg

from flask import Flask
from elasticapm.contrib.flask import ElasticAPM

#Cloverfield API System, Reverse engineered from Goonhub.
# Made to operate with Project Clover, Beestation's modification of Goonstation.

#10-26-20, V1-RC0, Made in a little over 2 weeks.
#See settings.py for configuration options.
#RC0 has callback support for only one server.


#Import prints.
from cloverfield.blueprints import participation, secret_sauce, extras, bans, cloud, stubbed_routes, round_tracking, antags, secure, notes, exptracking, map_rotation, vpn_detection


def register_extensions(reg_app):
    sqlalchemy_ext.init_app(reg_app)

def create_app():
    app = Flask(__name__)

    app.url_map.strict_slashes = False

    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://{username}:{password}@{host}:{port}/{db}".format(
        username    = cfg["db"]["user"],
        password    = cfg["db"]["pass"],
        host        = cfg["db"]["host"],
        port        = cfg["db"]["port"],
        db          = cfg["db"]["dbname"]
    )

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #We don't use this anyways, afaik

    register_extensions(app)

    app.config['ELASTIC_APM'] = {
        'SERVICE_NAME': cfg["apm"]["name"],
        'SECRET_TOKEN': cfg["apm"]["token"],
        'SERVER_URL': cfg["apm"]["url"],
        'DEBUG': True,
        'SANITIZE_FIELD_NAMES': (
            #Infrastructure Security
            'auth',
            'api_key',
            #Player Safety
            'compID',
            'compid', #Not sure if either of these work.
            'ip',
            'cid'
        )
    }

    return app

app = create_app()
apm = None #pylint: disable=invalid-name
if cfg["apm"]["enabled"]:
    apm = ElasticAPM(app)

#Register segmented modules.
app.register_blueprint(participation.api_participation) #COMPLETE, mercifully
app.register_blueprint(secret_sauce.api_secrets)        #COMPLETE
app.register_blueprint(extras.api_extras)               #Versions/add isn't necessary to release.
app.register_blueprint(bans.api_ban)                    #COMPLETE (See secure.py for the ban panel getter)
app.register_blueprint(cloud.api_cloudhub)              #COMPLETE
app.register_blueprint(stubbed_routes.api_deadroutes)   #Explicitly unfinished.
app.register_blueprint(round_tracking.api_rounds)
app.register_blueprint(antags.api_antags)
app.register_blueprint(secure.api_secure)
app.register_blueprint(notes.api_notes)
app.register_blueprint(exptracking.api_exptrak)
app.register_blueprint(map_rotation.api_maprotation)
app.register_blueprint(vpn_detection.vpn_detection)

app.json_encoder = JSON_Goon #Overwrite the default encoder to serialize bans.

