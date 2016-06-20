# -*- coding: utf-8 -*-
"""
基于底层的三个模块进行特定的数据处理和可视化app-
我并不打算将他们非常通用化，更多的是为了在notebook中使用方便；
本模块用于Hall测量的处理

@author: Leon
"""
import matplotlib.pyplot as plt
import process, plot


def simpleVg(files, legend, L=5.5, w=2.538,xlim=(), ylim=()):
	"""
	将文件原始的文件列表化成电阻电导图，横轴为背压Vg
	参数：files为含路径的.dat文件List'
	      legend为曲线的label列表
	      L,w为Hall Bar尺寸信息，直接传递给process.calResistConduct函数
	      # 暂时弃用：xrange为显示x轴的范围
	      改用xlim, ylim的tuple,例如xlim=(-20,60)

	"""
	fig = plt.figure(figsize=(15,6))
	ax1, ax2 = fig.add_subplot(121),fig.add_subplot(122)

	dataset = []
	dataset2 = []

	#Ydata2=[]
	for i,f in enumerate(files):
	    res = process.toResistance(f)
	    RC = process.calResistConduct(res, L=L, w=w)
	    RC = process.oneDataset(RC, col='Vg')    
	    xdata = RC['Vg']
	    ydata = RC['Rou_xx']*1e-3

	    # selectData函数不是特别稳定，原始数据在扫描时由于超量程等各种原因比较复杂
	    #xdata,ydata = process.selectData(xdata, RC['Rou_xx']*1e-3, xrange=xrange)
	    dataset.extend([xdata,ydata])


	    xdata2,ydata2 = xdata, RC['Sigma_xy_q']
	    #xdata3,ydata3 = process.selectData(xdata, RC['Sigma_xy_q'], xrange=xrange)
	    dataset2.extend([xdata2,ydata2])

	alabel = (r'$V_g$ (V)',r'$\rho_{xx}$ (k$\Omega$)',r'$\rho_{xy}$ (k$\Omega$)')
	ax1 = plot.fastPlot(dataset,ax=ax1,Ydata2=None,axis_label=alabel,label=legend)

	blabel = (r'$V_g$ (V)',r'$\sigma_{xy}$ ($h/e^2$)')
	ax2 = plot.fastPlot(dataset2,ax=ax2,Ydata2=None,axis_label=blabel,label=legend)

	for ax in (ax1,ax2):
		if xlim: ax.set_xlim(xlim)
		if ylim: ax.set_ylim(ylim)

	return ax1, ax2 # 返回axes列表供配置


def simpleMag(files, legend, L=5.5, w=2.538,xlim=(), ylim=()):
	"""
	将文件原始的文件列表化成电阻(电导)图，横轴为磁场B
	参数：files为含路径的.dat文件List'
	      legend为曲线的label列表
	      L,w为Hall Bar尺寸信息，直接传递给process.calResistConduct函数
	      # 暂时弃用：xrange为显示x轴的范围
	      改用xlim, ylim的tuple,例如xlim=(-20,60)

	"""
	fig = plt.figure(figsize=(15,6))
	ax1, ax2 = fig.add_subplot(121),fig.add_subplot(122)

	dataset = []
	dataset2 = []

	#Ydata2=[]
	for i,f in enumerate(files):
	    res = process.toResistance(f)
	    RC = process.calResistConduct(res, L=L, w=w)
	    RC = process.oneDataset(RC, col='MagF')    
	    xdata = RC['MagF']
	    ydata = RC['Rou_xx']*1e-3
	    dataset.extend([xdata,ydata])


	    xdata2,ydata2 = xdata, RC['Rou_xy']*1e-3
	    dataset2.extend([xdata2,ydata2])

	alabel = (r'$B$ (T)',r'$\rho_{xx}$ (k$\Omega$)')
	ax1 = plot.fastPlot(dataset,ax=ax1,Ydata2=None,axis_label=alabel,label=legend)

	blabel = (r'$B$ (T)',r'$\rho_{xy}$ (k$\Omega$)')
	ax2 = plot.fastPlot(dataset2,ax=ax2,Ydata2=None,axis_label=blabel,label=legend)

	for ax in (ax1,ax2):
		if xlim: ax.set_xlim(xlim)
		if ylim: ax.set_ylim(ylim)

	return ax1, ax2 # 返回axes列表供配置