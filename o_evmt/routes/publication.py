from flask import Blueprint, request, jsonify, abort

from ..models.commentaire import Commentaire
from ..models.enterprise import Entreprise
from ..models.publication import Publication
from ..models.exposant import Exposant

publication_bp = Blueprint('publication_bp', __name__, url_prefix='/publications')


@publication_bp.route('/')
def getAll():
    posts = [post.format() for post in Publication.query.all()]

    return jsonify({
        "success": True,
        "total": len(posts),
        "publications": posts
    })


@publication_bp.route('/<creator>/<int:id>')
def make_post(creator: str, id: int):
    # checking the creator

    # TODO : Analyse if we should combine Publication and Evenemen.t

    creator = Exposant if creator is 'exposant' else Entreprise
    if Exposant.query.get(id) is not None:
        body = request.get_json()
        coordonnees = body.get('coordonnees', 'Coordonnées non renseignée')
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


@publication_bp.route("/<int:id>/comments")
# Récupérer tous les commentaires d'une publication donnée
def get_all_comments(id):
    publication = Publication.query.get(id)
    if publication is None:
        return jsonify({
            "status": 404,
            "message": "The Publication of id={} was not found".format(id)
        })
    else:
        commentaires = Commentaire.query.filter(Commentaire.publication_id == id)
        commentaire_formated = [commentaire.commentaire_format() for commentaire in commentaires]

        return jsonify(
            {
                'publication_id': id,
                'total': len(commentaire_formated),
                'commentaires': commentaire_formated
            }
        )

# @publication_bp.route('/<str:command>')
# # this route is for make our backend RQLable :) (:
# # command can in [sort, search, ]
# # route will be implemented after.
# def search_exposant(command):
#     pass
