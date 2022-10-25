import pandas as pd
import os
import sys
import urllib.request as urllib
import pdb
import cv2
import threading
import rembg
import numpy as np
from tqdm import tqdm

LABEL_PATH = './label/pills_data.origin.xls'
IMAGE_ROOT = './image'
PRE_IMAGE_ROOT = './pre_image'
CUT_IMAGE_ROOT = './cut_image'
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

def remove_background(img_root, pre_root):
    ''' Remove background of images
    '''
    #SEMA = threading.Semaphore(10)
    print(f"[remove_background] Start foreach...")
    for idx, img_name in enumerate(tqdm(os.listdir(img_root), desc="Image Background Remove", mininterval=0.1)):
        try:
            threads = []
            path = os.path.join(img_root, img_name)
            pre_path = os.path.join(pre_root, img_name)
            if not os.path.isfile(path):    # if image file not exists, skipping
                continue
            if os.path.isfile(pre_path):    # if pre_image file exists, skipping remove background
                continue
            img = cv2.imread(path)
            SEMA.acquire()                  # acquire semaphore
            t = threading.Thread(target=rembg_save, args=(img, pre_path,))
            threads.append(t)
            t.start()
        except Exception as E:
            print(f"[remove_background] Error {img_name}")
            print(E)
            pass

def rembg_save(img, pre_path):
    try:
        result = rembg.bg.remove(img)
        cv2.imwrite(pre_path, result)
        SEMA.release()                  # release semaphore
    except Exception as E:
        print(f"[rembg_save] Error {pre_path}")
        print(E)
        SEMA.release()
        pass

def imgproc(pre_img_root, cut_root):   
    for idx, img_name in enumerate(tqdm(os.listdir(pre_img_root), desc="Image Cut", mininterval=0.1)):
        try:
            path = os.path.join(pre_img_root, img_name)
            cut_path = os.path.join(cut_root, img_name)
            if not os.path.isfile(path):    # if pre_image file not exists, skipping
                continue
            if os.path.isfile(cut_path):    # if cut_image file exists, skipping
                continue
            imgr = cv2.imread(path)

            image_gray = cv2.cvtColor(imgr, cv2.COLOR_BGR2GRAY) #Gray Scale
            ret, thresh1 = cv2.threshold(image_gray, 127, 255, cv2.THRESH_BINARY) #Binary Thresholding
            edged = cv2.Canny(image_gray, 30, 100) #Canny Edge Detection
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7,7)) #Morphology Kernel
            closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel) #Morphology Close
            contours, _ = cv2.findContours(closed.copy(),cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) #Find Contours

            contour_xy = np.array(contours) #Contour to Numpy Array
            x_min_0, x_max_0 = 0,0
            value = list()

            # x의 min과 max 찾기
            for j in range(len(contour_xy[0])):
                value.append(contour_xy[0][j][0][0]) #네번째 괄호가 0일때 x의 값
                x_min_0 = min(value)
                x_max_0 = max(value)

            # y의 min과 max 찾기
            y_min_0, y_max_0 = 0,0
            value = list()
            for j in range(len(contour_xy[0])):
                value.append(contour_xy[0][j][0][1]) #네번째 괄호가 0일때 x의 값
                y_min_0 = min(value)
                y_max_0 = max(value)

            trm = 10
            x0 = x_min_0
            y0 = y_min_0
            w0 = x_max_0-x_min_0+trm
            h0 = y_max_0-y_min_0+trm
            #img_trim0 = imgr[y0:y0+h0, x0:x0+w0]
            imgr = cv2.rectangle(imgr, (x0, y0), (x0+w0, y0+h0), (0, 0, 0), -1)
            if imgr.shape[0] + imgr.shape[1] < 100:
                print("[Skip] Image size is too small")
                continue
            else:
                cv2.imwrite(cut_path, imgr)
        except Exception as E:
            print(f"[Error] ImgProc {cut_path}")
            print(E)
            pass
    return 0

def imgCrop(img_root):
    ''' Croping and Resize images to 1024*512*3
    '''
    print(f"[imgCrop] Start foreach...")
    for idx, img_name in enumerate(tqdm(os.listdir(img_root), desc="Image Crop", mininterval=0.1)):
        try:
            path = os.path.join(img_root, img_name)
            if not os.path.isfile(path):
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

def main():
    #download(LABEL_PATH, IMAGE_ROOT)               # Download images
    #remove_background(IMAGE_ROOT, PRE_IMAGE_ROOT)   # Remove background
    imgproc(PRE_IMAGE_ROOT, CUT_IMAGE_ROOT)         # Image processing
    #imgCrop(IMAGE_ROOT)                            # Crop and Resize of Original images
    #imgCrop(PRE_IMAGE_ROOT)                        # Crop and Resize of Preprocessed images
    imgCrop(CUT_IMAGE_ROOT)                         # Crop and Resize of CUT images
    #sizeCheck(IMAGE_ROOT)                          # Check image size of Original images
    sizeCheck(PRE_IMAGE_ROOT)                      # Check image size of Preprocessed images
    sizeCheck(CUT_IMAGE_ROOT)                      # Check image size of Preprocessed images

if __name__ == '__main__':
    main()
