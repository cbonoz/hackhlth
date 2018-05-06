import os
import json
import requests

# Code assumes the entities have already been created in Softheon.
STIM_ENTITY_TYPE = 161

# https://curl.trillworks.com/
class Softheon:
    def __init__(self, client_id, client_secret, scopes="enterpriseapi openid"):
        self.client_id = client_id
        self.client_secret = client_secret
        self.scopes = scopes
        self.access_token = None
        return

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
            ('grant_type', 'password'),
            ('scope', self.scopes),
            ('username', 'hack100'),
            ('password', 'CyN6Csh2'),
        ]

        print(headers)

        try:
            response = requests.post('https://hack.softheon.io/oauth2/connect/token', headers=headers, data=data)
            res = response.json()
            if 'access_token' not in res:
                return res
            token = res['access_token']
            self.access_token = token
            return token
        except Exception as e:
            print('error', e)
            return {'error': e}

    def create_stim_entity(self, type=160):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer %s' % self.access_token
        }

        data = '{"Category":"Common","Name":"Stim Template","Type":"%s","Profiles":[{"Type":1,"Name":"Stim","Fields":[{"Name":"User Id","Type":"String","Index":0,"Position":0,"Default":"1","Length":25},{"Name":"Timestamp","Type":"Integer","Index":0,"Position":0}]}],"Drawers":[100]}' % type


        response = requests.post('https://hack.softheon.io/api/enterprise/v1/template/ftl/', headers=headers, data=data)
        response.json()
        return response

    # 6313883095

    def get_stim_events(self, drawer=100):
        """
        Get stim events for a provided user id.
        :param data: {userId: ...}
        :return: api response containing list of stimming events associated with the given user id {userId: ..., data: [...]}
        """

        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer %s' % self.access_token
        }


        url = "https://hack.softheon.io/api/enterprise/v1/content/entities?drawerID=%s" % drawer
        response = requests.get(url, headers=headers)
        response.json()
        return response

    def send_stim_event(self, userId, timestamp, type=STIM_ENTITY_TYPE, drawer=100):
        """
        Send autistic stimming event to the softheon server for secure storage and recording.
        :param userId: userId of the user to record
        :param timestamp: timestamp of the stim event occurence.
        :return: Softheon API response
        """

        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer %s' % self.access_token,
        }

        data = {
            "Profiles": [
                {
                    "Acl": -1,
                    "Type": 1,
                    "Strings": [
                        userId
                    ],
                    "Integers": [
                        timestamp
                    ]
                }
            ],
            "Acl": -1,
            "Type": type,
            "Subtype": 0,
            "State": "Available",
            "Name": "Stim Entity"
        }

        print(data)

        response = requests.post('https://hack.softheon.io/api/enterprise/v1/content/entities/%d' % drawer, headers=headers,
                                 data=json.dumps(data))
        return response
