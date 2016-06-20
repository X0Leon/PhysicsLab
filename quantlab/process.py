# -*- coding: utf-8 -*-
"""
低温数据预处理 Data Preprocess 
仪器采集结果主要为电压信号，需要先转换成常用的物理量，如电阻、电导、载流子浓度等；
同时包含常用的数据选择和简单变换功能；

@author: Leon
"""
from Constants import e,h # 导入定义的物理常量
import pandas as pd



def toResistance(filepath, V=('RxxX','RxyX'), I=1e-7,\
                 targetCols=('MagF','RxxX','RxyX','Vg'), saveit=False):
    """
    将测量的电压信号转换为电阻
    参数：filepath为待处理的单个.dat文件
         V为需要处理的数据列名，我们测量时直接写成RxxX,RxyX
         I为测量恒流值，默认的电流为0.1uA
         targetCols用于删选实验量，可将不需要的物理量删去
         saveit指定是否保存为CSV文件，默认直接返回DataFrame
         读入文件为.dat(其实是TSV)
    """
    df = pd.read_table(filepath)
    quantity = [col.strip() for col in df.columns]  # 清理表头名的TAB空格
    df.columns = quantity   # 或用rename函数
    
    for col in df.columns:
        if col not in targetCols: del df[col]    
    
    for r in V:                        # 计算电阻，R = V/I
        df[r]=df[r].map(lambda x:x/I)  # 其实可以直接矩阵计算，但对于非计算操作只有map
    
    if saveit:
        df.to_csv(filepath.split('.dat')[0]+'.csv', sep=',', na_rep='')
        
    return df

        
def calResistConduct(df, L, w, R=('RxxX','RxyX'), savepath='D://temp.csv',\
                     Sigma=True, saveit=False):
    """
    Hall测量可以计算电阻率和电导率，只接受df对象，一般与toResistance函数配合使用
    参数：df为DataFrame对象
         L, w为器件长宽
         R指定Rxx和Rxy的列名
         Sigma说明是否计算电导
         saveit指定是否保存为CSV文件，默认保存
         返回DataFrame
    """
    Rxx, Rxy = R
    f = w/L
    Rou_xx = df[Rxx].map(lambda x:x*f)
    Rou_xy = df[Rxy]
    df['Rou_xx'] = Rou_xx
    df['Rou_xy'] = Rou_xy
    df['Rou_xy_q'] = Rou_xy/(h/(e**2))
    
    if Sigma:
        Sigma_xx = Rou_xx/(Rou_xx**2+Rou_xy**2) # element-wise直接矩阵计算
        Sigma_xy = Rou_xy/(Rou_xx**2+Rou_xy**2)
        Sigma_xx_q = Sigma_xx/(e**2/h)
        Sigma_xy_q = Sigma_xy/(e**2/h)
        df['Sigma_xx'] = Sigma_xx
        df['Sigma_xy'] = Sigma_xy
        df['Sigma_xx_q'] = Sigma_xx_q
        df['Sigma_xy_q'] = Sigma_xy_q
        
    if saveit:
        df.to_csv(savepath, sep=',', na_rep='')
    
    return df
    

def mergeFile(dataList, datatype='DataFrame', savepath='D://temp.csv',\
             targetCols=('MagF','RxxX','RxyX','Vg'), saveit=True, re=False):
    """
    归并数据列表，可以是'csv'文件，‘dat'或者'DataFrmae'对象
    savepath为保存csv文件名的位置
    targetCols选择需要归并的列    
    """
    if datatype == 'csv':
        dataList = [pd.read_csv(file) for file in dataList]
    elif datatype == 'dat':
        dataList = [pd.read_table(file) for file in dataList]
    
    mergedata = []
    for data in dataList:
        if datatype=='dat':
            data.columns = [col.strip() for col in data.columns] # 清理TAB空格
        for col in targetCols:
            mergedata.append(data[col])
    merge_df = pd.concat(mergedata, axis=1)
    if saveit:
        merge_df.to_csv(savepath, sep=',', na_rep='')
    
    if re:
        return merge_df


def oneDataset(df, col='MagF'):
    """
    一般测试时测几个来回，这里仅选一个
    col为自变量列，用于确定一个完整的回合
    """
    s_index = df[col].idxmax()   # 获取最大值的index
    e_index = df[col].idxmin()
    if s_index > e_index: # 扫的方向也有可能是先负向 
        s_index, e_index = e_index, s_index
    return df[s_index+1:e_index+1]


def selectData(Xseries, Yseries, xrange=(), withstart=True, withend=True):
    """
    画图时根据选择x轴范围选择数据，如xrange=(0, 0.1)，可以选择是否包含首尾
    TODO：该函数在应对复杂的测量过程是不是特别稳定，产生X、Y数据列不等的情形，需要升级
    """
    if len(xrange)==2:
        if withstart:
            Xseries = Xseries[Xseries>=xrange[0]]
        else:
            Xseries = Xseries[Xseries>xrange[0]]
        if withend:
            Xseries = Xseries[Xseries<=xrange[1]]
        else:
            Xseries = Xseries[Xseries<xrange[1]]
        Yseries = Yseries.loc[Xseries.index[0]:Xseries.index[-1]]
        #print(len(Xseries),len(Yseries))
    return Xseries, Yseries
    
            
def lowField(Bseries, Yseries, feature='peak', threshold=0.01, deltaY=True):
    """
    用于分析WL/WAL的预处理函数，将曲线移动B=0的中心，计算Delta值
    参数：Bseries为磁场，Yseries为电阻率或者电导率
         feature指明0 T附近是peak还是dip
         threshold用于设置寻峰的低场范围，一般剩余磁场不会超过0.01T
         deltaY说明是否同时求电阻或电导率的相对值，默认为True
    """
    Bsample = Bseries[Bseries<=threshold][Bseries>=-threshold]
    Ysample = Yseries.loc[Bsample.index[0]:Bsample.index[-1]] # 按label选择，包含首末
    if feature == 'peak':
        Bseries = Bseries - Bseries[Ysample.idxmax()]
        if deltaY: Yseries = Yseries - Ysample.max() # 虽然得到负值，但不改变形状
    elif feature == 'dip':
        Bseries = Bseries - Bseries[Ysample.idxmin()]
        if deltaY: Yseries = Yseries - Ysample.min() # 虽然得到负值，但不改变形状 
    
    return Bseries, Yseries






        
        

