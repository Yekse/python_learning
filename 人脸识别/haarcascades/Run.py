import torch
import torchvision
import torchvision.transforms as transforms
import matplotlib.pyplot as plt
from Resnet_fashion import*
from IPython import display
import time
import sys
import random
from torch.utils.data import Dataset
from torch.utils.data import DataLoader
import torch.nn.functional as F
import numpy as np
import torch.nn as nn
import torch.optim as optim
import os
from torch.autograd import Variable
import torchvision.datasets as dsets

def use_svg_display():
    display.set_matplotlib_formats('retina')

def get_fashion_mnist_labels(labels):
    text_labels = ['t-shirt', 'trouser', 'pullover', 'dress','coat','sandal', 'shirt', 'sneaker', 'bag', 'ankle boot']
    return [text_labels[i] for i in labels]

text_labels = ['t-shirt', 'trouser', 'pullover', 'dress','coat','sandal', 'shirt', 'sneaker', 'bag', 'ankle boot']

def show_fashion_mnist(images,labels):
    use_svg_display()

    _,figs=plt.subplots(1,len(images),figsize=(25,25))#
    for f,img,lbl in zip(figs,images,labels):
        f.imshow(img.view((28,28)).numpy())
        f.set_title(lbl,color='white')
        f.axes.get_xaxis().set_visible(False)
        f.axes.get_yaxis().set_visible(False)
    plt.show()
#查看训练数据集中部分图像内容与类别
x,y=[],[]
for i in range(10):
    x.append(mnist_train[i][0])
    y.append(mnist_train[i][1])
show_fashion_mnist(x,get_fashion_mnist_labels(y))

batch_size=128

trainloader=torch.utils.data.DataLoader(mnist_train,batch_size=batch_size,shuffle=True,
                                       num_workers=2)
testloader=torch.utils.data.DataLoader(mnist_test,batch_size=batch_size,shuffle=False,
                                       num_workers=2)

net = resnet34(10,True)
net = net.cuda()

import torch.optim as optim

criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(net.parameters(), lr = 0.005,momentum = 0.9)


def train(epoch, net, dataloader):
    train_loss = 0
    net.train()

    for i, (datas, labels) in enumerate(dataloader):
        datas, labels = datas.to('cuda'), labels.to('cuda')

        optimizer.zero_grad()

        outputs = net(datas)

        loss = criterion(outputs, labels)

        loss.backward()

        optimizer.step()

        train_loss += loss.item()

    train_loss /= len(dataloader)
    return train_loss


def test(epoch, net, dataloader):
    test_loss = 0
    net.eval()

    for datas, labels in dataloader:
        datas, labels = datas.to('cuda'), labels.to('cuda')
        with torch.no_grad():
            outputs = net(datas)
            loss = criterion(outputs, labels)

            test_loss += loss.item()

    test_loss /= len(dataloader)

    return test_loss


EPOCHS = 9
train_loss = []
test_loss = []
for epoch in range(EPOCHS):

    trn_loss = train(epoch, net, trainloader)
    tst_loss = test(epoch, net, testloader)
    train_loss.append(trn_loss)
    test_loss.append(tst_loss)
    print("Epoch : %d , Batch : %2d , train_loss : %.3f,test_loss : %.3f" % (epoch + 1, i + 1, trn_loss, tst_loss))

    if (i % 1 == 0):

        correct = 0
        total = 0
        with torch.no_grad():
            for i, (datas, labels) in enumerate(testloader):
                datas, labels = datas.cuda(), labels.cuda()

                outputs = net(datas)  # 输出为batch_size x 10    输出的10列都是数值,不是概率

                _, predicted = torch.max(outputs.data, dim=1)  # _第一个是值的张量（概率），第二个是序号的张量

                # 累计数据量
                total += labels.size(0)
                # 比较有多少个预测正确
                correct += (predicted == labels).sum()  # 相同为1，不同为0，利用sum()求总和
            print(",准确率: {:.3f}%".format(correct / total * 100))

            import matplotlib.pyplot as plt
            plt.plot(train_loss, label='Training loss')
            plt.plot(test_loss, label='Validation loss')
            plt.legend()