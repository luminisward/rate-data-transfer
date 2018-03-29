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

    def getOptionsWhereTidIs(self, oid):
        with self.__connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT polloptionid FROM cdb_forum_polloption WHERE tid = %s ORDER BY displayorder"
            cursor.execute(sql,(oid,))
            result = cursor.fetchall()
            options = map(lambda x: x['polloptionid'], result)
            return list(options)

    def getTidWhereOptionidIs(self, tid):
        with self.__connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT tid FROM cdb_forum_polloption WHERE polloptionid = %s"
            cursor.execute(sql,(tid,))
            result = cursor.fetchone()
            return result['tid']

    def getVotersWhereTidIs(self, tid):
        with self.__connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT * FROM cdb_forum_pollvoter WHERE tid = %s"
            cursor.execute(sql,(tid,))
            result = cursor.fetchall()
            return result

    def optionid2score(self, optionid):
        tid = self.getTidWhereOptionidIs(optionid)
        options = self.getOptionsWhereTidIs(tid)
        score = 2 - options.index(int(optionid))
        return score

    def tid2title(self, tid):
        with self.__connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT `subject` FROM cdb_forum_thread WHERE tid = %s"
            cursor.execute(sql,(tid,))
            result = cursor.fetchone()
            return result['subject']