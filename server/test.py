# from apns2.client import APNsClient
from apns2.payload import Payload
from apns import APNs# , Frame, Payload

CERT_FILE = "./apns-dev.pem"
KEY_FILE = "./apns-dev-key-noenc.pem"


# token_hex = 'f7ca3b57016e6882fe11b7253e16b2068bdee0f119800b4271456bb04e896149'
# payload = Payload(alert="Hello World!")
# topic = 'com.epage.QuietMind'

token_hex = 'b5bb9d8014a0f9b1d61e21e796d78dccdf1352f23cd32812f4850b87'
payload = Payload(alert="Hello World!", sound="default", badge=1)
apns_enhanced = APNs(use_sandbox=True, cert_file=CERT_FILE, enhanced=True)
identifier = random.getrandbits(32)
apns_enhanced.gateway_server.send_notification(token_hex, payload, identifier=identifier)
# client = APNsClient(CERT_FILE, use_sandbox=True, use_alternative_port=False)
# client.send_notification(token_hex, payload, topic)
