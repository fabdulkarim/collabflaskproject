from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
import textwrap
import sys



# create Image object with the input image

def generate_text_to_image(pilih,input_file, message):
    if pilih=='URL':
        try:
            response=requests.get(input_file)
            image=Image.open(BytesIO(response.content))
        except:
            print("input file is not URL")

    else:
        try:
            image=Image.open(input_file)
        except:
            print("input file is not image file")
        
    width,height=image.size
    text_ori=sys.getsizeof(message)


    font_size=round(height/10)
    print(font_size)
    font = ImageFont.truetype('RobotoCondensed-Bold.ttf', size=font_size)
    font2 = ImageFont.truetype('RobotoCondensed-Bold.ttf', size=font_size+1)
    width_font, height_font= font.getsize(message)

    draw = ImageDraw.Draw(image)

    a=width/3

    if width_font>a:
        print("errrr")
        pembesaran=round(width_font/text_ori)
        print(a)
        print(pembesaran)
        lines = textwrap.wrap(message, pembesaran, break_long_words=False)
        print(lines)
        per=0
        for text in lines:
            per=per+60
            (x, y) = (a-2, per-5)
            color = 'rgb(0, 0, 0)' # black color
            draw.text((x, y),text, fill=color, font=font2) 
            
            (x2, y2) = (a, per)
            color2 = 'rgb(255, 255, 255)' # white color
            draw.text((x2, y2),text, fill=color2, font=font) 
    else:
        per=height/3
        a=round(width/3)

        (x, y) = (a-2, per-5)
        color = 'rgb(0, 0, 0)' # black color
        draw.text((x, y), message, fill=color, font=font2) 
 
        (x2, y2) = (a, per)
        color2 = 'rgb(255, 255, 255)' # white color
        draw.text((x2, y2), message, fill=color2, font=font) 

  
    image.show()
    # # image.save('greeting_card.png')

x={"text": "He is a wise man who does not grieve for the things which he has not, but rejoices for those which he has. Epictetus"}
generate_text_to_image('FILE', "mentee.jpg", x['text'])
