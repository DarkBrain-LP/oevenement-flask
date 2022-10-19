from datetime import date

from flask import Blueprint, request, jsonify, abort

from ..models.domaine import Domaine
from ..models.publication import Publication
from ..models.enterprise import Entreprise

entreprise_bp = Blueprint('entreprise_bp', __name__, url_prefix='/entreprises')


# creation
@entreprise_bp.route('/', methods=['POST'])
def create():
    body = request.get_json()

    nom = body.get('nom', None)
    description = body.get('description', None)

    pays = body.get('pays', None)
    ville = body.get('ville', None)
    mail = body.get('mail', None)
    contact = body.get('contact', None)

    domaine = Domaine.query.filter(Domaine.libelle == body.get('domaine', None)).first()
    abonnement = body.get('abonnement', None)
    abonPub = body.get('abonPub', None)

    if domaine is None:
        return jsonify({
            "status": 404,
            "message": "Domain not found"
        })

    entreprise = Entreprise(nom=nom, description=description, pays=pays, ville=ville, mail=mail,
                            contact=contact, domaine_id=domaine.id, abonnement=abonnement, abonPub=abonPub,
                            )  # , idDomaine=domaine.id

    entreprise.insert()

    return jsonify(
        {
            'message': 'Exposant créé avec succes',
            'nom': nom,
            'prenom': description,
            'pays': pays,
            'ville': ville,
            'mail': mail,
            'contact': contact,
            'domaine': domaine.format(),
            'abonnement': abonnement,
            'abonPub': abonPub
        }
    )


# get all
@entreprise_bp.route('/')
def get_all():
    all = [ent.format() for ent in Entreprise.query.all()]

    return jsonify({
        'success': True,
        'total': len(all),
        'enterprises': all
    })


# get with id
@entreprise_bp.route('/<int:id>')
def get(id: int):
    ent = Entreprise.exists(id)
    if ent is not False:
        return jsonify({
            'success': True,
            'entreprise': ent.format()
        })
    else:
        return jsonify({
            "status": 404,
            "message": "Entreprise  was not found"
        })


@entreprise_bp.route('/<int:id>', methods=['DELETE'])
def delete(id: int):
    ent = Entreprise.exists(id)
    if ent is not False:
        ent.delete()
        return jsonify({
            "status": 200,
            "deletedId": id
        })
    else:
        return jsonify({
            "status": 404,
            "message": "Entreprise  was not found"
        })


@entreprise_bp.route('/<int:id>', methods=['PATCH'])
def update(id: int):
    ent = Entreprise.exists(id)
    if ent is not False:
        body = request.get_json()

        # Hard Coding
        # TODO : Create a project that will automatically generate CRUD with FLASK
        nom = body.get('nom', None)
        if nom is not None:
            ent.nom = nom
        description = body.get('description', None)
        if description is not None:
            ent.description = description
        pays = body.get('pays', None)
        if pays is not None:
            ent.pays = pays

        ville = body.get('ville', None)
        if ville is not None:
            ent.ville = ville
        mail = body.get('mail', None)
        if mail is not None:
            ent.mail = mail
        contact = body.get('contact', None)
        if contact is not None:
            ent.contact = contact

        domaine = Domaine.query.filter(Domaine.libelle == body.get('domaine', None)).first()
        if domaine is not None:
            ent.domaine_id = domaine.id
        abonnement = body.get('abonnement', None)
        if abonnement is not None:
            ent.abonnement = abonnement
        abonPub = body.get('abonPub', None)
        if abonPub is not None:
            ent.abonPub = abonPub
        ent.update()

        return jsonify({
            "status": 200,
            "entreprise": ent.format()
        })
    else:
        abort(404)


@entreprise_bp.route('/<int:id>/ok', methods=['POST'])
def toto(id:int):

    return jsonify({
        "status": True
    })

@entreprise_bp.route('/<int:id>/publications', methods=['POST'])
def make_post_(id: int):
    entreprise = Entreprise.query.get(id)
    if entreprise is not None:
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
        return jsonify({
            "status": 404,
            "message": "Entreprise  was not found"
        })
# TODO : implement search methods
# Create a post
# @entreprise_bp.route('/<int:id>/publications', methods=['POST'])
# def make_post(id: int):
#     # check if an Exposant have this id
#     if Entreprise.query.get(id) is not None:
#         body = request.get_json()
#         coordonnees = body.get('coordonnees', 'Coordonnées non renseignées')
#         lienPhoto = body.get('lienPhoto', None)
#         lienVideo = body.get('lienVideo', None)
#
#         publication = Publication(exposant_id=id, coordonnees=coordonnees, lienPhoto=lienPhoto, lienVideo=lienVideo)
#         publication.insert()
#
#         return jsonify({
#             "success": True,
#             "publication": publication.format(),
#             "total": Publication.query.count()
#         })
#     else:
#         abort(404)


# delete a post. You should pass the creator id for the security
@entreprise_bp.route('/<int:id_exposant>/publications/<int:id_publication>', methods=['DELETE'])
def delete_post(id_exposant: int, id_publication: int):
    exposant = Entreprise.query.get(id_exposant)
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
@entreprise_bp.route('/<int:id_exposant>/publications')
def get_posts_of_exposant(id_exposant: int):
    if Entreprise.exists(id_exposant):
        posts = [post.format() for post in Publication.query.filter_by(exposant_id=id_exposant)]
        return jsonify({
            'success': True,
            'total': len(posts),
            'posts': posts
        })
