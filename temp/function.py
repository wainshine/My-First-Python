# -*- coding: utf-8 -*-
'''
Created on Sat Oct 12 10:43:39 2019

@author: KX
@site:www.newview.top
仅供参考，禁止抄袭
'''

import wordcloud
import jieba
import datetime
from wordcloud import ImageColorGenerator


def wordCount(fileName):
    # 统计文本中的词汇
    def caculateAllLine(fileName):
        # 计算文本的总行数
        print("计算总行数中...")
        f = open(fileName, "rb")
        lineAll = 0
        for index, line in enumerate(f):
            lineAll += 1
        print('文本共%d行.' % lineAll)
        f.close()
        return lineAll

    def processText(text, words):
        # 统计一行单词

        # 分词处理
        wordsArr = jieba.lcut(text, cut_all=False)

        # 统计词汇
        for name in wordsArr:
            # if len(name) <= 1:
            #    continue
            if name not in words:
                words[name] = 1
            else:
                words[name] = words[name] + 1

    # 计算要处理的文本的总行数
    lineAll = caculateAllLine(fileName)

    print("打开文本中...")
    f = open(fileName, "rb")

    print("处理文本中...")

    # 用于统计词汇出现的次数
    words = dict()

    # 用于记录读取的行数
    lineCount = 1
    try:
        # 记录开始执行的时间
        startTime = datetime.datetime.now()
        while True:

            # 读取一行文本
            text = f.readline()

            # 如果没有读取完
            if text:

                if lineCount % 10000 == 0:
                    # 每读10000行显示一次进度

                    # 获取现在时间
                    nowTime = datetime.datetime.now()

                    # 计算已完成进度
                    finishedRatio = lineCount / lineAll

                    # 计算已花费时间
                    usedTime = (nowTime - startTime).seconds

                    # 计算剩余时间
                    remainTime = (usedTime / finishedRatio) - usedTime
                    print("处理文本中. 进度:%.2f%% 预计剩余时间:%02d:%02d:%02d 已用时间:%02d:%02d:%02d"
                          % (finishedRatio * 100, remainTime / 3600
                             , (remainTime / 60) % 60, remainTime % 60
                             , usedTime / 3600, (usedTime / 60) % 60, usedTime % 60))

                # 处理一行文本
                processText(text, words)
                lineCount = lineCount + 1
            else:
                break
    finally:
        print("文本处理完成...")
        f.close()
    return words


def generateWordCloud(words, maskFile, fontPath, scale=32, maxWords=200):
    print("生成词云中...")
    import numpy as np
    from PIL import Image

    # 生成图形遮罩
    mask = np.array(Image.open(maskFile))
    genclr = ImageColorGenerator(mask)

    # 生成词云
    wc = wordcloud.WordCloud(
        font_path=fontPath,  # 字体
        background_color="white",  # 背景颜色
        min_font_size=5,  # 最小字体大小
        max_words=maxWords,  # 词云显示的最大词数
        mask=mask,  # 造型遮盖
        scale=scale,  # 画布大小
        relative_scaling=0.4  # 词频和字体大小的关联性
    )
    wc.generate_from_frequencies(frequencies=words)

    # 对词云重新上色
    wc.recolor(color_func=genclr)
    fileName = "wordCloud_" + datetime.datetime.now().strftime("%Y%m%d%H%M%S") + ".jpg"

    # 保存词云文件
    wc.to_file(fileName)
    print("词云图片已保存至" + fileName)
    return fileName


def getDictFromFile(fileName):
    # 读取本地缓存，简单写的，Python版本不同可能会不适用
    print("读取词汇缓存中...")
    # 如果有词汇缓存就直接读缓存 就不用再次处理文本了
    f = open(fileName, "r")
    words = dict()
    try:
        char = ""
        isEnd = False
        while True:
            word = ""  # 本次读取的词语
            num = 0  # 本次词语的出现次数

            while f.read(1) != "'":
                # 读一个字符
                # 没有读到词语开始的单引号则继续读下一个字符
                # 知道读到词语开始的位置
                continue

            while True:
                # 读词语
                char = f.read(1)
                if char == "'":
                    # 读到单引号说明词语结束
                    break
                else:
                    word += char

            while f.read(1) != ":":
                # 读一个字符
                # 没有读到次数开始的单引号则继续读下一个字符
                # 知道读到次数开始的位置
                continue

            while True:
                # 读取次数
                char = f.read(1)
                if "0" <= char <= "9":
                    num = num * 10 + int(char)
                elif char == ",":
                    # 读到了,或}说明次数结束
                    break
                elif char == " ":
                    # 读到空格跳过
                    continue
                elif char == "}":
                    isEnd = True
                    break
            words[word] = num
            if isEnd:
                break
    finally:
        f.close()
    return words


def putDictToFile(fileName, words):
    # 将词汇字典写入文件 方便以后直接引用
    print("将词汇内容写入缓存中...")
    f = open(fileName, "w")
    f.write(str(words))
    f.close()


def filterStopWords(words, stopWordsFileName):
    print("过滤停用词中...")

    # 过滤长度为1的词和\开头的词
    for word in list(words):
        if len(word) == 1 or word[0] == '\\':
            words.pop(word)

    # 过滤停用词
    f = open(stopWordsFileName, "rb")
    stopWord = f.readline()
    while stopWord:

        # strip()：清空后面的\r\n   decode():将字节串转化为字符串
        stopWord = stopWord.strip().decode()
        if stopWord in words:
            words.pop(stopWord)
        stopWord = f.readline()
    f.close()
    return words
