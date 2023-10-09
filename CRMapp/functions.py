
from django.core.files.base import ContentFile
import base64,shortuuid

def convert_base64(code64,name1,name2):    
       
            s = shortuuid.ShortUUID(alphabet="0123456789abcdef")
            otp = s.random(length=5)
            var=code64.split('/')[1]
            image_name =  otp+  '.'+var.split(';')[0]

            extension = image_name.split('.')[1].lower()

            image_name = '{}_{}.{}'.format( name1 , name2, extension)

            imgStr = code64.split(';base64')

            new_image = ContentFile(base64.b64decode(imgStr[1]), name=image_name)

            return new_image