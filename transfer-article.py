import discuz
import mediawiki
import re
from html.parser import HTMLParser

def parseTitle(row):
    title = row['subject']
    print(title)
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

def addCategory(row):
    if 'category1' in row:
        row['message'] += '\n\n[[Category:' + row['category1'] + ']]'
    if 'category2' in row:
        row['message'] += '[[Category:' + row['category2'] + ']]'
    return row

def removeImgTag(row):
    row['message'] = row['message'].replace('[img]', '\n')
    row['message'] = row['message'].replace('[/img]', '\n')
    return row

def removeUrlTag(row):
    row['message'] = row['message'].replace('[/url]', '\n')
    row['message'] = re.sub(r'\[url.*?\]', '', row['message'])
    return row

def newline(row):
    row['message'] = row['message'].replace('\n', '\n\n')
    return row

def removeEdited(row):
    row['message'] = re.sub(r'\[i\].+编辑 \[\/i\]', '', row['message'])
    return row

def retry(mw, title, wikitext):
    if mw.edit(title, wikitext):
        return True
    else:
        mw.login('S1@123456','gugcr2e2apc3tvmpohjrrfd1rifjla94')
        retry(mw, title, wikitext)

dz = discuz.DiscuzDB('172.16.233.100','root','root','stage1stdz')
tids = dz.getTidWhereFidIs('83')
data = dz.getPostWhereTidIn(tids)

data = map(newline, data)
data = map(parseTitle, data)
data = filter(lambda x: x, data)
data = map(addCategory, data)
data = map(removeImgTag, data)
data = map(removeUrlTag, data)

mw = mediawiki.MediawikiAPI('http://172.17.0.1/api.php')
mw.login('S1@123456','gugcr2e2apc3tvmpohjrrfd1rifjla94')

for article in data:
    if 'title' in article:
        title, wikitext = article['title'], article['message']
        title = HTMLParser().unescape(title)
        retry(mw, title, wikitext)