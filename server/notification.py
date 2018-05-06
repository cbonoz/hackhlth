
# from apns import APNs, Frame, Payload
from apns2.client import APNsClient
from apns2.payload import Payload
# from pushjack import APNSClient

DEV_CERT_FILE = "./apns-dev.pem"
KEY_FILE = "./apns-dev-key-noenc.pem"
PROD_CERT_FILE = "./apns-prod.pem"

DEFAULT_TOKEN = 'f7ca3b57016e6882fe11b7253e16b2068bdee0f119800b4271456bb04e896149'
# DEFAULT_TOKEN =

# https://github.com/Pr0Ger/PyAPNs2
class NotificationService:

    def __init__(self):
        self.topic = 'com.epage.QuietMind'
        self.token_map = {}
        self.client = APNsClient(DEV_CERT_FILE, use_sandbox=True, use_alternative_port=False)
        # self.apns = APNs(use_sandbox=True, cert_file=CERT_FILE, key_file=KEY_FILE)
        # self.apns = APNs(use_sandbox=True, cert_file=CERT_FILE, enhanced=True)
        # self.client = APNSClient(certificate=CERT_FILE,
        #                     default_error_timeout=10,
        #                     default_expiration_offset=2592000,
        #                     default_batch_size=100,
        #                     default_retries=3)

    def register_token(self, userId, token):
        print('register notification token', userId, token)
        self.token_map[userId] = token

    def get_token(self, userId):
        if userId in self.token_map:
            return self.token_map[userId]
        return DEFAULT_TOKEN

    def send_notification(self, userId, message="Hello World!"):

        token_hex = self.get_token(userId)
        payload = Payload(alert=message, sound="default", badge=1)
        print(payload.__dict__)
        topic = 'com.epage.QuietMind'

        self.client = APNsClient(DEV_CERT_FILE, use_sandbox=True, use_alternative_port=False)
        self.client.send_notification(token_hex, payload, topic)

        # Send an iOS 10 compatible notification
        # payload = Payload(alert=message, sound="default", badge=1)
        # token_hex = self.get_token(userId)
        # self.client.send(token_hex, message)
        # self.apns.gateway_server.send_notification(token_hex, payload)

        # print('send notification payload', payload, 'token', token_hex)
        # self.client.send_notification(token_hex, payload, self.topic)
