# QuantLab
The architecture of data process and visualization for low temperature quantum transport experiment.

Simple toolboxs for speeding up the workflow of the two-terminal, Hall adn Nonlocal mearsuments via cryogenic instruments.

Package Tree

    QuantLab/
        |--__init__.py
        |--process    (I/O, data cleaning, simple calculation)
        |--fitting    (fitting functions, sucn as SdH oscillations)
        |--plot       (plotting component)
        |--Constants  (physical constants in SI units)
        |--appHall    (out-of-box toolkits for Hall mearsuments)
        |--tools/     (complex utils for fitting and plot)
          --__init__.py

This is a work in progress, welcome for help.


量子输运实验（两端法、Hall Bar、Nonlocal等）数据的处理和可视化。

其中，

* process、plot和fitting三个模块分别用于数据预处理、2D/3D绘图和拟合；
* tools子库中是一些复杂功能的实现，例如寻峰；
* Constants是国际单位制的物理常数；
* appHall等更顶层的模块，用于Hall bar等特定的测量结果，可以帮助快速预览测量结果；

Author: X0Leon