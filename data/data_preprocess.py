import pandas as pd
import os
import sys
import urllib.request as urllib
import pdb
import cv2
import threading
from tqdm import tqdm

LABEL_PATH = './label/pills_data.origin.xls'
IMAGE_ROOT = './image'
MASK_ROOT = './mask'
SEMA = threading.Semaphore(10)  # image download thread semaphore

def list_chunk(lst, n):
    return [lst[i:i+n] for i in range(0, len(lst), n)]

def download(label_path, output_root):
    ''' Download images based on image link
    '''
    xls = pd.read_excel(label_path)
    for i in tqdm(range(len(xls['품목일련번호'])), desc="Dataset Download", mininterval=0.1):
        try:
            threads = []
            link = xls['큰제품이미지'][i]
            name = xls['품목일련번호'][i]
            img_name = os.path.join(output_root, str(name)) + '.jpg' #preprocessing_filename path
            if os.path.isfile(img_name): #if file exists, skipping download
                #print(f"[Download] {name}...Skip")
                continue
            if not isinstance(link, str):
                print(f"[Download] {name}...No link Pass")
                continue
            if link.split(':')[0] == 'https':
                SEMA.acquire()
                t = threading.Thread(target=jpg_download, args=(link,img_name,))
                threads.append(t)
                t.start()
        except Exception as E:
            print("[Download] Error occured")
            print(E)
            pass


def jpg_download(link, path):
    try:
        urllib.urlretrieve(link, path)
        name = os.path.basename(path)
        SEMA.release()
    except:
        SEMA.release()
        pass

def imgCrop(img_root):
    ''' Croping and Resize images to 1024*512*3
    '''
    print(f"[imgCrop] Start foreach...")
    for idx, img_name in enumerate(tqdm(os.listdir(img_root), desc="Image Crop", mininterval=0.1)):
        try:
            path = os.path.join(img_root, img_name)
            if not os.path.isfile(path): #if file exists, skipping download
                continue
            img = cv2.imread(path)
            img = cv2.resize(img, (1300,710))
            img = img[10:10+650, :, :]
            img = cv2.resize(img, (1024,512))
            cv2.imwrite(path, img)
        except Exception as E:
            os.remove(os.path.join(img_root, img_name))
            pass

def sizeCheck(img_root):
    size_list = []
    print(f"[sizeCheck] Start foreach...")
    for img_name in tqdm(os.listdir(img_root), desc="Image Size Check", mininterval=0.1):
        try:
            path = os.path.join(img_root, img_name)
            img = cv2.imread(path)
            if isinstance(img, type(None)):
                print(f"[sizeCheck] Type Error {path}")
            else:
                size_list.append(img.shape)
        except Exception as E:
            print(f"[sizeCheck] File Error {img_name}")
            pass
    print(set(size_list))

#download(LABEL_PATH, IMAGE_ROOT)
imgCrop(IMAGE_ROOT)
sizeCheck(IMAGE_ROOT)
