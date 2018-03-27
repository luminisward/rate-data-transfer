import requests

class Mediawiki(object):
    def __init__(self, apiUrl):
        self.__url = apiUrl
        self.__session = requests.Session()
        

    def clientLogin(self, username, password):
        loginToken = self.__getLoginToken()
        payload = {
            'action': 'clientlogin',
            'username': username,
            'password': password,
            'loginreturnurl': 'http://localhost/',
            'logintoken': loginToken,
            'format': 'json'
        }
        self.__session.post(self.__url, data=payload)

    def login(self, username, password):
        loginToken = self.__getLoginToken()
        payload = {
            'action': 'login',
            'lgname': username,
            'lgpassword': password,
            'lgtoken': loginToken,
            'format': 'json'
        }
        self.__session.post(self.__url, data=payload)
        self.__csrfToken = self.getCsrfToken()
        return True

    def edit(self, title, text):
        payload = {
            'action': 'edit',
            'title': title,
            'text': text,
            'token': self.__csrfToken,
            'bot': True,
            'format': 'json'
        }
        self.__session.post(self.__url, data=payload)
        return True

    def __getLoginToken(self):
        querystring = {"action":"query","meta":"tokens","format":"json","type":"login"}
        response = self.__session.get(self.__url, params=querystring)
        data = response.json()
        return data['query']['tokens']['logintoken']
    
    def getCsrfToken(self):
        querystring = {"action":"query","meta":"tokens","format":"json","type":"csrf"}
        response = self.__session.get(self.__url, params=querystring)
        data = response.json()
        return data['query']['tokens']['csrftoken']

    def ratePage(self, pageId, score):
        payload = {
            'action': 'RatePage',
            'pageid': pageId,
            'score': score,
            'format': 'json',
            'token': self.__csrfToken
        }
        self.__session.post(self.__url, data=payload)
        return True
