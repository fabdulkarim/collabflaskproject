import hmac,hashlib
import requests

import xmltodict, json
import time                 #mengambil fungsi delay
from PIL import Image, ImageFilter, ImageOps, ImageDraw



img_task_api_host = 'http://opeapi.ws.pho.to/addtask/'
img_get_api_host = 'http://opeapi.ws.pho.to/getresult'

filter_blur = 'blur'
filter2 = 'color_dominance'




#proses ambil gambar dari url
# file_name = download_file('https://upload.wikimedia.org/wikipedia/commons/thumb/d/d3/Nelumno_nucifera_open_flower_-_botanic_garden_adelaide2.jpg/800px-Nelumno_nucifera_open_flower_-_botanic_garden_adelaide2.jpg')
# blurImage(file_name)

def download_file(img_url):
    local_filename = img_url.split('/')[-1]
    with requests.get(img_url, stream=True) as r:
        r.raise_for_status()
        try:
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192): 
                    if chunk: # filter out keep-alive new chunks
                        f.write(chunk)


                return local_filename        
        except Exception as e:
            return e




def filterImage(file_name):
    try:
        image = Image.open(file_name)
        # return image.show()
        blurred_img = image.filter(ImageFilter.BLUR)
        

        new_img = Image.new('RGB', image.size, (66,122,181))
        new_img.putalpha(225)

        blurred_img.paste(new_img, (0, 0), new_img)

        blurred_img.save(file_name)
        return file_name
        # blurred_img.show()


    
        # image.save(sys.stdout, "PNG")
        # final_img = ImageOps.grayscale(blurred_img)
        # final_img.save(file_name)
        # image = Image.open(file_name)
        # return image.show()
    except Exception as e:
        return e


def main(img_url):
    file_name = download_file(img_url)
    return filterImage(file_name)


# def main(p_app_id, p_app_key, p_img_url):

    # result = proceedBlurring(p_app_id,  p_app_key, p_img_url)
    
    # if result['status']=='successful':
    #     time.sleep(3)
    #     result1 = proceedDesaturate(p_app_id, p_app_key, p_img_url)
    #     print(result1)
    #     if result1['status']=='successful':

    #         return {'status':'successful', 'img_url':result1['img_url']}
    #     else:
    #         return {'status':result1['status'], 'message':result1['message']}
    # else:
    #     return {'status':result['status'], 'message':result['message']}

#########################################################################################





def proceedDesaturate(app_id, app_key, img_url):

    #MENDEKATI HITAM PUTIH
    # the_data = '<image_process_call><image_url>'+img_url+'</image_url><methods_list><method><name>'+ filter2 +'</name><params>hue=3.5;fixed_saturation=0.3</params></method></methods_list></image_process_call>'
    
    #COVER COLOR BIRU
    the_data = '<image_process_call><image_url>'+img_url+'</image_url><methods_list><method><name>'+ filter2 +'</name><params>hue=3.5;fixed_saturation=0.6</params></method></methods_list></image_process_call>'
    
    the_sign_data = hmac.new(bytes(app_key, 'utf8'), bytes(the_data, 'utf8'), hashlib.sha1).hexdigest()
    form_data = {'app_id': app_id, 'sign_data': the_sign_data, 'data': the_data}

    rq = requests.post(img_task_api_host, data=form_data)

    resp0 = json.dumps(xmltodict.parse(rq.text))

    resp = json.loads(resp0)

    if (resp is not None) and (resp['image_process_response']['status'].lower() == 'ok'):
        req_id = resp['image_process_response']['request_id']

        result = proceedReqId(req_id)
        
        if (result != None) and (result['status']=='successful'):
            return {'status':'successful', 'img_url':result['img_url']}
        else:
            return {'status':'failed', 'message':'third party request error, Failed proceed get req id'}
    else:
        return {'status':'failed', 'message':'third party request error, Failed proceed task'}


def proceedBlurring(app_id, app_key, img_url, count_no=3):

    if count_no < 1:
        return {'status':'successful','img_url':img_url}

    else:
        the_data = '<image_process_call><image_url>'+img_url+'</image_url><methods_list><method><name>'+ filter_blur +'</name><params>radius</params></method></methods_list></image_process_call>'
        
        the_sign_data = hmac.new(bytes(app_key, 'utf8'), bytes(the_data, 'utf8'), hashlib.sha1).hexdigest()
        form_data = {'app_id': app_id, 'sign_data': the_sign_data, 'data': the_data}

        rq = requests.post(img_task_api_host, data=form_data)

        resp0 = json.dumps(xmltodict.parse(rq.text))

        resp = json.loads(resp0)

        if (resp is not None) and (resp['image_process_response']['status'].lower() == 'ok'):
            req_id = resp['image_process_response']['request_id']

            result = proceedReqId(req_id)

            if (result != None) and (result['status']=='successful'):
                time.sleep(3)
                return proceedBlurring(app_id, app_key, result['img_url'], count_no-1)
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

        if (resp is not None)and(resp['image_process_response']['status'].lower() == 'ok'):
            img_url = resp['image_process_response']['nowm_image_url']

            return {'status':'successful', 'img_url':img_url}
            
        else:
            return {'status':'failed', 'message':'error dari third party api, Failed to get filter result by req id'}



