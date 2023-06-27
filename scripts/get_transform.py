"""
處理料的轉換函式
"""

from torchvision import transforms
import numpy as np
import librosa
from sklearn.preprocessing import StandardScaler
import torch

class PreEmphasisTransform:
    def __init__(self, coef=0.97):
        self.coef = coef

    def __call__(self, y):
        y_preemphasized = librosa.effects.preemphasis(y=y, coef=self.coef)
        return y_preemphasized

class MelSpectrogramTransform:
    def __init__(self, sr=44100, n_fft=2048, hop_length=512, win_length=None, window='hann', center=True, pad_mode='reflect', power=2.0):
        self.sr = sr
        self.n_fft = n_fft
        self.window = window
        self.hop_length = hop_length
        self.win_length = win_length
        self.center = center
        self.pad_mode = pad_mode
        self.power = power

    def __call__(self, y):
        y_mel = librosa.feature.melspectrogram(y=y, sr=self.sr, n_fft=self.n_fft, hop_length=self.hop_length, win_length=self.win_length, window=self.window, center=self.center, pad_mode=self.pad_mode, power=self.power)
        return y_mel

class PowerToDbTransform:
    def __init__(self, ref=np.max, amin=1e-10, top_db=80.0):
        self.ref = ref
        self.amin = amin
        self.top_db = top_db

    def __call__(self, y):
        y_db = librosa.power_to_db(y, ref=self.ref, amin=self.amin, top_db=self.top_db)
        return y_db

class StandardizationTransform:
    def __init__(self):
        pass

    def __call__(self, y):
        scaler = StandardScaler()
        y = scaler.fit_transform(y)
        y_standardized = y / 4
        return y_standardized

class ExpandDimsTransform:
    def __init__(self, axis=0):
        self.axis = axis

    def __call__(self, y):
        return np.expand_dims(y, axis=self.axis)
    
class ToTensorTransform:
    def __init__(self):
        pass

    def __call__(self, y):
        tensor = torch.tensor(torch.from_numpy(y),
                              dtype=torch.float32)
        return tensor


def get_transform():
    transform = transforms.Compose([
        PreEmphasisTransform(coef=0.97),
        MelSpectrogramTransform(sr=44100, n_fft=2048, hop_length=512, win_length=None, window='hann', center=True, pad_mode='reflect', power=2.0),
        PowerToDbTransform(ref=np.max, amin=1e-10, top_db=80.0),
        StandardizationTransform(),
        ExpandDimsTransform(axis=0),
        ToTensorTransform()
    ])
    return transform