import requests

http_session = requests.Session()
api_path = "/api"

class MealieClient(object):
    def __init__(self, api_key, mealie_base_url):
        self.api_key = api_key
        self.mealie_base_url = mealie_base_url
        
    def get_todays_mealplan(self):
        request_url = self.mealie_base_url + api_path + "/groups/mealplans/today"
        headers = {
            "Authorization": f"Bearer ${self.api_key}"
        }
        
        try:
            response = http_session.get(request_url, headers=headers)
        except requests.exceptions.ConnectionError:
            raise ConnectionFailedException()
        
        return self.__handle_response(response)
    
    def get_self(self):
        request_url = self.mealie_base_url + api_path + "/users/self"
        headers = {
            "Authorization": f"Bearer ${self.api_key}"
        }
        
        try:
            response = http_session.get(request_url, headers=headers)
        except requests.exceptions.ConnectionError:
            raise ConnectionFailedException()
        
        return self.__handle_response(response)
            
    def __handle_response(self, response):
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            raise UnauthorizedException()
        else:
            response.raise_for_status()
        
        
class UnauthorizedException(Exception):
    """ Server returned HTTP 401 """
    
class ConnectionFailedException(Exception):
    """ Connection to the Mealie API failed """