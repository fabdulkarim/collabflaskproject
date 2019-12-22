
from flask_restful import Resource
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
import textwrap
import sys

#fadhil making changes
import string,json
import os, inspect

class MergeResource(Resource):
      
    def merge(input_file, texts, author):
        
        current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        
        font_use = current_dir + '/RobotoCondensed-Bold.ttf'
        
        try:
            response=requests.get(input_file)
            image=Image.open(BytesIO(response.content))
        except:
            print("input file is not URL")
            
        width,height=image.size
        text_ori=sys.getsizeof(texts)
        if text_ori>300 or height > 1000 or width > 1000:
            print("Your Qoutes  or Image is too long for a Quotes, Please Make it Shorter")
        else:
            font_size=round(height/15)
            font = ImageFont.truetype(font_use, size=font_size)
            font2 = ImageFont.truetype(font_use, size=font_size)
            font_author=ImageFont.truetype(font_use, size=font_size-20)
            font_author2=ImageFont.truetype(font_use, size=font_size-20)
            width_font, height_font= font.getsize(texts)

            draw = ImageDraw.Draw(image)

            a=width/3

            if width_font>a:
                pembesaran=round(width_font/text_ori)
                bagi_text=text_ori/10
                lines = textwrap.wrap(texts, bagi_text, break_long_words=False)
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
                draw.text((x, y),"-"+ author +"-", fill=color, font=font_author2) 
            
                (x2, y2) = (a, new_per)
                color2 = 'rgb(255, 255, 255)' # white color
                draw.text((x2, y2),"-"+ author +"-", fill=color2, font=font_author) 
        
            else:
                per=height/3
                a=round(width/3)
            
                (x, y) = (a+55, per-5)
                color = 'rgb(0, 0, 0)' # black color
                draw.text((x, y), texts, fill=color, font=font2) 
            
                (x2, y2) = (a+50, per)
                color2 = 'rgb(255, 255, 255)' # white color
                draw.text((x2, y2), texts, fill=color2, font=font) 
            
                (x, y) = (a-2, per+65)
                color = 'rgb(0, 0, 0)' # black color
                draw.text((x, y), "-"+ author +"-", fill=color, font=font_author2) 
 
                (x2, y2) = (a, per+70)
                color2 = 'rgb(255, 255, 255)' # white color
                draw.text((x2, y2), "-"+ author +"-", fill=color2, font=font_author) 
        
        image.save('mantap.jpg')
        #url_out = uploads('mantap.jpg')
        #return url_out

    def uploads(fileto):
        cmd = "curl -sb POST --include " + "'https://api.pixhost.to/images' " + "-H 'Content-Type: multipart/form-data; charset=utf-8' " + "-H 'Accept: application/json' " + "-F 'img=@" + fileto + "' -F 'content_type=0' > out.json" 

        os.system(cmd)
        
        with open('out.json') as src:
            lines = src.readlines()
            for i,line in enumerate(lines):
                #print(i, line)
                if i == len(lines) - 1:
                    data = json.loads(line)
                    data = data['th_url']
                   
        true_link = data.replace('thumbs','images')
        true_link = 'https://img' + ''.join(true_link[9:])

        return true_link


