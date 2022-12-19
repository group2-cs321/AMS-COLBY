'''
File with functions used in the backend
'''
from csv import DictReader
import pandas as pd
from website.models import User, Athlete, Coach, Team, Note
from werkzeug.security import generate_password_hash



def parse_CSV():

    """parse CSV file
    
    Reads an athelete data csv file
 
    Returns
    -------
    watchData: nested list of strings and floats
    """
    watchData=[[],[],[],[],[],[],[],[],[],[]]

    with open("website/static/assets/testdata/watchData.csv", 'r') as f:
         
        dict_reader = DictReader(f)
         
        list_of_dict = list(dict_reader)
        for i in range(5):
            watchData[0].append(list_of_dict[i]["date"])
            watchData[1].append(float(list_of_dict[i]["Restfulness Score"]))
            watchData[2].append(float(list_of_dict[i]["Total Sleep Duration"])/60**2)
            watchData[3].append(float(list_of_dict[i]["REM Sleep Duration"])/60**2)
            watchData[4].append(float(list_of_dict[i]["Light Sleep Duration"])/60**2)
            watchData[5].append(float(list_of_dict[i]["Deep Sleep Duration"])/60**2)
            watchData[6].append(float(list_of_dict[i]["Average Resting Heart Rate"]))
            watchData[7].append(float(list_of_dict[i]["Lowest Resting Heart Rate"]))
            watchData[8].append(float(list_of_dict[i]["Steps"]))
            watchData[9].append(float(list_of_dict[i]["Sleep Score"]))
    return watchData

def importCSV (fileAdress):
     '''ImportCSV will read a csv file and create the set of users, CSV should follow the next format: [Colby ID, Name, Last Name]

     Parameters:
     -----------
     filepath: string. location of the data 

     Output:
     ------------
     ''' 
     #reads the data and converts it to numpy
     data = pd.read_csv(fileAdress)
     data = data.to_numpy()


     #goes though the data an obtains the information from teh CSV
     for athlete in data:
            colby_id = data[0]
            first_name = data[1]
            last_name = data[2]
            password1 = "12345678"
            athlete_data = 3
            team_data = 3
            notes = 3
            create_account = 3
            permission_change = 3
            role = 3
        
        #add user to database
            new_user = User(colby_id=colby_id, first_name=first_name, last_name = last_name,
                password=generate_password_hash(password1, method='sha256'),
                role = role, athlete_data = athlete_data, team_data = team_data, notes = notes,
                account_create = create_account, permission_change = permission_change)
            db.session.add(new_user)

            athlete = Athlete(colby_id=colby_id, first_name=first_name, last_name = last_name)
            db.session.add(athlete)

            db.session.commit()
            
     flash("All users have been succesfully created", category='success')
     return 
