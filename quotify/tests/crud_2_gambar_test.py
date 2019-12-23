from flask import json, request

# from unittest import mock
# from unittest.mock import patch

from . import app, call_client, create_token, client, reset_db, create_token_nonint

class TestGambar():
    def mocked_fadhil_pro(*args, **kwargs):
        class Resp_Mock:
            def __init__(self, json_data, status_code):
                self.json_data = json_data
                self.status_code = status_code
            def json(self):
                return json_data

        return 'Tough times don\'t last, tough people do','Marshawn Lynch'

    #@mock.patch('scriptFadhil.fadhilProcess', side_effect=mocked_fadhil_pro)
    def test_post(self, client): #, test_fadpro_mock, client):
        
        token = create_token_nonint()

        data = {
            'arg1':'22b6a922-3890-41ef-879d-18af9ee7af5c',
            'arg2':'2eac58cf82mshc8201e58c8deafap170a5bjsn179d049bdd69',
            'arg3':'213',
            'arg4':'asd'
        }

        req = call_client(request)
        res = req.post('/gambar', query_string=data, files='okMtCt3F.jpg',
        headers={'Authorization': 'Bearer ' + token})

        with open('tesout.txt','w') as fileo:
            fileo.write(res.url_to_see)
        assert res.status_code == 200