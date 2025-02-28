import torch
import torch.nn as nn

import matplotlib.pyplot as plt

import random
import numpy as np


# for reproducibility
def fix_seed(random_seed):
    """
    fix seed to control any randomness from a code 
    (enable stability of the experiments' results.)
    """
    torch.manual_seed(random_seed)
    torch.cuda.manual_seed(random_seed)
    torch.cuda.manual_seed_all(random_seed)  # if use multi-GPU
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False
    np.random.seed(random_seed)
    random.seed(random_seed)


class PhysicsModel(nn.Module):
    def __init__(self, model_size = 10, model_depth = 0, learning_rate = 0.01, epochs = 1000, random_seed = 20060221):
        super(PhysicsModel, self).__init__()

        fix_seed(random_seed)

        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.model_size = model_size
        self.model_depth = model_depth
        self.learning_rate = learning_rate
        self.epochs = epochs
        self.random_seed = random_seed

        layers = []
        layers.append(nn.Linear(1, self.model_size, bias=True))
        layers.append(nn.ReLU())
        for i in range(model_depth):
            layers.append(nn.Linear(self.model_size, self.model_size, bias=True))
            layers.append(nn.ReLU())
        layers.append(nn.Linear(self.model_size, 1, bias=True))

        self.model = nn.Sequential(*layers).to(self.device)

        self.criterion = torch.nn.MSELoss().to(self.device)
        self.optimizer = torch.optim.SGD(self.model.parameters(), lr=self.learning_rate)

        self.is_training = False

    
    def forward(self, x):
        return self.model(x)
    

    def train(self, x, y):
        self.is_training = True

        x = torch.FloatTensor(x).reshape(len(x), 1)
        y = torch.FloatTensor(y).reshape(len(y), 1)
        x = x.to(self.device)
        y = y.to(self.device)

        for epoch in range(1, self.epochs+1):
            self.optimizer.zero_grad()
            # forward 연산
            predict = self.model(x)

            # 비용 함수
            cost = self.criterion(predict, y)
            cost.backward()
            self.optimizer.step()

            # 100의 배수에 해당되는 에포크마다 비용을 출력
            if epoch % 100 == 0:
                print(f'Epoch: {epoch}; Error: {cost.item()}')

        self.is_training = False
    

    def test(self, x, y):
        x = torch.FloatTensor(x).reshape(len(x), 1)
        y = torch.FloatTensor(y).reshape(len(y), 1)

        x = x.to(self.device)
        y = y.to(self.device)

        with torch.no_grad():
            predict = self.model(x)
            error = self.criterion(y, predict)
            # print('모델의 예측값(Predict): ', predict.detach().cpu().numpy())
            # print('실제값(Y): ', Y.cpu().numpy())
            print("---------------------------")
            print('오차(Error): ', error.item())
    

    def graph(self, x):
        new_x = torch.linspace(np.min(x), np.max(x), 1000).reshape(1000, 1).to(self.device)

        with torch.no_grad():
            predict = self.model(new_x)
        
        return new_x.cpu().numpy(), predict.cpu().numpy()
