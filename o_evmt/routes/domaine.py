from flask import Blueprint, request, jsonify, abort
from ..models.domaine import Domaine

domaine_bp = Blueprint("domaine_bp", __name__, url_prefix='/domaine')


@domaine_bp.route('/')
def getAll():
    return jsonify({
        "success": True,
        "domains": [domain.format() for domain in Domaine.query.all()]
    })

@domaine_bp.route('/', methods=['POST'])
def create():
    body = request.get_json()
    libelle = body.get('libelle', None)
    domaine = Domaine(libelle=libelle)
    domaine.insert()

    return jsonify(
        {
            'message': 'Domaine crée avec succes',
            'libelle': libelle
        }
    )

@domaine_bp.route('/addRange', methods=['POST'])
def addRange():
    body = request.get_json()
    # libelle = body.get('libelle', None)
    # domaine = Domaine(libelle=libelle)
    # domaine.insert()
    all = body.get('domains')
    domains = []
    print(type(all))
    for el in all:
        libelle = el.get('libelle')
        if libelle is not None:
            domain = Domaine(libelle)
            domains.append(domain)

    message = ""
    inserted = Domaine.insertRange(domains)
    if inserted > 0:
        message = f"{inserted} domaines enregistrés avec succes"
    else :
        message = "Une erreur s'est produite, les domaines ne sont pas enregistrés"

    return jsonify(
        {
            'message': message,
            'success': True,
            'inserted': [dom.format() for dom in domains]
            # 'libelle': libelle
        }
    )
