import discuz
import mediawiki
import re
from html.parser import HTMLParser

def parseTitle(row):
    title = row['subject']
    m1 = re.match(r'\[(.+)\]\[(.+)\](.+?)\/(.*)', title)
    m2 = re.match(r'\[(.+)\]\[(.+)\](.+)', title)
    if m1:
        m = m1
    elif m2:
        m = m2
    else:
        return False

    row['category1'] = m.group(1)
    row['category2'] = m.group(2)
    row['title'] = m.group(3)
    return row


mw = mediawiki.MediawikiAPI('http://172.17.0.1/api.php')
mwdb = mediawiki.MediawikiDatabase('172.17.0.1','root','MjqVXTUhDgp4xsakiwT5','my_wiki')
dz = discuz.DiscuzDB('172.16.233.100','root','root','stage1stdz')
tids = dz.getTidWhereFidIs('83')
tids = filter(lambda x: len(dz.getOptionsWhereTidIs(x)) == 5, tids)
data = map(dz.getVotersWhereTidIs, tids)
data = filter(lambda x: x, data)
for page in data:
    for row in page:
        print(row)
        score = dz.optionid2score(row['options'])
        print(score)

        row['subject'] = dz.tid2title(row['tid'])
        row = parseTitle(row)
        row['title'] = row['title'].strip()
        row['title'] = HTMLParser().unescape(row['title'])
        print(row['title'])
        pageid = mwdb.getPageidWhereTitleIs(row['title'])

        mwdb.insertRateRecord(pageid ,0 ,row['username'] ,score ,row['dateline'])
