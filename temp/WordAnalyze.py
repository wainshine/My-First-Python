# -*- coding: utf-8 -*-
"""
Created on Sat Oct 12 10:43:39 2019

@author: KX
@site:www.newview.top
!!!仅供参考，禁止抄袭!!!
"""

import function as f
import os

print("开始运行...")

# 要处理的文件名
fileName = "xaa.txt"

# 判断是否存在本地词汇统计缓存
if os.path.exists("Dict_" + fileName):
    # 存在则直接读取缓存
    words = f.getDictFromFile("Dict_" + fileName)
else:
    # 不存在则需要对文本进行分词、统计等处理

    # 文本进行分词、统计等处理
    words = f.wordCount(fileName)
    # 将处理完的词汇统计字典写入本地缓存，下次就不用再次处理文本了
    f.putDictToFile("Dict_" + fileName, words)

# 过滤停用词
words = f.filterStopWords(words, "../other/stopWords.txt")

# 生成词云
wordCloud = f.generateWordCloud(words=words, maxWords=300, maskFile="../other/china.jpg",
                                fontPath=r'../other/simhei.ttf', scale=8)
print("自动为您打开图片中...")

# 完成后自动打开图片
os.system(wordCloud)

print("运行结束")
