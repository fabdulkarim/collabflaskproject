from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal
from blueprints import db, internal_required
from flask_jwt_extended import create_access_token, get_jwt_identity, get_jwt_claims, jwt_required

from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
import textwrap
import sys

bp_merge=Blueprint('merge', __name__)
api=Api(bp_merge)

class MergeResource(Resource):
    def __init__(self):
        pass
       
    def post(self, input_file, message):
        #input_file=URL IMAGE
        #message=Dictionary with text and author key
        # try:
        #     response=requests.get(input_file)
        #     image=Image.open(BytesIO(response.content))
        # except:
        #     print("input file is not URL")
        image = Image.open(BytesIO(input_file))

        width,height=image.size
        text_ori=sys.getsizeof(message["text"])
        
        font_size=round(height/9)
        print(font_size)
        font = ImageFont.truetype('RobotoCondensed-Bold.ttf', size=font_size)
        font2 = ImageFont.truetype('RobotoCondensed-Bold.ttf', size=font_size+1)
        font_author=ImageFont.truetype('RobotoCondensed-Bold.ttf', size=font_size-20)
        font_author2=ImageFont.truetype('RobotoCondensed-Bold.ttf', size=font_size-19)
        width_font, height_font= font.getsize(message["text"])

        draw = ImageDraw.Draw(image)

        a=width/3

        if width_font>a:
            pembesaran=round(width_font/text_ori)
           
            lines = textwrap.wrap(message["text"], pembesaran, break_long_words=False)
           
            new_a=a-90
            new_a_author=new_a-55
            per=0
            for text in lines:
                per=per+60
                (x, y) = (new_a-2, per-2)
                color = 'rgb(0, 0, 0)' # black color
                draw.text((x, y),text, fill=color, font=font2) 
                
                (x2, y2) = (new_a, per)
                color2 = 'rgb(255, 255, 255)' # white color
                draw.text((x2, y2),text, fill=color2, font=font) 
            
            new_per=per+70
            (x, y) = (new_a_author-2,new_per-5)
            color = 'rgb(0, 0, 0)' # black color
            draw.text((x, y),"-"+message["author"]+"-", fill=color, font=font_author2) 
            
            (x2, y2) = (new_a_author, new_per)
            color2 = 'rgb(255, 255, 255)' # white color
            draw.text((x2, y2),"-"+message["author"]+"-", fill=color2, font=font_author) 
        
        else:
            per=height/3
            a=round(width/3)
            
            (x, y) = (a-2, per-5)
            color = 'rgb(0, 0, 0)' # black color
            draw.text((x, y), message["text"], fill=color, font=font2) 
            
            (x2, y2) = (a, per)
            color2 = 'rgb(255, 255, 255)' # white color
            draw.text((x2, y2), message["text"], fill=color2, font=font) 
            
            (x, y) = (a-2, per+65)
            color = 'rgb(0, 0, 0)' # black color
            draw.text((x, y), "-"+message["author"]+"-", fill=color, font=font_author2) 
 
            (x2, y2) = (a, per+70)
            color2 = 'rgb(255, 255, 255)' # white color
            draw.text((x2, y2), "-"+message["author"]+"-", fill=color2, font=font_author) 
        
        return image.show()
        #return image.save('quotes.jpg')
        

api.add_resource(MergeResource, '')
    


