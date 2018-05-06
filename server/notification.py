
from apns2.client import APNsClient
from apns2.payload import Payload

# https://github.com/Pr0Ger/PyAPNs2
class NotificationService:

    def __init__(self):
        self.topic = 'com.epage.QuietMind'
        self.token_map = {}
        self.client = APNsClient('key.pem', use_sandbox=False, use_alternative_port=False)

    def register_token(self, userId, token_file):
        self.token_map[userId] = token_file

    def get_token(self, userId):
        if userId in self.token_map:
            return self.token_map[userId]
        return ''

    def send_notification(self, userId, message="Hello World!"):
        payload = Payload(alert=message, sound="default", badge=1)
        token_hex = self.get_token(userId)
        self.client.send_notification(token_hex, payload, self.topic)
        print('send notification payload', payload)