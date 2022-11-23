from flask import request

from sommelier.rest_mock import app
from sommelier.rest_mock.registry import service_mock_registry
from sommelier.rest_mock.service_mocks import generate_id_on_none


@app.get("/mocks/services/<service_id>/endpoints")
def get_endpoint_mocks(service_id):
    result = service_mock_registry.get_service(service_id).get_summary()
    return result, 200


@app.post("/mocks/services/<service_id>/endpoints/form")
def create_endpoint_mock(service_id):
    identifier = generate_id_on_none(request.form['id'])
    operation = request.form['operation']
    url = request.form['url']
    status_code = request.form['statusCode']
    mocked_service = service_mock_registry.get_service(service_id)
    mocked_service.create_endpoint(identifier, operation, url, status_code)
    result = mocked_service.get_endpoint(identifier)
    return result, 201


@app.get("/mocks/services/<service_id>/endpoints/<identifier>")
def get_endpoint_mock(service_id, identifier):
    result = service_mock_registry.get_service(service_id).get_endpoint(identifier)
    return result, 200


@app.put("/mocks/services/<service_id>/endpoints/<identifier>")
def update_endpoint_mock(service_id, identifier):
    endpoint = service_mock_registry.get_service(service_id).get_endpoint(identifier)
    endpoint.redefine_contract(
        headers=(request.form["headers"]),
        req=(request.form["request"]),
        res=(request.form["response"]),
        expected_num_calls=(request.form["expectedNumCalls"]),
        status_code=(request.form["statusCode"])
    )
    return endpoint, 200


@app.delete("/mocks/services/<service_id>/endpoints/<identifier>")
def delete_endpoint_mock(service_id, identifier):
    service_mock_registry.get_service(service_id).delete_endpoint(identifier)
    return None, 204
