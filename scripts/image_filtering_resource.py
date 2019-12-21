from flask import Blueprint
from flask_restful import Api, reqparse, Resource, marshal, inputs
from sqlalchemy import desc
import datetime

from blueprints import app

from blueprints import internal_required
from flask_jwt_extended import jwt_required


import hmac,hashlib
import requests

import xmltodict, json
import time                 #mengambil fungsi delay


bp_blur = Blueprint('the_blur', __name__)  
api = Api(bp_blur)

class BlurResource(Resource):
    img_task_api_host = 'http://opeapi.ws.pho.to/addtask/'
    img_get_api_host = 'http://opeapi.ws.pho.to/getresult'

    filter_blur = 'blur'
    filter2 = 'color_dominance'

######################### method POST INI HANYA UTK TESTING VIA POSTMAN ###########################
#########################       JANGAN PANGGIL ATAU COMMENT SAJA        ###########################
    def __init__(self):
        pass
    
    # @jwt_required
    # @internal_required
    def post(self):
        # self.the_app_id = args['app_id']
        # self.the_key = args['key']

        parser = reqparse.RequestParser()
        parser.add_argument('app_id', location='json', required=True)
        parser.add_argument('key',  location='json', required=True)
        parser.add_argument('img_url', location='json', required=True)


        args = parser.parse_args()

    
        result = self.proceedBlurring(args['app_id'], args['key'], args['img_url'])
        if result['status']=='successful':
            time.sleep(3)
            result1 = self.proceedDesaturate(args['app_id'], args['key'], result['img_url'])
            print(result1)
            if result1['status']=='successful':

                return {'status':'successful', 'img_url':result1['img_url']}
            else:
                return {'status':result1['status'], 'message':result1['message']}
        else:
            return {'status':result['status'], 'message':result['message']}

#########################################################################################





    def proceedDesaturate(self, app_id, app_key, img_url):

        #MENDEKATI HITAM PUTIH
        # the_data = '<image_process_call><image_url>'+img_url+'</image_url><methods_list><method><name>'+ self.filter2 +'</name><params>hue=3.5;fixed_saturation=0.3</params></method></methods_list></image_process_call>'
        
        #COVER COLOR BIRU
        the_data = '<image_process_call><image_url>'+img_url+'</image_url><methods_list><method><name>'+ self.filter2 +'</name><params>hue=3.5;fixed_saturation=0.6</params></method></methods_list></image_process_call>'
        
        the_sign_data = hmac.new(bytes(app_key, 'utf8'), bytes(the_data, 'utf8'), hashlib.sha1).hexdigest()
        form_data = {'app_id': app_id, 'sign_data': the_sign_data, 'data': the_data}

        rq = requests.post(self.img_task_api_host, data=form_data)

        resp0 = json.dumps(xmltodict.parse(rq.text))

        resp = json.loads(resp0)

        if (resp is not None) and (resp['image_process_response']['status'].lower() == 'ok'):
            req_id = resp['image_process_response']['request_id']

            result = self.proceedReqId(req_id)
            
            if (result != None) and (result['status']=='successful'):
                return {'status':'successful', 'img_url':result['img_url']}
            else:
                return {'status':'failed', 'message':'third party request error, Failed proceed get req id'}
        else:
            return {'status':'failed', 'message':'third party request error, Failed proceed task'}


    def proceedBlurring(self, app_id, app_key, img_url, count_no=3):
    
        if count_no < 1:
            return {'status':'successful','img_url':img_url}

        else:
            the_data = '<image_process_call><image_url>'+img_url+'</image_url><methods_list><method><name>'+ self.filter_blur +'</name><params>radius</params></method></methods_list></image_process_call>'
            
            the_sign_data = hmac.new(bytes(app_key, 'utf8'), bytes(the_data, 'utf8'), hashlib.sha1).hexdigest()
            form_data = {'app_id': app_id, 'sign_data': the_sign_data, 'data': the_data}

            rq = requests.post(self.img_task_api_host, data=form_data)

            resp0 = json.dumps(xmltodict.parse(rq.text))

            resp = json.loads(resp0)

            if (resp is not None) and (resp['image_process_response']['status'].lower() == 'ok'):
                req_id = resp['image_process_response']['request_id']

                result = self.proceedReqId(req_id)

                if (result != None) and (result['status']=='successful'):
                    time.sleep(3)
                    return self.proceedBlurring(app_id, app_key, result['img_url'], count_no-1)
                else:
                    return {'status':'failed', 'message':'third party request error, Failed proceed get req id'}
            else:
                return {'status':'failed', 'message':'third party request error, Failed proceed task'}   
            
    
    def proceedReqId(self, request_id):
        rq = requests.get(self.img_get_api_host, params={'request_id':request_id})
                
        if rq.status_code != 200:
            return {'status':'failed', 'message':'error dari third party api'}, 400


        resp0 = json.dumps(xmltodict.parse(rq.text))

        resp = json.loads(resp0)

        if resp is not None:
            if resp['image_process_response']['status'].lower() == 'ok':
                img_url = resp['image_process_response']['nowm_image_url']

                return {'status':'successful', 'img_url':img_url}
        else:
            return {'status':'failed', 'message':'error dari third party api'}, 400



######################### BARIS CODE INI HANYA UTK ROUTING URL REQUEST  ###########################
#########################       JANGAN PANGGIL ATAU COMMENT SAJA        ###########################
api.add_resource(BlurResource,'')   

