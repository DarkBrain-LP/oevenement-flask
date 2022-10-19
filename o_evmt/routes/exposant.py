from flask import Blueprint, request, jsonify, abort
from datetime import date
from ..models.exposant import Exposant
from ..models.domaine import Domaine
from ..models.publication import Publication

exposant_bp = Blueprint("exposant_bp", __name__, url_prefix='/exposant')


@exposant_bp.route('/create', methods=["POST"])
def create():
    body = request.get_json()

    nom = body.get('nom', None)
    prenom = body.get('prenom', None)

    # TODO: Prendre la date du body
    dateNaiss = date.today()
    pays = body.get('pays', None)
    ville = body.get('ville', None)
    mail = body.get('mail', None)
    telephone = body.get('telephone', None)

    domaine = Domaine.query.filter(Domaine.libelle == body.get('domaine', None)).first()
    specialisation = body.get('specialisation', None)
    abonnement = body.get('abonnement', None)
    abonPub = body.get('abonPub', None)

    print(domaine.id)
    exposant = Exposant(nom=nom, prenom=prenom, dateNaiss=dateNaiss, pays=pays, ville=ville, mail=mail,
                        telephone=telephone, specialisation=specialisation,
                        abonnement=abonnement, abonPub=abonPub, idDomaine=domaine.id)  # , domaine_id=domaine.id
    print(exposant)
    exposant.insert()

    return jsonify(
        {
            'message': 'Exposant créé avec succes',
            'nom': nom,
            'prenom': prenom,
            'dateNaiss': dateNaiss,
            'pays': pays,
            'ville': ville,
            'mail': mail,
            'telephone': telephone,
            'domaine_id': domaine.id,
            'specialisation': specialisation,
            'abonnement': abonnement,
            'abonPub': abonPub
        }
    )


# get all Exposant
@exposant_bp.route('/')
def getAll():
    all = [exposant.format() for exposant in Exposant.query.all()]

    return jsonify(
        {
            "success": True,
            "total": Exposant.query.count(),
            "exposants": all
        }
    )


# get a specific user
@exposant_bp.route('/<int:id>')
def get(id: int):
    result = Exposant.query.get(id)
    if result is not None:
        return jsonify({
            "success": True,
            "exposant": result.format()
        })
    abort(404)


# update a Exposant
@exposant_bp.route('/<int:id>', methods=['PATCH'])
def update(id: int):
    exposant = Exposant.query.get(id)
    body = request.get_json()

    # Hard Coding
    # TODO : Create a project that will automatically generate CRUD with FLASK
    nom = body.get('nom', None)
    if nom is not None:
        exposant.nom = nom
    prenom = body.get('prenom', None)
    if prenom is not None:
        exposant.prenom = prenom
        # TODO: Prendre la date du body
    dateNaiss = date.today()
    pays = body.get('pays', None)
    if pays is not None:
        exposant.pays = pays

    ville = body.get('ville', None)
    if ville is not None:
        exposant.ville = ville
    mail = body.get('mail', None)
    if mail is not None:
        exposant.mail = mail
    telephone = body.get('telephone', None)
    if telephone is not None:
        exposant.telephone = telephone

    domaine = Domaine.query.filter(Domaine.libelle == body.get('domaine', None)).first()
    if domaine is not None:
        exposant.domaine_id = domaine.id
    specialisation = body.get('specialisation', None)
    if specialisation is not None:
        exposant.specialisation = specialisation
    abonnement = body.get('abonnement', None)
    if abonnement is not None:
        exposant.abonnement = abonnement
    abonPub = body.get('abonPub', None)
    if abonPub is not None:
        exposant.abonPub = abonPub

    exposant.update()

    return jsonify({
        "succes": True,
        "exposant": exposant.format()
    })


# Delete Exposant
@exposant_bp.route('/<int:id>', methods=['DELETE'])
def delete(id: int):
    exposant = Exposant.query.get(id)
    if exposant is not None:
        exposant.delete()
        return jsonify({
            "success": True,
            "total": Exposant.query.count()
        })
    abort(404)

# Create a post
@exposant_bp.route('/<int:id>/publications', methods=['POST'])
def make_post(id: int):
    # check if an Exposant have this id
    if Exposant.query.get(id) is not None:
        body = request.get_json()
        coordonnees = body.get('coordonnees', 'Coordonnées non renseignées')
        lienPhoto = body.get('lienPhoto', None)
        lienVideo = body.get('lienVideo', None)

        publication = Publication(exposant_id=id, coordonnees=coordonnees, lienPhoto=lienPhoto, lienVideo=lienVideo)
        publication.insert()

        return jsonify({
            "success": True,
            "publication": publication.format(),
            "total": Publication.query.count()
        })
    else:
        abort(404)


# delete a post. You should pass the creator id for the security
@exposant_bp.route('/<int:id_exposant>/publications/<int:id_publication>', methods=['DELETE'])
def delete_post(id_exposant: int, id_publication: int):
    exposant = Exposant.query.get(id_exposant)
    publication = Publication.query.get(id_publication)
    if exposant is not None and publication is not None and (publication.exposant_id is id_exposant):
        publication.delete()
        return jsonify({
            "success": True,
            "deleted_post": publication.format()
        })
    else:
        return jsonify({
            "status": 404,
            "message": "Exposant or Publication  was not found"
        })


# get Publications made by an Expostant
@exposant_bp.route('/<int:id_exposant>/publications')
def get_posts_of_exposant(id_exposant: int):
    if Exposant.exists(id_exposant):
        posts = [post.format() for post in Publication.query.filter_by(exposant_id=id_exposant)]
        return jsonify({
            'success': True,
            'total': len(posts),
            'posts': posts
        })
