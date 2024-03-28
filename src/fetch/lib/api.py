import requests

class API:
    def __init__(self, url, logger):
        self.api = url
        self.logger = logger
    
    def getResponse(self, params, retry=5):
        response = None
        while response is None and retry > 0:
            try:
                response = requests.get(self.api, params=params)
                if response is None:
                    self.logger.warning('response is None')
                    response = None
                else:
                    response = response.json()
                    if response['status'] != 'OK':
                        self.logger.warning('status: %s', response['status'])
                        response = None
            except requests.exceptions.ConnectionError:
                self.logger.warning('ConnectionError,' 'retry after 5 seconds, %d times left', retry)
                retry -= 1
        if response is None:
            self.logger.error('Failed to get response {url} with params {params}'.format(url=self.api, params=params))
            return None
        return response["result"]