import grpc
from chirpstack_api import api


class DeviceUtil:
    def __init__(self, api_token, server="localhost:8080"):
        self.server = server
        self.api_token = api_token
        self.auth_token = [("authorization", "Bearer %s" % self.api_token)]

        # Connect without using TLS.
        channel = grpc.insecure_channel(self.server)

        # Device-queue API client.
        self.client = api.DeviceServiceStub(channel)

    def create(
        self,
        application_id,
        dev_eui,
        name,
        device_profile_id,
        description="",
        skip_fcnt_check=False,
        is_disabled=False,
        variables={},
        tags={},
        join_eui="",
    ):
        req = api.CreateDeviceRequest()
        req.device.dev_eui = dev_eui
        req.device.name = name
        req.device.description = description
        req.device.application_id = application_id
        req.device.device_profile_id = device_profile_id
        req.device.skip_fcnt_check = skip_fcnt_check
        req.device.is_disabled = is_disabled
        for key, variable in variables.items():
            req.device.variables[key] = variable
        for key, tag in tags.items():
            req.device.variables[key] = tag
        if len(join_eui) > 0:
            req.device.join_eui = join_eui
        return self.client.Create(req, metadata=self.auth_token)

    def delete(self, dev_eui):
        req = api.DeleteDeviceRequest()
        req.dev_eui = dev_eui
        return self.client.Delete(req, metadata=self.auth_token)

    def activate(
        self,
        dev_eui,
        dev_addr,
        app_s_key,
        ntw_s_key,
        uplink_fc=0,
        ntw_downlink_fc=0,
        serving_ntw_s_int_key="",
        forwarding_ntw_s_int_key="",
        app_downlink_fc=0,
    ):
        req = api.ActivateDeviceRequest()
        req.device_activation.dev_eui = dev_eui
        req.device_activation.dev_addr = dev_addr
        req.device_activation.app_s_key = app_s_key
        req.device_activation.nwk_s_enc_key = ntw_s_key

        # LoraWan 1.0.3 ABP should not need theses guys to be provided, but currently device activation won't work if not set due to gRPC API internal handlying
        if len(serving_ntw_s_int_key) > 0:
            req.device_activation.s_nwk_s_int_key = serving_ntw_s_int_key
        else:
            req.device_activation.s_nwk_s_int_key = ntw_s_key

        if len(forwarding_ntw_s_int_key) > 0:
            req.device_activation.f_nwk_s_int_key = forwarding_ntw_s_int_key
        else:
            req.device_activation.f_nwk_s_int_key = ntw_s_key

        req.device_activation.f_cnt_up = uplink_fc
        req.device_activation.n_f_cnt_down = ntw_downlink_fc
        req.device_activation.a_f_cnt_down = app_downlink_fc
        return self.client.Activate(req, metadata=self.auth_token)

    def deactivate(self, dev_eui):
        req = api.DeactivateDeviceRequest()
        req.dev_eui = dev_eui
        return self.client.Deactivate(req, metadata=self.auth_token)

    def enqueue(self, dev_eui, payload, f_port=10, confirmed=False):
        req = api.EnqueueDeviceQueueItemRequest()
        req.queue_item.confirmed = confirmed
        req.queue_item.data = payload
        req.queue_item.dev_eui = dev_eui
        req.queue_item.f_port = f_port
        return self.client.Enqueue(req, metadata=self.auth_token)

    def get_activation(self, dev_eui):
        req = api.GetDeviceActivationRequest()
        req.dev_eui = dev_eui
        return self.client.GetActivation(req, metadata=self.auth_token)
