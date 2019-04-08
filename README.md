[![LICENSE](https://img.shields.io/badge/license-Anti%20996-blue.svg)](https://github.com/996icu/996.ICU/blob/master/LICENSE)
OPPOSE 996


# NFN_cutting
cutting word,viterbi,HMM,learning


# What is an NFN_CUTTing
NFN_CUTTing is a easy programe for cutting the Chinese words.


#
文件夹中包括
3个python文件

其中
HMM训练.py 用于训练模型的参数
testing.py 维特比算法和分词
词云--main--.py 主要入口 包括 词云显示 ，数据来源为excel的各种获取


3个pkl文件

InitStatus.pkl 初始参数
TransferMatrix.pkl 转移概率矩阵 参数
emit.pkl 发射/生成概率 参数

一个字体文件：
msyh.tff

数据来源为 mysql数据库 暂时还未编写


文件夹：
log参数 最新： 用于备份参数数据，防止覆盖
training_data ： 训练集,utf-8 后缀
词云示例： 3张图片，一张为原图


然后还有分词概率不太高=-=
