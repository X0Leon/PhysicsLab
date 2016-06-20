# -*- coding: utf-8 -*-
"""
Plot 作图

@author: Leon
"""
import numpy as np
import matplotlib.pyplot as plt       
from matplotlib.patches import Rectangle  
import matplotlib.colors as colors

def shiftedColorMap(cmap, start=0, midpoint=0.5, stop=1.0, name='shiftedcmap'):
    '''
    设置colorMap的范围，例如数据中包含不对称的正负值，可以设置midpoint到数值0的位置

    参数
      cmap : The matplotlib colormap to be altered
      start : 默认0.0 (no lower ofset). 应当介于0.0和midpoint
      midpoint : 默认0.5 (no shift). 介于0.0 -1.0. 可以设置成1 - vmax/(vmax + abs(vmin))
      stop : 介于midpoint和1.0.
    参考：http://stackoverflow.com/questions/7404116/defining-the-midpoint-of-a-colormap-in-matplotlib
    '''
    cdict = {
        'red': [],
        'green': [],
        'blue': [],
        'alpha': []
    }

    reg_index = np.linspace(start, stop, 257)

    shift_index = np.hstack([
        np.linspace(0.0, midpoint, 128, endpoint=False), 
        np.linspace(midpoint, 1.0, 129, endpoint=True)
    ])

    for ri, si in zip(reg_index, shift_index):
        r, g, b, a = cmap(ri)

        cdict['red'].append((si, r, r))
        cdict['green'].append((si, g, g))
        cdict['blue'].append((si, b, b))
        cdict['alpha'].append((si, a, a))

    newcmap = colors.LinearSegmentedColormap(name, cdict)
    plt.register_cmap(cmap=newcmap)

    return newcmap


def fastPlot(XYdata,ax=None,axis_label=('X','Y','Y2'),label=[],Ydata2=None,label2=[]):
    """
    快速2D画图，且支持双Y轴作图。
    如果曲线数超过9条，启用colormap；
    如果双Y轴各有一条曲线，将Y2的yaxis,tick和label颜色全设为曲线色
    参数：XYdata是x1,y1,x2,y2...的list，可以画多条前线
         ax参数指定plot的Axes container，使该函数更具伸缩性
         axis_label指定坐标轴lable的tuple
         label可以指定每条曲线的legend
         Ydata2用于画Double Y图，y2的list
         label2指定Y2坐标轴label
    例如：
    fastPlot([[1,2],[2,3],[2,3],[4,8]],axis_label=('T (K)',r'R ($\Omega$)'),label=['L1','L2'])
    """
    if ax is None:           
        fig = plt.figure(figsize=(7,6))
        ax = fig.add_subplot(111)
    else:
        ax = ax
    
    # colormap实例参见网址：
    # http://matplotlib.org/examples/color/colormaps_reference.html
    num_lines = len(XYdata)/2
    if num_lines > 3: # 如果我们有很多条曲线，譬如说10条，那我们用colormap的渐变
        colormap = plt.cm.brg# brg 0,0.9
        ax.set_color_cycle([colormap(i) for i in np.linspace(0,0.8,num_lines)]) # highlight
    elif num_lines <= 3: # 如果一条曲线，我们将颜色设为蓝色，存在双Y轴时，另一条曲线为红色
        ax.set_color_cycle(['b', 'r','k'])
        

    lines = ax.plot(*XYdata, linestyle='-',linewidth=1)
    
    ax.set_xlabel(axis_label[0],fontsize=16)
    ax.set_ylabel(axis_label[1],fontsize=16)
    for tick in ax.xaxis.get_major_ticks() + ax.yaxis.get_major_ticks():
        tick.label.set_fontsize(14)


    # Double-Y plot
    if Ydata2 is not None:
        ax2 = ax.twinx()
        
        if num_lines > 3: # 设置曲线束的颜色
            ax2.set_color_cycle([colormap(i) for i in np.linspace(0,0.99,num_lines)])
        elif num_lines == 1:
            ax2.set_color_cycle(['r'])
            
        XYdata2 = []
        XYdata2.extend([XYdata[0],Ydata2])
        lines2 = ax2.plot(*XYdata2,linestyle='-',linewidth=1)
        ax2.set_ylabel(axis_label[2],fontsize=16)
        for tick in ax2.yaxis.get_major_ticks():
            tick.label2.set_fontsize(14)       # tick的label对象是做下两个label,label2是右上两个
        
        if num_lines ==1: # 双Y轴且只各有一条曲线时设置坐标轴的颜色与曲线相同
            ycolor = lines2[0].get_color()
            ax2.spines['right'].set_color(ycolor)
            ax2.yaxis.label.set_color(ycolor)
            [t.set_color(ycolor) for t in ax2.yaxis.get_ticklines()]
            [tl.set_color(ycolor) for tl in ax2.yaxis.get_ticklabels()]
            
        #if label2: ax2.legend(lines2, label2,fontsize=10,loc=1)
        
        # 当Double Y时，应该将连个legend合并到一起，并且添加说明，这里用Rectangle，且用split去除单位
        extra = Rectangle((0, 0), 1, 1, fill=False, edgecolor='none', linewidth=0)
        if label and label2: ax2.legend([extra]+lines+[extra]+lines2,\
                   [axis_label[1].split(' ')[0]]+label+[axis_label[2].split(' ')[0]]+label2,\
                   fontsize=11,loc='upper left',fancybox=True,framealpha=0.5)
        
        return ax,ax2 # 返回ax对象便于具体调整图的属性

    else:
        if label: ax.legend(lines,label,fontsize=11,loc=2,fancybox=True,framealpha=0.5)
        return ax
    #plt.tight_layout() 