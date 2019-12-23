from flask import json, request

from . import app, call_client, create_token, client, reset_db

class TestUserCrud():

    reset_db()

    def test_user_signup(self, client):
        data = {
            'username':'fadhil',
            'password':'jojobamina'
        }

        req = call_client(request)
        res = req.post('/signup',
            query_string=data
        )

        res_json = json.loads(res.data)

        assert res.status_code == 200

    def test_login(self, client):
        data = {
            'username':'fadhil',
            'password':'jojobamina'
        }

        req = call_client(request)
        res = req.post('/login',
            query_string=data
        )

        assert res.status_code == 200

    def test_get_login(self, client):
        token = create_token()
        
        req = call_client(request)
        res = req.get('/login',
            headers={'Authorization':'Bearer ' + token}
        )

        assert res.status_code == 200

    def test_add_user(self, client):
        token = create_token()
        data = {
            'username':'fadhil2',
            'password':'minajuga'
        }

        req = call_client(request)
        res = req.post('/internal',
            query_string=data,
            headers={'Authorization': 'Bearer '+ token},
        )

        assert res.status_code == 200

    def test_edit_user(self, client):
        token = create_token()
        data = {
            'username':'fadhil2',
            'password':'masihmina'
        }

        req = call_client(request)
        res = req.put('/internal/2',
            json=data,
            headers={'Authorization':'Bearer {}'.format(token)},
        )

        assert res.status_code == 200

    def test_del_user(self, client):
        token = create_token()
        req = call_client(request)
        res = req.delete('/internal/2',
            headers={'Authorization':'Bearer ' + token}
        )

        assert res.status_code == 200

    def test_get_user(self, client):
        token = create_token()
        req = call_client(request)
        res = req.get('/internal',
            headers={'Authorization':'Bearer ' + token}
        )

        assert res.status_code == 200