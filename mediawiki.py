import requests
import pymysql

class MediawikiAPI(object):
    def __init__(self, apiUrl):
        self.__url = apiUrl
        self.__restful = 'http://172.17.0.1/api/v1'
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
        r = self.__session.post(self.__url, data=payload)
        data = r.json()
        print(data)
        if 'error' in data:
            return False
        elif 'edit' in data:
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

    def getPageidByTitle(self, title):
        url = self.__restful + '/page/title/' + title
        response = self.__session.get(url)
        data = response.json()
        return data['items'][0]['page_id']

class MediawikiDatabase(object):
    def __init__(self, host, user, password, db):
        self.__connection = pymysql.connect(host=host,
                             user=user,
                             password=password,
                             db=db,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

    def insertRateRecord(self, pageid, userid, username, score, date):
        data = (pageid, userid, username, score, date,)
        with self.__connection.cursor() as cursor:
            sql = "INSERT INTO `s1rate_records` (`page_id`, `user_id`, `user_name`, `score`, `date`) VALUES (%s, %s, %s, %s, FROM_UNIXTIME(%s))"
            cursor.execute(sql,(pageid, userid, username, score, date,))
            self.__connection.commit()

    def getPageidWhereTitleIs(self, title):
        title = title.replace(' ','_')
        with self.__connection.cursor() as cursor:
            sql = "SELECT page_id FROM page WHERE page_title = %s"
            cursor.execute(sql,(title,))
            result = cursor.fetchone()
            return result['page_id']

    def getTitleByPageid(self, pageid):
        with self.__connection.cursor() as cursor:
            sql = "SELECT page_title FROM page WHERE page_id = %s"
            cursor.execute(sql,(pageid,))
            result = cursor.fetchone()
            return result['page_title']

    def getAllPageId(self):
        with self.__connection.cursor() as cursor:
            sql = "SELECT page_id FROM page"
            cursor.execute(sql,)
            result = cursor.fetchall()
            result = map(lambda x:x['page_id'], result)
            return list(result)

    def getRecordsByPageid(self, pageid):
        with self.__connection.cursor() as cursor:
            sql = "SELECT `user_name`,`score` FROM s1rate_records where page_id = %s"
            cursor.execute(sql,(pageid,))
            result = cursor.fetchall()
            return result

    def setRateResult(self, page_id, item1, item2, item3, item4, item5):
        title = self.getTitleByPageid(page_id)
        with self.__connection.cursor() as cursor:
            sql = "REPLACE INTO `s1rate_results` VALUES (%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql,(page_id, title, item1, item2, item3, item4, item5,))
            self.__connection.commit()
