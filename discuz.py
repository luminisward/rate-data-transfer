import pymysql.cursors

class DiscuzDB(object):

    def __init__(self, host, user, password, db):
        self.__connection = pymysql.connect(host=host,
                             user=user,
                             password=password,
                             db=db,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

    def __del__(self):
        self.__connection.close()

        
    def getPostWhereTidIn(self, tids):
        with self.__connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT `subject`,`message` FROM cdb_forum_post WHERE tid in %s AND `first`=1"
            cursor.execute(sql,(tids,))
            result = cursor.fetchall()
            return result

    def getTidWhereFidIs(self, fid):
        with self.__connection.cursor() as cursor:
            sql = "SELECT `tid` FROM cdb_forum_thread WHERE fid=%s AND displayorder=0"
            cursor.execute(sql, (fid,))
            result = cursor.fetchall()
            result = map(lambda x:x['tid'], result)
            return tuple(result)



