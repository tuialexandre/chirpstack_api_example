import grpc
from chirpstack_api import api

# Configuration.

# This must point to the API interface.
server = "localhost:8080"

# The MultiCast group for which you want to enqueue the downlink.
multicast_group_id = "..."

# The API token (retrieved using the web-interface).
api_token = "..."

if __name__ == "__main__":
    # Connect without using TLS.
    channel = grpc.insecure_channel(server)

    # Device-queue API client.
    client = api.MulticastGroupServiceStub(channel)

    # Define the API key meta-data.
    auth_token = [("authorization", "Bearer %s" % api_token)]

    # Construct request.
    req = api.EnqueueMulticastGroupQueueItemRequest()
    req.queue_item.data = b"payload msg"
    req.queue_item.multicast_group_id = multicast_group_id
    req.queue_item.f_port = 10

    resp = client.Enqueue(req, metadata=auth_token)

    # Print the downlink frame counter
    print(resp.f_cnt)
