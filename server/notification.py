
from apns2.client import APNsClient
from apns2.payload import Payload

# https://github.com/Pr0Ger/PyAPNs2
class NotificationService:

    def __init__(self):
        self.topic = 'com.example.App'
        # TODO: replace with db lookup so token hex can be mapped for each device.
        self.token_hex = 'b5bb9d8014a0f9b1d61e21e796d78dccdf1352f23cd32812f4850b87'
        self.client = None
        # self.client = APNsClient('key.pem', use_sandbox=False, use_alternative_port=False)

    def send_notification(self, message="Hello World!"):
        payload = Payload(alert=message, sound="default", badge=1)
        # self.client.send_notification(self.token_hex, payload, self.topic)
        print('send notification payload', payload)