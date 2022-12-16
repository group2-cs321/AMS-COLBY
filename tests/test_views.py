
from website import create_app
import json
import pytest
from website import views


def create_admin(client):

    client.post("/create-user", 
                    data={"colby_id": "testAdmin",
                          "firstname": "Admin",
                          "lastname": "Test",
                          "athlete_data": "0",
                          "team_data": "0",
                          "notes": "0",
                          "create_account": "0",
                          "permission_change": "0",
                          "role": "0",
                          "password1": "12345678",
                          "password2": "12345678"})
    client.post("/login", 
            data={"colby_id": "testAdmin",
                  "password": "12345678"})

def test_admin_home(client):

    response = client.get('/')
    print(response.data)
    assert response.status_code == 302 # redirect to login page
    assert b'Redirecting' in response.data
    assert b'login' in response.data


    create_admin(client)

    response = client.get('/', follow_redirects=True)
    print(response.data)
    assert response.status_code == 200 # redirect to home page
    assert b'<a class="btn btn-primary btn-block" href="/admin/permissions">Edit Permissions</a>' in response.data

def create_peak(client):

    client.post("/create-user", 
                        data={"colby_id": "testPEAK",
                              "firstname": "PEAK",
                              "lastname": "Test",
                              "athlete_data": "1",
                              "team_data": "1",
                              "notes": "1",
                              "create_account": "1",
                              "permission_change": "1",
                              "role": "1",
                              "password1": "12345678",
                              "password2": "12345678"})
    client.post("/login", 
            data={"colby_id": "testPEAK",
                  "password": "12345678"})

def test_peak_home(client):

    response = client.get('/')
    print(response.data)
    assert response.status_code == 302 # redirect to login page
    assert b'Redirecting' in response.data
    assert b'login' in response.data


    create_peak(client)

    response = client.get('/', follow_redirects=True)
    print(response.data)
    assert response.status_code == 200 # redirect to home page
    assert b'<a class="btn btn-primary btn-block" href="/new-note">Send notes</a>' in response.data


def create_coach_athlete_and_team(client):

    client.post("/create-user", 
                        data={"colby_id": "testCoach3",
                              "firstname": "Coach",
                              "lastname": "Test",
                              "athlete_data": "2",
                              "team_data": "2",
                              "notes": "2",
                              "create_account": "2",
                              "permission_change": "2",
                              "role": "2",
                              "password1": "12345678",
                              "password2": "12345678"})

    client.post("/create-user", 
                        data={"colby_id": "testAthlete3",
                          "firstname": "Athlete3",
                          "lastname": "Test",
                          "athlete_data": "3",
                          "team_data": "3",
                          "notes": "3",
                          "create_account": "3",
                          "permission_change": "3",
                          "role": "3",
                          "password1": "12345678",
                          "password2": "12345678"})

    create_admin(client)
    
    client.post("/create-team", 
            data={"team_name": "testTeam",
                  "athletes": ["testAthlete3"],
                  "coaches": "testCoach3"})


def test_coach_home(client):

    response = client.get('/')
    print(response.data)
    assert response.status_code == 302 # redirect to home page
    assert b'Redirecting' in response.data
    assert b'login' in response.data


    create_coach_athlete_and_team(client)

    client.post("/login", 
        data={"colby_id": "testCoach3",
              "password": "12345678"})

    response = client.get('/team/1', follow_redirects=True)
    print(response.data)
    assert response.status_code == 200 # redirect to home page
    assert b'<h6 class="mb-1">Notes</h6>' in response.data 


def test_athlete_home(client):

    response = client.get('/')
    print(response.data)
    assert response.status_code == 302 # redirect to home page
    assert b'Redirecting' in response.data
    assert b'login' in response.data


    create_coach_athlete_and_team(client)

    response = client.post("/login", 
        data={"colby_id": "testAthlete3",
              "password": "12345678"})

    print(response.data)
    assert response.status_code == 302 # redirect to home page
    assert b'Redirecting' in response.data 


def test_athlete_coach_dashboard(client):

    create_coach_athlete_and_team(client)

    client.post("/login", 
        data={"colby_id": "testCoach3", 
              "password": "12345678"})

    response = client.get('team/coach/athlete/1', follow_redirects=True)

    print(response.data)
    assert response.status_code == 200 # redirect to home page
    assert b'<h5><a>Readiness</a></h5>' in response.data 

def test_permission_page(client):

    #1. create admin and login as admin
    create_admin(client)

    #2. create the coach and team, to be changed to an athlete
    create_coach_athlete_and_team(client)

    #3. login as the coach
    client.post("/login", 
        data={"colby_id": "testCoach3",
              "password": "12345678"})

    #4. check if they could login in as the coach
    response = client.get('/team/1', follow_redirects=True)
    print(response.data)
    assert response.status_code == 200 # redirect to home page
    assert b'<h6 class="mb-1">Notes</h6>' in response.data 

    #5. login in as the admin
    client.post("/login", 
            data={"colby_id": "testAdmin",
                  "password": "12345678"})

    #6. change the coach's permission to an athlete
    client.post("/admin/permissions", 
        data={"user_to_change": "testCoach3", 
              "athlete_data": "3",
              "team_data": "3",
              "notes": "3",
              "create_account": "3",
              "permission_change": "3",
              "role": "3"})

    #7. login as the coach (already changed to an athlete)
    client.post("/login", 
        data={"colby_id": "testCoach3",
              "password": "12345678"})

    #8. check if they don't have access to coach page anymore
    response = client.get('/team/1', follow_redirects=True)
    print(response.data)
    assert response.status_code == 200 # redirect to home page
    assert b'<h1>No Access</h1>' in response.data 

def test_permission_page_peak(client):

    #1. create admin and login as admin
    create_admin(client)

    #2. create the coach and team, to be changed to an athlete
    create_coach_athlete_and_team(client)

    #3. login as the coach
    client.post("/login", 
        data={"colby_id": "testCoach3",
              "password": "12345678"})

    #4. check if they could login in as the coach
    response = client.get('/team/1', follow_redirects=True)
    print(response.data)
    assert response.status_code == 200 # redirect to home page
    assert b'<h6 class="mb-1">Notes</h6>' in response.data 

    response = client.get('/admin/permissions')

    assert response.status_code == 200
    assert b'<h1>No Access</h1>' in response.data

    #5. login in as the admin
    client.post("/login", 
            data={"colby_id": "testAdmin",
                  "password": "12345678"})

    #6. change the coach's permission to an athlete
    client.post("/admin/permissions", 
        data={"user_to_change": "testAthlete3", 
              "athlete_data": "1",
              "team_data": "1",
              "notes": "1",
              "create_account": "1",
              "permission_change": "1",
              "role": "1"})

    #7. login as the coach (already changed to an athlete)
    client.post("/login", 
        data={"colby_id": "testAthlete3",
              "password": "12345678"})

    #8. check if they don't have access to coach page anymore
    response = client.get('/team/1', follow_redirects=True)
    print(response.data)
    assert response.status_code == 200 # redirect to home page
    #assert b'<h1>No Access</h1>' in response.data 

def test_create_note(client):
    create_coach_athlete_and_team(client)
    create_peak(client)

    client.post("/new-note", 
        data={"athletes": "testAthlete3", 
              "content": "Testing Note",
              "clearance": "Cleared"})

    client.post("/login", 
        data={"colby_id": "testCoach3",
              "password": "12345678"})

    response = client.get('team/coach/athlete/1', follow_redirects=True)

    print(response.data)
    assert response.status_code == 200 # redirect to home page
    assert b'<p class="text-muted mb-0"> Testing Note</p>' in response.data 

def test_edit_team(client):
    create_coach_athlete_and_team(client)
    create_admin(client)

    #create testAthlete4 to be added to testTeam - begin
    client.post("/create-user", 
                        data={"colby_id": "testAthlete4",
                          "firstname": "Athlete4",
                          "lastname": "Test",
                          "athlete_data": "3",
                          "team_data": "3",
                          "notes": "3",
                          "create_account": "3",
                          "permission_change": "3",
                          "role": "3",
                          "password1": "12345678",
                          "password2": "12345678"})
    #create testAthlete4 to be added to testTeam - end

    #to make sure now testAthlete4 is not in testTeam - begin
    client.post("/login", 
        data={"colby_id": "testCoach3",
              "password": "12345678"})

    response = client.get('/team/1', follow_redirects=True)

    #print(response.data)
    assert response.status_code == 200 # redirect to home page
    assert b'<span class="pl-2">Athlete4 Test</span>' not in response.data
    #to make sure now testAthlete4 is not in testTeam - end

    #Add testAthlete4 to testTeam - begin
    client.post("/login", 
            data={"colby_id": "testAdmin",
                  "password": "12345678"})

    client.get("/team-select")

    team_id = "1"

    client.post("/edit-team/1", 
        data={ "athletes_add": ["testAthlete4"],
              "athletes_del": [],
              "coaches": "testCoach3"})
    #Add testAthlete4 to testTeam - end

    #to make sure now testAthlete4 is in testTeam now - begin
    client.post("/login", 
        data={"colby_id": "testCoach3",
              "password": "12345678"})

    response = client.get('/team/1', follow_redirects=True)

    #print(response.data)
    assert response.status_code == 200 # redirect to home page
    assert b'<span class="pl-2">Athlete4 Test</span>' in response.data
    #to make sure now testAthlete4 is in testTeam now - end

def test_create_team(client):
    create_admin(client)

    client.post('/login', data = {"colby_id": "testAdmin",
                  "password": "12345678"})

    response = client.get('/create-team')

    create_coach_athlete_and_team(client)

    assert response.status_code == 200

    client.post('/create-team', data={"team_name": "testTeam",
                  "athletes": ["testAthlete3"],
                  "coaches": "testCoach3"})

    response = client.get('/create-team')

    assert response.status_code == 200


def test_parse_CSV():
    views.parse_CSV()
    assert len(views.parse_CSV()) == 10
    assert len(views.parse_CSV()[1]) != 0

def test_users_csv(client):
    create_peak(client)

    response = client.post("/users-CSV")

    print(response.data)
    assert b'<h1>No Access</h1>' in response.data 


    create_admin(client)

    response = client.post("/users-CSV", 
            data={"file": "/website/static/assets/testdata/user.csv"})

    print(response.data)
    assert b'<!doctype html>' in response.data 


def test_livesearch(client):
    create_coach_athlete_and_team(client)

    client.post("/login", 
        data={"colby_id": "testCoach3",
              "password": "12345678"})

    response = client.post("livesearch", 
        data={"text": "testTeam"})
    print(response.data)
    assert b'testTeam' in response.data 

def test_livesearchathletes(client):
    create_coach_athlete_and_team(client)

    client.post("/login", 
        data={"colby_id": "testCoach3",
              "password": "12345678"})

    response = client.post("livesearchathletes/1", 
        data={"text": "Athlete3"})
    print(response.data)
    assert b'Athlete3' in response.data 

def test_team_select(client):
    create_coach_athlete_and_team(client)

    client.post("/login", 
        data={"colby_id": "testCoach3",
              "password": "12345678"})

    response = client.get("/team-select")
    print(response.data)
    assert b'testTeam' in response.data
