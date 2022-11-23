from typing import List, Optional

from sommelier.rest_mock.registry.application_runner import ApplicationRunner
from sommelier.rest_mock.registry.endpoints_mock_registry import EndpointsMockRegistry


class ServiceMock(object):

    def __init__(self, identifier, port, service) -> None:
        self.id = identifier
        self.port = port
        self.server = service
        self.endpoint_registry = EndpointsMockRegistry(service)

    def summary(self) -> dict:
        return {
            'id': self.id,
            'port': self.port,
            'summary': self.endpoint_registry.get_summary(),
        }


class ServiceMockRegistry(object):

    def __init__(self) -> None:
        self.services = {}

    def create_service(self, identifier, port):
        if identifier in self.services:
            # service with this identifier already is created
            # no-op
            return
        service = ApplicationRunner(identifier, port)
        service.start_daemon()
        self.services[identifier] = ServiceMock(identifier, port, service)

    def get_services_response(self) -> List[dict]:
        result = []
        for v in self.services.values():
            result.append(v.summary())
        return result

    def get_service_response(self, identifier):
        if identifier not in self.services:
            return None
        v = self.services[identifier]
        return v.summary()

    def get_service(self, identifier) -> Optional[EndpointsMockRegistry]:
        if identifier not in self.services:
            return None
        v = self.services[identifier]
        return v.endpoint_registry

    def clear(self):
        for v in self.services.values():
            v.endpoint_registry.clear()

    def delete_service(self, identifier):
        if identifier not in self.services:
            return
        v = self.services[identifier]
        v.server.stop_daemon()
        del self.services[identifier]

    def get_unsatisfied_endpoints(self) -> List[dict]:
        result = []
        for v in self.services.values():
            element = v.endpoint_registry.get_unsatisfied()
            result.append(element)
        return result
