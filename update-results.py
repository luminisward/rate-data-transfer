import mediawiki

mwdb = mediawiki.MediawikiDatabase('172.17.0.1','root','MjqVXTUhDgp4xsakiwT5','my_wiki')

pids = mwdb.getAllPageId()

for pid in pids:
    finalScore = dict()
    result = {
        'item1': 0,
        'item2': 0,
        'item3': 0,
        'item4': 0,
        'item5': 0
    }
    records = mwdb.getRecordsByPageid(pid)

    # get final score
    for row in records:
        user = row['user_name'].decode()
        finalScore[user] = row['score']

    for user, score in finalScore.items():
        key = 'item' + str(3 - score)
        result[key] +=1

    print(result)

    mwdb.setRateResult(pid, result['item1'], result['item2'], result['item3'], result['item4'], result['item5'])
