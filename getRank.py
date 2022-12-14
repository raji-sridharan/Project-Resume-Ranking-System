import os
import getScore
from operator import itemgetter
import json
def rank():
    file_object = open('result.json', 'a')
    file_object.write("[\n")
    rankList=[]
    path="files"
    files=os.listdir(path)

    i=0
    for file in files:
        print("\nGetting score of Resume - ",i+1,"\n")
        info = getScore.score("files/"+file)
        rank = {
                "name":info[0],
                "email":info[1],
                "number":info[2],
                "file":file,
                "score":info[3]
                }
        print("\n",rank,"\n")
        rankList.append(rank)
        json_object = json.dumps(rank, indent = 4) 
        file_object.write(json_object)
        if i!=len(files)-1:
            file_object.write(",\n")
        i += 1
        print('-'*175)

    file_object.write("]")
    file_object.close()
    rankList = sorted(rankList, key=itemgetter('score'), reverse=True)
    return rankList


