import zipfile
import os
import requests

IMAGE_ZIP_DOWNLOAD = 'https://doc-04-4s-docs.googleusercontent.com/docs/securesc/l05vsjkrjdad1ik0vgla21adpmotm2hp/s69d7cbr6hkmcqvlkpnluo6iv10lhsn5/1666662525000/09102638969616469165/09102638969616469165/1yHRDtlvW8rSU0lCPqlD1gdGB8yL59pat?e=download&ax=ALW9-sDeT7MiAVikEcuTA8H7MIrMMKh5Z1nfajKpTITRLas9TADiHefDlo349PsgDBvSdY8'

def unzip(zip_path, unzip_path):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(unzip_path)

def main():
    if os.path.exists('image'):
        if not os.file.exists('image.zip'):
            print('image.zip Download Start')
            r = requests.get(IMAGE_ZIP_DOWNLOAD)
            with open('image.zip', 'wb') as f:
                f.write(r.content)
            print('image.zip Download Complete')
            return
        print('image.zip Unzip Start')
        zip_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'image.zip')
        unzip_path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
        unzip(zip_path, unzip_path)
        print('image.zip Unzip Complete')
    else: 
        print('image folder already exists')

if __name__ == '__main__':
    main()