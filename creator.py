from io import BytesIO
from ftplib import FTP
from dotenv import load_dotenv
import os
load_dotenv()

ftp = FTP(os.environ["FTP_SERVER_URL"])
ftp.login(os.environ["FTP_LOGIN"], os.environ["FTP_PASS"])

from PIL import Image

ftp.sendcmd("CWD "+os.environ["FTP_THUMBS_PATH"])

allThumbsName = ftp.nlst(os.environ["FTP_THUMBS_PATH"])
allImgName = os.listdir(os.environ["IMG_FOLDER"]);
print("in the folder:", len(allImgName))

sent = 0
notSent = 0
for imgName in allImgName:
    if("th_"+imgName in allThumbsName):
        notSent += 1
        print("Already exists", imgName)
    else:
        img = Image.open(os.environ["IMG_FOLDER"]+"/"+imgName)
        img.thumbnail((200, 200))
        flo = BytesIO()
        img.save(flo, format="JPEG")
        ftp.storbinary("STOR th_"+imgName, BytesIO(flo.getvalue()))
        
        sent += 1
        print("sent", imgName)

print("all not sent:", notSent)
print("all sent:", sent)

ftp.quit()