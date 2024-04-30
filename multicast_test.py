import grpc
from chirpstack_api import api

# Configuration.

# This must point to the API interface.
server = "192.168.0.181:8080"

# The MultiCast group for which you want to enqueue the downlink.
multicast_group_id = "c781c15b-d988-4080-b16f-b3200886c906"

# The API token (retrieved using the web-interface).
api_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJjaGlycHN0YWNrIiwiaXNzIjoiY2hpcnBzdGFjayIsInN1YiI6ImE4YWVhNDU1LWU1M2QtNDhmNi1iOTViLTUwMTkyMDQxZTgyNyIsInR5cCI6ImtleSJ9.LNrWvRzO1ap8FaKNO0btYZwJN4zJI_oCS61Bq03y4Kk"

if __name__ == "__main__":
    # Connect without using TLS.
    channel = grpc.insecure_channel(server)

    # Device-queue API client.
    client = api.MulticastGroupServiceStub(channel)

    # Define the API key meta-data.
    auth_token = [("authorization", "Bearer %s" % api_token)]

    # Construct request.
    req = api.EnqueueMulticastGroupQueueItemRequest()
    req.queue_item.data = b"teste multicast"
    req.queue_item.multicast_group_id = multicast_group_id
    req.queue_item.f_port = 10

    resp = client.Enqueue(req, metadata=auth_token)

    # Print the downlink id
    print(resp.f_cnt)
