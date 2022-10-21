import glob
import pandas as pd
import torch
import pdb
import os
import numpy as np
import PIL
import torchvision.transforms as transforms
from torch.utils.data import DataLoader, Dataset
from PIL import Image

from config import *

def data_loader(args, mode='TRAIN'):
    if mode == 'TRAIN':
        shuffle = True
    elif mode =='VALID' or mode=='TEST':
        shuffle = False
    else:
        raise ValueError('InValid Flag in data_loader')

    dataset = Dataset(args, mode)
    dataloader = DataLoader(Dataset(args, mode),
                            batch_size=args.batch_size,
                            num_workers=0,                  # 0 for windows
                            shuffle=shuffle,
                            drop_last=True)
    return dataloader


class Dataset(torch.utils.data.Dataset):
    def __init__(self, args, mode):
        self.mode = mode
        self.data = args.data
        self.img_root = args.img_root
        self.img_path = []
        self.label_path = args.label_path
        self.shape_list = []
        self.color1_list = []
        self.color2_list = []
        self.transform = transforms.Compose([
                    transforms.RandomVerticalFlip(),
                    transforms.RandomAffine(degrees=(-25,25),translate=(0.1,0.1),
                                            scale=(0.5,1.5), shear=(-0.2,0.2)),
                    transforms.ColorJitter(saturation=0.1, brightness=0.2),
                    transforms.ToTensor()])
        file_list = os.listdir(self.img_root)
        img_list = []
        for i in range(len(file_list)):
            if file_list[i].split('.')[-1] == 'jpg':
                img_list.append(file_list[i])
        img_list = sorted(img_list, key=lambda x: int(os.path.splitext(x)[0]))
        for img_name in img_list:
            self.img_path += glob.glob(os.path.join(self.img_root, img_name))

        xls = pd.read_excel(self.label_path)
        for i in range(len(xls['의약품제형'])):
            self.shape_list.append(shapeConvert(xls['의약품제형'][i]))
            self.color1_list.append(colorConvert(xls['색상앞'][i].split(',')[0]))
            if isinstance(xls['색상뒤'][i], float):
                self.color2_list.append(colorConvert(xls['색상앞'][i].split(',')[0]))
            else:
                self.color2_list.append(colorConvert(xls['색상뒤'][i].split(',')[0]))

    def __len__(self):
        return len(self.img_path)

    def __getitem__(self, idx):
        img = Image.open(self.img_path[idx])
        if self.mode == 'TRAIN':
            img = self.transform(img)
        else:
            img = transforms.ToTensor()(img)
        if self.data == 'shape':
            label = self.shape_list[idx]
        elif self.data == 'color1':
            label = self.color1_list[idx]
        elif self.data == 'color2':
            label = self.color2_list[idx]
        else:
            label = self.shape_list[idx], self.color1_list[idx], self.color2_list[idx]
        return img, label, self.img_path[idx]
