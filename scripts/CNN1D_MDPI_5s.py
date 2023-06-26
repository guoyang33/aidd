from torch.nn.modules.container import Sequential
import torch
import torch.nn as nn
import torch.nn.functional as F


class CNN1D_MDPI_5(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv1d(128,32,32,1,padding =1)
        self.conv2 = nn.Conv1d(32,64,18,1,padding =1)
        self.conv3 = nn.Conv1d(64,128,3,1,padding =1)
        self.flatten = nn.Flatten()
        self.linear1 = nn.Linear(512,4)
        self.linear2 = nn.Linear(4,2)
        self.sigmoid = nn.Sigmoid()


    def forward(self,x):
        x = self.conv1(x)
        x = F.relu(x)
        x = F.max_pool1d(x,8)
        x = F.dropout(x,p=0.3)
        # print(x.shape)

        x = self.conv2(x)
        x = F.relu(x)
        x = F.max_pool1d(x,4)
        x = F.dropout(x,p=0.3)
        # print(x.shape)

        x = self.conv3(x)
        x = F.relu(x)
        x = F.max_pool1d(x,2)
        x = F.dropout(x,p=0.3)
        # print(x.shape)

        x = self.flatten(x)
        # print(x.shape)

        x = self.linear1(x)
        # print(x.shape)

        x = self.linear2(x)

        x = self.sigmoid(x)

        return x

# model = CNN1D_MDPI_5()
# x =torch.ones(32,128,431)
# print(model(x).shape)

