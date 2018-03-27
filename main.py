import discuz
import mediawiki
import re

def parseTitle(row):
    title = row['subject']
    m = re.match(r'\[(.+)\]\[(.+)\](.+?)\/(.+)', title)
    if m:
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

dz = discuz.DiscuzDB('172.16.233.100','root','root','stage1stdz')
tids = dz.getTidWhereFidIs('83')
data = dz.getPostWhereTidIn(tids)

data = map(parseTitle, data)
data = map(addCategory, data)

mw = mediawiki.Mediawiki('http://172.16.233.151/api.php')
mw.login('S1@123456','gugcr2e2apc3tvmpohjrrfd1rifjla94')

for article in data:
    if 'title' in article:
        title, wikitext = article['title'], article['message']
        mw.edit(title, wikitext)
        print(title)