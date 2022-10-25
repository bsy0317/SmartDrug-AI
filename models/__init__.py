import os
import sys

import torch
from torch.optim import Adam

from .resnet import *
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from utils import *

def load_model(args, mode):
    # Device Init
    device = None
    if torch.backends.mps.is_available():
        device = torch.device("mps")
    elif torch.cuda.is_available():
        device = torch.device("cuda")
    if device is None:
        device = torch.device("cpu")
    torch.backends.cudnn.benchmark=True
    
    if args.data == 'shape':
        class_num = 11
    elif args.data == 'color1' or args.data == 'color2':
        class_num = 16
    elif args.data == 'all':
        class_num = (11,16,16)
    else:
        raise ValueError('args.data ERROR')
    model = resnet18(num_classes=class_num, drop_rate=args.drop_rate)
    if mode == 'TRAIN':
        optimizer = Adam(model.parameters(), lr=args.lr)
        resume = args.resume
    elif mode == 'TEST' or mode=='VALID':
        optimizer = None
        resume = True
    else:
        raise ValueError('InValid Flag in load_model')

    if device == 'cuda':
        CUDA_VISIBLE_DEVICES=0
        model.cuda()
        model = torch.nn.DataParallel(model).cuda()
        model.to(device)
        torch.backends.cudnn.benchmark=True
    if device == 'mps':
        model.to(device)
        model = torch.nn.DataParallel(model)
        torch.backends.cudnn.benchmark=True
    if resume:
        checkpoint = Checkpoint(model, optimizer, device=device)
        checkpoint.load(args.ckpt_path, device=device)
        best_loss = checkpoint.best_loss
        start_epoch = checkpoint.epoch+1
    else:
        best_loss = 9999
        start_epoch = 1
    return model, optimizer, best_loss, start_epoch

