import os
import requests

# https://curl.trillworks.com/
class Softheon:

    def __init__(self, client_id, client_secret, scopes=""):
        self.client_id = client_id
        self.client_secret = client_secret
        self.scopes = scopes
        self.access_token = None
        return

    def get_stim_events(self, data):
        """
        Get stim events for a provided user id.
        :param data: {userId: ...}
        :return: api response containing list of stimming events associated with the given user id {userId: ..., data: [...]}
        """
        # TODO: implement

        response = []
        return response

    def send_stim_event(self, data):
        """
        Send autistic stimming event to the softheon server for secure storage and recording.
        :param data: {userId: ..., data: [...]}
        :return: Softheon API response
        """

        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer %s' % self.access_token,
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

        try:
            response = requests.post('https://hack.softheon.io/oauth2/connect/token', headers=headers, data=data)
            res = response.json()
            return res['access_token']
        except Exception as e:



