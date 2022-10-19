from flask import Blueprint, request, jsonify, abort
from datetime import date

from ..models.client import Client

client_bp = Blueprint("client_bp", __name__, url_prefix='/client')
#
#
@client_bp.route('/create', methods=["POST"])
def create():
    body = request.get_json()

    nom = body.get('nom', None)
    prenom = body.get('prenom', None)
    # dateNaiss = datetime.strptime(body.get('dateNaiss', None), '%d/%m/%y')
    # dateNaiss = body.get('dateNaiss', None)
    dateNaiss = date.today()
    pays = body.get('pays', None)
    ville = body.get('ville', None)
    mail = body.get('mail', None)

    telephone = body.get('telephone', None)
    profession = body.get('profession', None)

    client = Client(nom=nom, prenom=prenom, dateNaiss=dateNaiss, pays=pays, ville=ville, mail=mail,
                    telephone=telephone, profession=profession)

    client.insert()

    return jsonify(
        {
            'message': "Client crée avec succès",
            'nom': nom,
            'prenom': prenom,
            'dateNaiss': dateNaiss,
            'pays': pays,
            'ville': ville,
            'mail': mail,
            'telephone': telephone,
            'profession': profession
        }
    )


@client_bp.route('/<int:id>')
def get_client(id):
    client = Client.query.get(id)
    if client is None:
        abort(404)
    else:
        return jsonify(
            {
                'client': client.client_format
            }
        )


@client_bp.route('/<int:id>', methods=["PUT"])
def update_client(id):
    client = Client.query.get(id)
    if client is None:
        abort(404)
    else:
        try:

            body = request.get_json()
            client.nom = body.get('nom')
            client.prenom = body.get('prenom')
            client.dateNaiss = body.get('dateNaiss')
            client.pays = body.get('pays')
            client.ville = body.get('ville')
            client.mail = body.get('mail')
            client.telephone = body.get('telephone')
            client.profession = body.get('profession')
            client.update()

            return jsonify(
                {
                    'client': client.client_format()
                }
            )
        except:
            abort(406)


@client_bp.route('/<int:id>', methods=["PUT"])
def delete_client(id):
    client = Client.query.get(id)
    if client is None:
        abort(404)
    else:
        client.delete()
        return {
            'message': 'Client supprimé avec succès'
        }
