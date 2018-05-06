from apns2.client import APNsClient
from apns2.payload import Payload

CERT_FILE = "./apns-dev.pem"
KEY_FILE = "./apns-dev-key-noenc.pem"


token_hex = 'f7ca3b57016e6882fe11b7253e16b2068bdee0f119800b4271456bb04e896149'
payload = Payload(alert="Hello World!", sound="default", badge=1)
print(payload.__dict__)
topic = 'com.epage.QuietMind'

client = APNsClient(CERT_FILE, use_sandbox=True, use_alternative_port=False)
client.send_notification(token_hex, payload, topic)
