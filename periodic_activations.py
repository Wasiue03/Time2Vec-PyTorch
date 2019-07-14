import torch
from torch import nn
import numpy as np
import math

def t2v(tau, f, k, w, b, w0, b0, arg=None):
    t1 = tau.repeat(1, k-1)
    if arg:
        v1 = f(torch.mm(t1, torch.t(w)) + b, arg)
    else:
        #print(w.shape, t1.shape, b.shape)
        v1 = f(torch.mm(t1, torch.t(w)) + b)
    v2 = w0 * tau + b0
    #print(v1.shape)
    return torch.cat([v1, v2], 1)

class SineActivation(nn.Module):
    def __init__(self, in_features, k):
        super(SineActivation, self).__init__()
        self.k = k
        self.w0 = nn.parameter.Parameter(torch.randn(in_features, 1))
        self.b0 = nn.parameter.Parameter(torch.randn(in_features, 1))
        self.w = nn.parameter.Parameter(torch.randn(in_features, k-1))
        self.b = nn.parameter.Parameter(torch.randn(in_features, k-1))
        self.f = torch.sin

    def forward(self, tau):
        return t2v(tau, self.f, self.k, self.w, self.b, self.w0, self.b0)

class CosineActivation(nn.Module):
    def __init__(self, in_features, k):
        super(CosineActivation, self).__init__()
        self.k = k
        self.w0 = nn.parameter.Parameter(torch.randn(in_features, 1))
        self.b0 = nn.parameter.Parameter(torch.randn(in_features, 1))
        self.w = nn.parameter.Parameter(torch.randn(in_features, k-1))
        self.b = nn.parameter.Parameter(torch.randn(in_features, k-1))
        self.f = torch.cos

    def forward(self, tau):
        return t2v(tau, self.f, self.k, self.w, self.b, self.w0, self.b0)

if __name__ == "__main__":
    sineact = SineActivation(1, 64)
    cosact = CosineActivation(1, 64)

    print(sineact(torch.Tensor([[7]])).shape)
    print(cosact(torch.Tensor([[7]])).shape)
    