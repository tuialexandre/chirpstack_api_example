import grpc
from chirpstack_api import api

# Configuration.

# This must point to the API interface.
server = "192.168.0.181:8080"

# The DevEUI for which you want to enqueue the downlink.
dev_eui = "0012f800000029a6"

# The API token (retrieved using the web-interface).
api_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJjaGlycHN0YWNrIiwiaXNzIjoiY2hpcnBzdGFjayIsInN1YiI6ImE4YWVhNDU1LWU1M2QtNDhmNi1iOTViLTUwMTkyMDQxZTgyNyIsInR5cCI6ImtleSJ9.LNrWvRzO1ap8FaKNO0btYZwJN4zJI_oCS61Bq03y4Kk"

if __name__ == "__main__":
    # Connect without using TLS.
    channel = grpc.insecure_channel(server)

    # Device-queue API client.
    client = api.DeviceServiceStub(channel)

    # Define the API key meta-data.
    auth_token = [("authorization", "Bearer %s" % api_token)]

    # Construct request.
    req = api.EnqueueDeviceQueueItemRequest()
    req.queue_item.confirmed = False
    req.queue_item.data = b"teste api"
    req.queue_item.dev_eui = dev_eui
    req.queue_item.f_port = 10

    resp = client.Enqueue(req, metadata=auth_token)

    # Print the downlink id
    print(resp.id)
