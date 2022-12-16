from website import create_app
import json

import pytest

colby_ids = ["testCoach", "testAthlete", "testPEAK", "testAdmin"]

def test_create_app():
    app = create_app()

    assert app != None

def test_failed_login_no_user(client):

    response = client.get('/login')
    print("\n\n ******* \n", response.data)
    print("\n\n ..... \n", response.status_code)
    assert response.status_code == 200
    assert b'colby_id' in response.data
    assert b'password' in response.data

    with client:
        response = client.post("/create-user", 
                    data={"colby_id": "testAth2",
                          "firstname": "Ath2",
                          "lastname": "Test",
                          "athlete_data": "3",
                          "team_data": "3",
                          "notes": "3",
                          "create_account": "3",
                          "permission_change": "3",
                          "role": "3",
                          "password1": "12345678",
                          "password2": "12345678"})

        response = client.post("/login", 
                                data={"colby_id": "testAth2",
                                      "password": "123456789"})

        print("\n\n", response.data)
        assert response.status_code == 200
        assert b'Incorrect password, try again.' in response.data

def test_wrong_password(client):
    response = client.get('/login')
    assert response.status_code == 200
    assert b'colby_id' in response.data
    assert b'password' in response.data


    with client:
        response = client.post("/login", 
                    data={"colby_id": "testCoach",
                            "password": "12345678"})

        print("\n\n", response.data)
        assert response.status_code == 200
        assert b'User does not exist.' in response.data

def test_create_admin(client):

    response = client.get('/create-user')
    assert response.status_code == 200
    assert b'colby_id' in response.data
    assert b'password1' in response.data

    with client:
        response = client.post("/create-user", 
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

        # print("\n\n", response.data)
        assert response.status_code == 302 # redirect to home page
        assert b'Redirecting' in response.data

def test_create_peak(client):

    response = client.get('/create-user')
    assert response.status_code == 200
    assert b'colby_id' in response.data
    assert b'password1' in response.data

    with client:
        response = client.post("/create-user", 
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

        # print("\n\n", response.data)
        assert response.status_code == 302 # redirect to home page
        assert b'Redirecting' in response.data

def test_create_coach(client):

    response = client.get('/create-user')
    assert response.status_code == 200
    assert b'colby_id' in response.data
    assert b'password1' in response.data

    with client:
        response = client.post("/create-user", 
                        data={"colby_id": "testCoach",
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

        # print("\n\n", response.data)
        assert response.status_code == 302 # redirect to home page
        assert b'Redirecting' in response.data

def test_create_athlete(client):

    response = client.get('/create-user')
    assert response.status_code == 200
    assert b'colby_id' in response.data
    assert b'password1' in response.data

    with client:
        response = client.post("/create-user", 
                    data={"colby_id": "testAthlete",
                          "firstname": "Athlete",
                          "lastname": "Test",
                          "athlete_data": "3",
                          "team_data": "3",
                          "notes": "3",
                          "create_account": "3",
                          "permission_change": "3",
                          "role": "3",
                          "password1": "12345678",
                          "password2": "12345678"})

        print("\n\n", response.data)
        assert response.status_code == 302 # redirect to home page
        assert b'Redirecting' in response.data 

def test_success_ath_login(client):

    response = client.get('/login')
    assert response.status_code == 200
    assert b'colby_id' in response.data
    assert b'password' in response.data

    with client:
        response = client.post("/create-user", 
                    data={"colby_id": "testAth2",
                          "firstname": "Ath2",
                          "lastname": "Test",
                          "athlete_data": "3",
                          "team_data": "3",
                          "notes": "3",
                          "create_account": "3",
                          "permission_change": "3",
                          "role": "3",
                          "password1": "12345678",
                          "password2": "12345678"})

        response = client.post("/login", 
                                data={"colby_id": "testAth2",
                                      "password": "12345678"})

        print("\n\n", response.data)
        assert response.status_code == 302 # redirect to home page
        assert b'Redirecting' in response.data 

def test_success_coach_login(client):

    response = client.get('/login')
    assert response.status_code == 200
    assert b'colby_id' in response.data
    assert b'password' in response.data

    with client:
        response = client.post("/create-user", 
                    data={"colby_id": "testCoach2",
                              "firstname": "Coach2",
                              "lastname": "Test",
                              "athlete_data": "2",
                              "team_data": "2",
                              "notes": "2",
                              "create_account": "2",
                              "permission_change": "2",
                              "role": "2",
                              "password1": "12345678",
                              "password2": "12345678"})

        response = client.post("/login", 
                                data={"colby_id": "testCoach2",
                                      "password": "12345678"})

        assert response.status_code == 302 # redirect to home page
        assert b'Redirecting' in response.data 


def test_logout(client):

    with client:
        response = client.post("/create-user", 
                    data={"colby_id": "testAth3",
                          "firstname": "Ath3",
                          "lastname": "Test",
                          "athlete_data": "3",
                          "team_data": "3",
                          "notes": "3",
                          "create_account": "3",
                          "permission_change": "3",
                          "role": "3",
                          "password1": "12345678",
                          "password2": "12345678"})

        response = client.post("/login", 
                                data={"colby_id": "testAth3",
                                      "password": "12345678"})

        response = client.get('/logout', follow_redirects=True)
        print("\n\n", response.data)

        assert response.status_code == 200 # redirect to login page
        assert b'login' in response.data

def test_ask_auth(client):
    client.post("/create-user", 
                    data={"colby_id": "testAthlete",
                          "firstname": "Ath",
                          "lastname": "ath",
                          "athlete_data": "1",
                          "team_data": "1",
                          "notes": "1",
                          "create_account": "1",
                          "permission_change": "1",
                          "role": "3",
                          "password1": "12345678",
                          "password2": "12345678"})
    client.post("/login", 
            data={"colby_id": "testAthlete",
                  "password": "12345678"})

    response = client.get('/auth/oura')
    response1 = client.get('/authorize/oura')

    assert response.status_code == 302
    assert response1.status_code == 400





