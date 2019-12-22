import json
from . import app,client
import hashlib

class TestMerge():

    def test_long_valid_input(self,client):
        data={'input_file':"https://cdn.pixabay.com/photo/2019/12/05/12/32/penguin-4675025_960_720.jpg"
        ,'texts':"Epictetus was a Greek Stoic philosopher. He was born a slave at Hierapolis, Phrygia and lived in Rome until his banishment, when he went to Nicopolis in northwestern Greece for the rest of his life."
        ,'author':"Epectitus"}
        

        res= client.post('/merge', json=data, content_type="application/json")
        res_json=json.loads(res.data)
        assert res.status_code==200
    
    def test_invalid_input(self,client):
        data={'input_file':"htt//cdn.pixabay.com/photo/2019/12/05/12/32/penguin-4675025_960_720.jpg"
        ,'texts':"Epictetus was a Greek Stoic philosopher. He was born a slave at Hierapolis, Phrygia and lived in Rome until his banishment, when he went to Nicopolis in northwestern Greece for the rest of his life."
        ,'author':"Epectitus"}
        

        res= client.post('/merge', json=data, content_type="application/json")
        res_json=json.loads(res.data)
        assert res.status_code==500
   
    def test_short_valid_input(self,client):
        data={'input_file':"https://cdn.pixabay.com/photo/2019/12/05/12/32/penguin-4675025_960_720.jpg"
        ,'texts':"Epictetus"
        ,'author':"Epectitus"}
        

        res= client.post('/merge', json=data, content_type="application/json")
        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_long_invalid_input(self,client):
        data={'input_file':"https://cdn.pixabay.com/photo/2019/12/05/12/32/penguin-4675025_960_720.jpg"
        ,'texts':"Epictetus was a Greek Stoic philosopher. He was born a slave at Hierapolis, Phrygia and lived in Rome until his banishment, when he went to Nicopolis in northwestern Greece for the rest of his life. balalalallalal aallalal alalalalal allalal allalalalall"
        ,'author':"Epectitus"}
        
        res= client.post('/merge', json=data, content_type="application/json")
        res_json=json.loads(res.data)
        assert res.status_code==200
        