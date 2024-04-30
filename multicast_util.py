import grpc
from chirpstack_api import api


class MulticastUtil:
    def __init__(self, multicast_group_id, api_token, server="localhost:8080"):
        self.server = server
        self.multicast_group_id = multicast_group_id
        self.api_token = api_token
        self.auth_token = [("authorization", "Bearer %s" % self.api_token)]

        # Connect without using TLS.
        channel = grpc.insecure_channel(self.server)

        # Device-queue API client.
        self.client = api.MulticastGroupServiceStub(channel)

    def enqueue(self, payload, f_port=10):
        # Construct request.
        req = api.EnqueueMulticastGroupQueueItemRequest()
        req.queue_item.data = payload
        req.queue_item.multicast_group_id = self.multicast_group_id
        req.queue_item.f_port = f_port

        # Return response
        return self.client.Enqueue(req, metadata=self.auth_token)

    def add_device(self, dev_eui):
        req = api.AddDeviceToMulticastGroupRequest()
        req.multicast_group_id = self.multicast_group_id
        req.dev_eui = dev_eui

        return self.client.AddDevice(req, metadata=self.auth_token)

    def remove_device(self, dev_eui):
        req = api.RemoveDeviceFromMulticastGroupRequest()
        req.multicast_group_id = self.multicast_group_id
        req.dev_eui = dev_eui

        return self.client.RemoveDevice(req, metadata=self.auth_token)

    def add_gateway(self, gateway_id):
        req = api.AddGatewayToMulticastGroupRequest()
        req.multicast_group_id = self.multicast_group_id
        req.gateway_id = gateway_id

        return self.client.AddGateway(req, metadata=self.auth_token)

    def remove_gateway(self, gateway_id):
        req = api.RemoveGatewayFromMulticastGroupRequest()
        req.multicast_group_id = self.multicast_group_id
        req.gateway_id = gateway_id

        return self.client.RemoveGateway(req, metadata=self.auth_token)
