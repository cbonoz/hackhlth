import os
import requests

# https://curl.trillworks.com/
class Softheon:

    def __init__(self, client_id, client_secret, scopes=""):
        self.client_id = client_id
        self.client_secret = client_secret
        self.scopes = scopes
        return

    def send_stim_event(self, data, access_token):
        """
        Send autistic stimming event to the softheon server for secure storage and recording.
        :param data: array of data
        :param type: oneof "accel" or "gyro"
        :return: Softheon API response
        """

        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer %s' % access_token,
        }

        response = requests.post('https://hack.softheon.io/api/enterprise/v1/content/entities/2', headers=headers, data=data)
        return response

    def get_auth_token(self):
        """
        Get identity token for softheon api.
        :return:
        """
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        data = [
            ('client_id', self.client_id),
            ('client_secret', self.client_secret),
            ('grant_type', 'client_credentials'),
            ('scope', self.scopes),
        ]

        response = requests.post('https://hack.softheon.io/oauth2/connect/token', headers=headers, data=data)
        return response


