from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal
# from blueprints import db, internal_required
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
       
    def post(self):
        #input_file=URL IMAGE
        #message=Dictionary with text and author key
        parser=reqparse.RequestParser()
        parser.add_argument('input_file', location='json', required=True)
        parser.add_argument('texts', location='json', required=True)
        parser.add_argument('author', location='json', required=True)
        args=parser.parse_args()
        try:
            response=requests.get(args['input_file'])
            image=Image.open(BytesIO(response.content))
        except:
            print("input file is not URL")
            
        width,height=image.size
        text_ori=sys.getsizeof(args['texts'])
        if text_ori>300:
            return "Your Qoutes is too long for a Quotes, Please Make it Shorter"
        else:
            font_size=round(height/15)
            font = ImageFont.truetype('RobotoCondensed-Bold.ttf', size=font_size)
            font2 = ImageFont.truetype('RobotoCondensed-Bold.ttf', size=font_size)
            font_author=ImageFont.truetype('RobotoCondensed-Bold.ttf', size=font_size-20)
            font_author2=ImageFont.truetype('RobotoCondensed-Bold.ttf', size=font_size-20)
            width_font, height_font= font.getsize(args['texts'])

            draw = ImageDraw.Draw(image)

            a=width/3

            if width_font>a:
                pembesaran=round(width_font/text_ori)
                bagi_text=text_ori/10
                lines = textwrap.wrap(args['texts'], bagi_text, break_long_words=False)
                print(lines)
                # new_a=a
                new_a_author=a-55
                per=0
                print(lines)
                for text in lines:
                    per=per+50
                    (x, y) = (a-1, per+1)
                    color = 'rgb(0, 0, 0)' # black color
                    draw.text((x, y),text, fill=color, font=font2) 
                
                    (x2, y2) = (a, per)
                    color2 = 'rgb(255, 255, 255)' # white color
                    draw.text((x2, y2),text, fill=color2, font=font) 
            
                new_per=per+70
                (x, y) = (a-1,new_per-2)
                color = 'rgb(0, 0, 0)' # black color
                draw.text((x, y),"-"+args['author']+"-", fill=color, font=font_author2) 
            
                (x2, y2) = (a, new_per)
                color2 = 'rgb(255, 255, 255)' # white color
                draw.text((x2, y2),"-"+args['author']+"-", fill=color2, font=font_author) 
        
            else:
                per=height/3
                a=round(width/3)
            
                (x, y) = (a-2, per-5)
                color = 'rgb(0, 0, 0)' # black color
                draw.text((x, y), args['texts'], fill=color, font=font2) 
            
                (x2, y2) = (a, per)
                color2 = 'rgb(255, 255, 255)' # white color
                draw.text((x2, y2), args['texts'], fill=color2, font=font) 
            
                (x, y) = (a-2, per+65)
                color = 'rgb(0, 0, 0)' # black color
                draw.text((x, y), "-"+args['author']+"-", fill=color, font=font_author2) 
 
                (x2, y2) = (a, per+70)
                color2 = 'rgb(255, 255, 255)' # white color
                draw.text((x2, y2), "-"+args['author']+"-", fill=color2, font=font_author) 
        
            # return image.save('mantap.jpg')
        return image.show()

        

api.add_resource(MergeResource, '')
    


