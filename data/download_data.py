import zipfile
import os
import requests

IMAGE_ZIP_DOWNLOAD = 'https://doc-04-4s-docs.googleusercontent.com/docs/securesc/l05vsjkrjdad1ik0vgla21adpmotm2hp/s69d7cbr6hkmcqvlkpnluo6iv10lhsn5/1666662525000/09102638969616469165/09102638969616469165/1yHRDtlvW8rSU0lCPqlD1gdGB8yL59pat?e=download&ax=ALW9-sDeT7MiAVikEcuTA8H7MIrMMKh5Z1nfajKpTITRLas9TADiHefDlo349PsgDBvSdY8'
CUT_IMAGE_ZIP_DOWNLOAD = 'https://doc-0c-4s-docs.googleusercontent.com/docs/securesc/l05vsjkrjdad1ik0vgla21adpmotm2hp/ss2jf7cpl4jboimja8iohof3ecr54mrq/1666714725000/09102638969616469165/09102638969616469165/1ZxAf55OMXFqVAfCzHdHGJt0OrE69yj66?e=download&ax=ALW9-sBDKg3q1b6HSSS1-gVgwIscfKj3n0h0pa4jUq4Owyd3wErcWIdQNJQoRm6wDhf4O0-'
PRE_IMAGE_ZIP_DOWNLOAD = 'https://doc-10-4s-docs.googleusercontent.com/docs/securesc/l05vsjkrjdad1ik0vgla21adpmotm2hp/n50nuo69t0lf9h558bqgfgt79ote8g9p/1666714725000/09102638969616469165/09102638969616469165/1ysDu8Fzc-5Qye9tG4zoysny-YxUPn6yl?e=download&ax=ALW9-sCncsAjKn5QbqeeGJ2MMEEsLAbwyjEVij3S7A4AIViWrKLJsVes3bIBSo11ja9AiqX'

IMAGE_ROOT = './image'
PRE_IMAGE_ROOT = './pre_image'
CUT_IMAGE_ROOT = './cut_image'

def unzip(zip_path, unzip_path):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(unzip_path)

def checkData(img_root,name):                       #arg(IMAGE_ROOT, 'image.zip')
    if not os.path.exists(img_root):
        if not os.path.isfile(name):
            print(f"{name} Download Start")
            r = requests.get(IMAGE_ZIP_DOWNLOAD)
            with open(name, 'wb') as f:
                f.write(r.content)
            print(f"{name} Download Complete")
        print(f"{name} Unzip Start")
        zip_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), name)
        unzip_path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
        unzip(zip_path, unzip_path)
        print(f"{name} Unzip Complete")
    else: 
        print(f"{img_root} folder already exists")

if __name__ == '__main__':
   checkData(IMAGE_ROOT, "image.zip")
   checkData(CUT_IMAGE_ROOT, "cut_image.zip")
   checkData(PRE_IMAGE_ROOT, "pre_image.zip")