import argparse
import pdb

import torch
import torch.nn as nn
import torch.backends.cudnn as cudnn
import torch.nn.functional as F
import torchvision.transforms as transforms

from dataset import *
from models import *
from utils import *
import config

MODEL_PATH = './save_model/model.pt'

def run_predict_all(args, img_path):
    # Device Init
    device = None
    device = torch.device("cpu")
    cudnn.benchmark = True

    #model = torch.load(MODEL_PATH, map_location=torch.device('cpu'))
    model, _, _, _ = load_model(args, mode='VALID')

    model.to(device)
    model.eval()
    torch.set_grad_enabled(False)

    outputs = []
    img = transforms.ToTensor()(Image.open(img_path)).to(device).unsqueeze(0)
    output = model(img)
    outputs.append(output)

    pred_shape = (output[0].cpu().detach().numpy()).argmax(axis=1)
    pred_color1 = (output[1].cpu().detach().numpy()).argmax(axis=1)
    pred_color2 = (output[2].cpu().detach().numpy()).argmax(axis=1)
    
    print(outputs)
    print(pred_shape)
    print(pred_color1)
    print(pred_color2)
    return output

def run_predict_shape(args, img_path):
    # Device Init
    device = None
    device = torch.device("cpu")
    cudnn.benchmark = True
    args.data = 'shape'
    #model = torch.load(MODEL_PATH, map_location=torch.device('cpu'))
    model, _, _, _ = load_model(args, mode='VALID')

    model.to(device)
    model.eval()
    torch.set_grad_enabled(False)

    img = transforms.ToTensor()(Image.open(img_path)).to(device).unsqueeze(0)
    output = model(img)

    pred_shape = (output.cpu().detach().numpy()).argmax(axis=0)
    
    print(output)
    print(pred_shape)
    return output

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=str, default="all",
                        help="data to train(shape, color1, color2, all)")
    parser.add_argument("--batch_size", type=int, default=10,
                        help="The batch size to load the data")
    parser.add_argument("--iter_num", type=int, default=20,
                        help="The training epochs to run.")
    parser.add_argument("--drop_rate", type=float, default=0.25,
                        help="Drop-out rate for uncertainty model")
    parser.add_argument("--img_root", type=str, default="./data/image",
                        help="The directory containing the training image dataset.")
    parser.add_argument("--label_path", type=str, default="./data/label/pills_data.origin.xls",
                        help="The directory containing the training label datgaset")
    parser.add_argument("--ckpt_path", type=str, default="./checkpoint/resnet.tar",
                        help="The directory containing the training label datgaset")
    args = parser.parse_args()

    run_predict(args, "test.jpg")