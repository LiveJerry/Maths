import numpy as np


def cost(n,c):
    return n * c;
def text(n,p0,a,x):
    p_hat = x / n;
    Z = (p_hat - p0) / np.sqrt(p0 * (1-p0) / n)
    Z_alpha = norm.ppf(1 - a)
