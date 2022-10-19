from flask import Blueprint, request, jsonify, abort

from ..models.client import Client
from ..models.commentaire import Commentaire
from ..models.exposant import Exposant
from ..models.message import Message

message_bp = Blueprint("message_bp", __name__, url_prefix="/message")


@message_bp.route('/', methods=["POST"])
def add():
    body = request.get_json()

    client_id = body.get("client_id")
    exposant_id = body.get("exposant_id")
    text = body.get("texte")
    lienPhoto = body.get("lienPhoto")
    lienVideo = body.get("lienVideo")

    if Client.exists(client_id) is not False and Exposant.exists(exposant_id):
        if text != '':
            message = Message(client_id=client_id, exposant_id=exposant_id, texte=text, lienPhoto=lienPhoto,
                              lienVideo=lienVideo)
            message.insert()

            return jsonify({
                "success": True,
                "message": "message added with success"
            })
        else:
            return jsonify({
                "success": False,
                "message": "please message text must not be empty"
            })
    else:
        return jsonify({
            "sucees": False,
            "message": "it seems that exposant or client not found"
        })


@message_bp.route("/<int:id_client>/<int:id_exposant>")
def get_chat(id_client: int, id_exposant: int):
    return jsonify({
        "success": True,
        "messages": [message.format() for message in
                     Message.query.filter_by(id_client=id_client, id_exposant=id_exposant)]
    })


@message_bp.route("/<int:id_client>/<int:id_exposant>/<int:id_message>", methods=["DELETE"])
def delete(id_client: int, id_exposant: int, id_message: int):
    message = Message.has_right_access(id_message, id_client, id_exposant)
    if message is not False:
        message.delete()
        return jsonify({
            "success": True,
            "message": "message was successfully deleted"
        })
    else:
        return jsonify({
            "success": False,
            "message": "Message does not exists or users you add to the query don't have right access"
        })
