from flask import Blueprint, request, make_response

from app.core import authorize, EndpointValidators, AdminBo

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/get-users', methods=['POST'])
@authorize
def get_users():

    information, error_response, status_code = EndpointValidators.validata_role_request(request)
    if error_response:
        return error_response, status_code

    response = AdminBo.get_users(information)
    return make_response(response)


@admin_bp.route('/get-messages', methods=['POST'])
@authorize
def get_messages():

    information, error_response, status_code = EndpointValidators.validata_role_request(request)
    if error_response:
        return error_response, status_code

    response = AdminBo.get_messages(information)
    return make_response(response)


@admin_bp.route('/get-suggestions', methods=['POST'])
@authorize
def get_suggestions():

    information, error_response, status_code = EndpointValidators.validata_role_request(request)
    if error_response:
        return error_response, status_code

    response = AdminBo.get_suggestions(information)
    return make_response(response)
