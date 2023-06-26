'''
runpred.py
使用輸入的音檔進行失智症預測
'''
# import argparse
import os
import sys
# import time
# import numpy as np
# import pandas as pd
# import librosa
# import librosa.display
# import matplotlib.pyplot as plt
import torch
from pathlib import Path

root_dir = Path(__file__).parents[0]
sys.path.append(root_dir.__str__())
from CNN1D_MDPI_5s import CNN1D_MDPI_5

pth_path = root_dir / 'pth/best.pth'
# sys.path.append(root_dir.__str__())

if __name__ == '__main__':
    model = torch.load(pth_path)
    print(model)
    # print(root_dir)

    # print(*os.listdir(root_dir))

    torch
    # parser = argparse.ArgumentParser(description='')
    # parser.add_argument('--model', type=str, default='', help='model path')
    # parser.add_argument('--sound', type=str, default='', help='audio path')