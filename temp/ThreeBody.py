# 本代码修改自 @偶尔有点小迷糊
# https://space.bilibili.com/39665558
#
# 第一次没跑通，最后发现是没有装wordcloud的库，==！

import jieba.posseg as psg


# 根据词频降序排序
def 列表中的词频排序(lst):
    word_frequency = {}
    for word in lst:
        if word in word_frequency:
            word_frequency[word] += 1
        else:
            word_frequency[word] = 1

    word_sort = sorted(word_frequency.items(), key=lambda x: x[1], reverse=True)
    return word_sort


# 生成词云
import numpy as np
from PIL import Image
from wordcloud import WordCloud, ImageColorGenerator, STOPWORDS


def 生成词云(lst):
    words_space_split = " ".join(lst)

    # 设置停用词 
    sw = set(STOPWORDS)
    sw.add("的")
    sw.add("这里不多写了，根据自己情况添加")

    # 图片模板和字体
    image = np.array(Image.open('../other/轮廓.jpg'))
    font = r'../other/simhei.ttf'

    # 生成词云
    my_wordcloud = WordCloud(scale=4, font_path=font, mask=image, stopwords=sw, background_color='white',
                             max_words=100, max_font_size=60, random_state=20).generate(words_space_split)

    # 保存生成的图片
    my_wordcloud.to_file('../output/词云.jpg')


if __name__ == "__main__":

    # 1. 打开存放项目名称的txt文件
    with open('../data/临高启明.txt', 'r', encoding='gbk') as f:
        content = (f.read())
        f.close()

    # 2. 分离出感兴趣的名词，放在 lst_words 里
    lst_words = []
    for x in psg.cut(content):
        # 保留名词、人名、地名，长度至少两个字
        if x.flag in ['n', 'nr', 'ns'] and len(x.word) > 1:
            lst_words.append(x.word)

    # 3. 按照词频由大到小排序，放在 lst_sorted 里     
    lst_sorted = 列表中的词频排序(lst_words)

    # 4. 打印TOP10
    print('\n序号\t名词\t词频\t柱图\n')
    for i in range(10):
        print('{}\t{}\t{}\t{}\n'.format(i + 1, lst_sorted[i][0], lst_sorted[i][1], '▂' * (lst_sorted[i][1] // 1000)))

    #
    生成词云([x[0] for x in lst_sorted])

