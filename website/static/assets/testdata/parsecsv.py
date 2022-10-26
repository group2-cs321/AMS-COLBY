
import json

from csv import DictReader


def getHawkinData(id):
    with open("hawkins.csv", 'r') as f:
         
        dict_reader = DictReader(f)
         
        list_of_dict = list(dict_reader)

        for line in list_of_dict:
            if line["ID"]==id:
                return json.dumps(line, indent = 4)

def getWatchData():
    # from this we want:
        #Date
        #Restfulness Score
        #Total Sleep Duration
        #REM Sleep Duration
        #Light Sleep Duration
        #Average Resting HR
    with open("watchData.csv", 'r') as f:
         
        dict_reader = DictReader(f)
         
        list_of_dict = list(dict_reader)
        output=[[],[],[],[],[],[]]
        for i in range(5):
            output[0].append(list_of_dict[i]["date"])
            output[1].append(list_of_dict[i]["Restfulness Score"])
            output[2].append(list_of_dict[i]["Total Sleep Duration"])
            output[3].append(list_of_dict[i]["REM Sleep Duration"])
            output[4].append(list_of_dict[i]["Light Sleep Duration"])
            output[5].append(list_of_dict[i]["Average Resting Heart Rate"])
        return json.dumps(output, indent = 4)



getHawkinData("Dylan")
getWatchData()