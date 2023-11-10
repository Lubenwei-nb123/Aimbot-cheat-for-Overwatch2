# Aimbot-cheat-for-Overwatch2      
这是一个基于MoveNet实现的守望先锋2辅助瞄准系统，仅作学习交流使用.

# 使用说明
按住F键即可自动瞄准.

# 原理
## 使用模型
本辅助瞄准系统采用的是由Google于2021年提出的MoveNet模型，原论文[点此跳转](https://arxiv.org/pdf/1704.04861.pdf), 原项目[点此跳转](https://github.com/Zehaos/MobileNet).  
本项目中包括了lighting和thunder两个版本的MoveNet模型，前者速度快但是精度低，后者反之.
## 控制鼠标移动
这里使用了pydirectinput来控制鼠标移动.

# 目前不足之处
识别速度不够快，且对非人型英雄识别精度较低.  
改进思路：更换新模型YoloNet，并重新标注数据集.
