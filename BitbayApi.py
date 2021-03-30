import requests
import json

class Bitbay_Api:
    """
    Class used to communicate with BitBay via API.
    It provides basic functionalities such as GET request (for now).
    """

    def __init__(self, base_url='https://api.bitbay.net/rest/', credentials=None):
        """
        Initialaze Bitbay_Api class.
        :param base_url: Base BitBay rest API's url
        :param credentials: User's login & password
        """
        self.base_url = base_url

    def get(self, item):
        """
        Performs GET request to the BitBay API
        :param item: Item, that we want to get
        """
        headers = {'content-type': 'application/json'}
        response = requests.get(self.base_url + item, headers=headers)
        return json.loads(response.content)

