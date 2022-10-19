from flask import Blueprint, request, jsonify, abort

from ..models.commentaire import Commentaire
from ..models.personne import Personne
from ..models.publication import Publication

commentaire_bp = Blueprint("commentaire_bp", __name__, url_prefix="/commentaires")


@commentaire_bp.route('/', methods=['POST'])
def create():
    body = request.get_json()

    texte_com = body.get('texteCom', None)
    lien_photo = body.get('lienPhoto', None)
    client_id = body.get('client_id', None)
    publication_id = body.get('publication_id', None)
    checked_person = Personne.query.get(client_id)
    checked_post = Publication.query.get(publication_id)

    if checked_person is None and checked_post is None:
        return jsonify({
            "status": 404,
            "message": "Person or Publication  was not found"
        })

    commentaire = Commentaire(client=client_id, publication=publication_id, commentaire=texte_com, photo=lien_photo)

    commentaire.insert()

    return jsonify(
        {
            'status': 200,
            'commentaire': commentaire.commentaire_format()
        }
    )


@commentaire_bp.route("/<int:id>/update", methods=['PATCH'])
def update(id):
    commentaire = Commentaire.query.get(id)
    if commentaire is None:
        abort(404)
    else:
        try:
            body = request.get_json()
            commentaire.texteCom = body.get('texteCom')
            commentaire.lienPhoto = body.get('lienPhoto')
            commentaire.update()

            return jsonify(
                {
                    'commentaire': commentaire.commentaire_format()
                }
            )
        except:
            abort(406)


@commentaire_bp.route("/<int:id>/delete", methods=['DELETE'])
def delete(id):
    commentaire = Commentaire.query.get(id)
    if commentaire is None:
        abort(404)
    else:
        commentaire.delete()
        return {
            'message': 'Commentaire supprimé avec succès'
        }
