# -*- coding: utf-8 -*-
"""
拟合模块，如果逐渐强大，是否也应该分成子模块

@author: Leon
"""
from Constants import e,h_bar,k_B
import numpy as np
from scipy.special import psi
from scipy.optimize import curve_fit
from scipy.integrate import quad

######################## WL/WAL拟合 ###############################
## 在石墨烯中拟合 ##
def F_psi(z):
    """
    双伽马工具函数
    """
    return np.log(z) + psi(1/2 + 1/z)

def WLfunction(B, B_fi, B_asy, B_sym):
    """
    2012 McCan公式的电导形式
    """
    return -1/(2*np.pi)*(F_psi(B/B_fi)-F_psi(B/(B_fi+2*B_asy))-2*F_psi(B/(B_fi+B_asy+B_sym)))    

def WLfunction_reduce(B, B_fi):
    """
    SO耦合为零时的McCan公式
    """
    return 1/np.pi*F_psi(B/B_fi)
    
def fitWL(Bseries, Sigma, withSO=False):
    """
    拟合弱局域化/弱反局域化，根绝E.McCan 2012 PRL石墨烯中公式
    参数：Bseries为磁场的Series数据，Sigma为纵向电导的Series数据(e^2/h为单位)
         withSO为False是拟合将B_asy和B_sym设为零，不考虑SO耦合
         
    使用如：popt = fitWL(xdata, ydata, withSO=False)
    """
    if withSO:
        f_fit = WLfunction
        popt, pcov = curve_fit(f_fit, Bseries, Sigma, p0=(1e-5,1e-5,1e-5), maxfev=4000)
    else:
        f_fit = WLfunction_reduce
        popt, pcov = curve_fit(f_fit, Bseries, Sigma, p0=1e-5, maxfev=4000)

    return popt

def calLen(B_fit):
    """
    根绝McCan拟合结果B_fit，计算L
    """
    return np.sqrt(h_bar/(4*e*B_fit))
    

############################ Tunneling I-V ###############################
## Graphene-TI隧穿结 ##
def f(E, mu=0, T=2):
    """
    Fermi-Dirac分布函数，化学势 mu=0，温度T=2K
    """
    return 1/(np.exp((E-mu)/k_B/T)+1)
    
def integrand_IV(V, *p):
    """
    被积函数，这里考虑石墨烯一侧是Dirac型，TI是2D普通DOS
    V是x数据，I是y数据，供拟合的dataset
    系数alpha可以事先预估算，A可以Handmade一个画图，然后再调整初值
    """
    A, alpha, E = p
    return A*(E*np.exp(alpha)*(f(E-e*V)-f(E)))*1e41

def funcIV(V, p):
    """
    计算数值积分
    """
    A, alpha = p
    return quad(lambda E: integrand_IV(V, A, alpha, E), 0, e*V)[0]

def vfuncIV(V, *p):
    """
    由于quad积分不具有矢量化计算特性，手动矢量化这个函数，便于curve_fit拟合，
    不需要用np.verctorize函数，因为其也用for循环，并不能提升性能
    
    使用如:fopt, fcov = curve_fit(vfunc,xdata, ydata, p0=p0)
    """
    evaluations = np.array([funcIV(i, p) for i in V])
    return evaluations
    
    
    