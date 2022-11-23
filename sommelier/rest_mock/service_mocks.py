from typing import Optional

from flask import request

from sommelier.rest_mock import app
from sommelier.rest_mock.registry import service_mock_registry
from sommelier.utils import StringUtils


@app.get("/mocks/services")
def get_service_mocks():
    data = service_mock_registry.get_services_response()
    return data, 200


@app.post("/mocks/services/form")
def create_service_mock():
    identifier = generate_id_on_none(request.form['id'])
    port = request.form['port']
    service_mock_registry.create_service(identifier, port)
    result = {
        'id': identifier,
        'port': port,
    }
    return result, 201


@app.get("/mocks/services/unsatisfied")
def get_unsatisfied_mocks():
    result = {
        'data': service_mock_registry.get_unsatisfied_endpoints()
    }
    return result, 200


@app.delete("/mocks/services/endpoints")
def delete_service_mocks():
    service_mock_registry.clear()
    return None, 204


@app.get("/mocks/services/<identifier>")
def get_service_mock(identifier):
    response = service_mock_registry.get_service_response(identifier)
    if response is None:
        return None, 404
    return response, 200


@app.delete("/mocks/services/<identifier>")
def delete_service_mock(identifier):
    service_mock_registry.delete_service(identifier)
    return None, 204


def generate_id_on_none(identifier) -> str:
    if identifier is None:
        return StringUtils.get_random_string(2)
    return identifier


def optional_integer(value) -> Optional[int]:
    if value is None:
        return None
    return int(value)
