import zipfile
import os
import requests
import gdown

IMAGE_ZIP_DOWNLOAD = '1yHRDtlvW8rSU0lCPqlD1gdGB8yL59pat'
CUT_IMAGE_ZIP_DOWNLOAD = '1ZxAf55OMXFqVAfCzHdHGJt0OrE69yj66'
PRE_IMAGE_ZIP_DOWNLOAD = '1ysDu8Fzc-5Qye9tG4zoysny-YxUPn6yl'

IMAGE_ROOT = './image'
PRE_IMAGE_ROOT = './pre_image'
CUT_IMAGE_ROOT = './cut_image'

google_path = 'https://drive.google.com/uc?id='

def unzip(zip_path, unzip_path):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(unzip_path)

def checkData(img_root,file_id,name): #Argument: IMAGE_ROOT, IMAGE_ZIP_DOWNLOAD, save_path
    if not os.path.exists(img_root):
        if not os.path.isfile(name):
            print(f"{name} Download Start")
            gdown.download(google_path+file_id,name,quiet=False)
            print(f"{name} Download Complete")
        print(f"{name} Unzip Start")
        zip_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), name)
        unzip_path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
        unzip(zip_path, unzip_path)
        print(f"{name} Unzip Complete")
    else: 
        print(f"{img_root} folder already exists")

if __name__ == '__main__':
    checkData(IMAGE_ROOT,IMAGE_ZIP_DOWNLOAD, "image.zip")
    checkData(CUT_IMAGE_ROOT,CUT_IMAGE_ZIP_DOWNLOAD,"cut_image.zip")
    checkData(PRE_IMAGE_ROOT,PRE_IMAGE_ZIP_DOWNLOAD,"pre_image.zip")