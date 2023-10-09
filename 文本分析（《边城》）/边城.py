import jieba
import csv
import random

# 文件地址 可以根据文件在个人电脑上的位置进行更改
baseurl = "/Users/yekse/Desktop/text/"
# 创建词典 链表
chapterwords = []
'''每一章出现的词语'''
subchapterwords = []
words = []
people = []
peoplecount = {}
'''人物计数'''
co_occurring = {}
'''共同出现人物 '''
counts = {}
# 删除不需要的词语
wrongwords = {"那个", "明白", "一面", "过渡", "唱歌", "一切", "心中", "个人", "那么", "碾坊", "家中", "地方", "以为", "一个", "什么",
              "渡船", "自己", "爷爷", "这个", "有人", "船上", "人家", "于是", "东西", "河边", "意思", "坐在", "两人", "声音",
              "事情", "不是", "因为", "下去", "眼睛", "回来", "一点", "似乎", "鸭子", "溪边", '神气', '回家', '我们', '可以', '不能',
              '知道', '茶峒', '河街', '如何', '两个', '起来', '不知', '这件', '身边', '一只', '还是', '听到', '日子', '一些', '这种',
              '码头', '各处', '轻轻', '这些', '应当', '仿佛', '仍然', '城里', '他们', '想起', '当真', '许多', '可是', '怎么', '家里',
              '不明', '笑话', '快乐', '过去', '看看', '对于', '母亲', '那人', '上去', '吊脚楼', '进城', '一定', '城中', '吊脚', '不要',
              '答应', '女孩', '女孩子', '同时', '孩子', '船头', '街上', '不明白', '注意', '一种', '自然', '似的', '歌声', '头上',
              '那些', '说话', '有点', '你们', '伯伯', '马路', '为了', '只是', '长年', '见到', '因此', '情形', '另外', '原来', '年青人',
              '不会', '鼓声', '葫芦', '正在', '年青', '样子', '这样', '青人', '翠翠说', '不见'}
for w in wrongwords:
    jieba.del_word(w)

# 读取文本
for i in range(0, 21):
    txt = open(baseurl + '第' + str(i + 1) + "章.txt", "r", encoding='utf-8').read()
    words = words + jieba.lcut(txt)

# 删除无用字符
for word in words:
    word = word.replace("，", "").replace("！", "").replace("“", "") \
        .replace("”", "").replace("。", "").replace("？", "").replace("：", "") \
        .replace("...", "").replace("、", "").strip(' ').strip('\r\n')


# 在词典中添加人名
fo = open(baseurl + "人物.txt", "r", encoding="utf-8")
for line in fo:
    people.append(line.replace('\n', ''))  # 去掉转义字符
fo.close()
for w in people:
    jieba.add_word(w)

# 取出现次数最多的八个词语（因选择的小说中人物名称较少 故只选择了8个名字）
for w in words:
    if w == "祖父" or w == "船夫":
        w = "老船夫"
    elif w == '船总':
        w = '顺顺'
    elif w == '大老':
        w = '天保'
    elif w == '二老':
        w = '傩送'
        # 当两个名字代表同一人时
    if len(w) == 1:
        # 如果词语长度等于一直接忽略
        continue
    else:
        counts[w] = counts.get(w, 0) + 1
        #统计一个词出现次数

# 将字典转为list
items = list(counts.items())
# 降序排序
items.sort(key=lambda x: x[1], reverse=True)
for i in range(8):
    word, count = items[i]
    print("{}:{}次".format(word, count))

# 把人物出现次数写入CSV文件
cs = open(baseurl + "人物.csv", "w", encoding='utf-8-sig')
fieldnames = ['人物', '第1章', '第2章', '第3章', '第4章', '第5章', '第6章', '第7章', '第8章', '第9章', '第10章', '第11章', '第12章', '第13章',
              '第14章', '第15章', '第16章', '第17章', '第18章', '第19章', '第20章', '第21章']
'''第一排元素名'''
character = csv.DictWriter(cs, fieldnames=fieldnames)
character.writeheader()
for name in people:
    for w in fieldnames:
        peoplecount[w] = peoplecount.get(w, 0)
    peoplecount['人物'] = name
    '''第一列填入人名'''
    for i in range(0, 21):
        txt = open(baseurl + '第' + str(i + 1) + "章.txt", "r", encoding='utf-8').read()
        chapterwords = jieba.lcut(txt)
        for w in chapterwords:
            if w == "祖父" or w == "船夫":
                w = "老船夫"
            elif w == '船总':
                w = '顺顺'
            elif w == '大老':
                w = '天保'
            elif w == '二老':
                w = '傩送'
            # 当两个名字代表同一人时
            if w == name:
                peoplecount['第' + str(i + 1) + '章'] = peoplecount['第' + str(i + 1) + '章'] + 1
    character.writerow(peoplecount)
    peoplecount.clear()
cs.close()

# 统计人物共同出现次数
for name in people:
    for w in people:
        co_occurring[w] = co_occurring.get(w, 0)
    for i in range(0, 21):
        txt = open(baseurl + '第' + str(i + 1) + "章.txt", "r", encoding='utf-8').read()
        chapterwords = jieba.lcut(txt)
        length = len(chapterwords)
        for j in range(0, length):
            if chapterwords[j] == "祖父" or chapterwords[j] == "船夫":
                chapterwords[j] = "老船夫"
            elif chapterwords[j] == '船总':
                chapterwords[j] = '顺顺'
            elif chapterwords[j] == '大老':
                chapterwords[j] = '天保'
            elif chapterwords[j] == '二老':
                chapterwords[j] = '傩送'
            if chapterwords[j] == name:
                co_occurring[name] = co_occurring[name] + 1
                if j >= 50:
                    start = j - 50
                else:
                    start = 0
                if j + 50 >= length:
                    end = length - 1
                else:
                    end = j + 50
                subchapterwords = chapterwords[start:end:1]
                for w in people:
                    if w != name and w in subchapterwords:
                        co_occurring[w] = co_occurring[w] + 1
    print("{}:共出场{}次".format(name, co_occurring[name]))
    items = list(co_occurring.items())
    items.sort(key=lambda x: x[1], reverse=True)
    for i in range(0, 8):
        word, count = items[i]
        print("{}:{}次".format(word, count))
    co_occurring.clear()
    print()#换行

# 返回两个人共同出现的文本片段
def find_co_occurrence(p1, p2, k):
    count_n = 0
    for n in range(0, 21):
        txt_n = open(baseurl + '第' + str(n + 1) + "章.txt", "r", encoding='utf-8').read()
        result = jieba.tokenize(txt_n)
        result_n = list(result)
        length_n = len(result_n)
        for m in range(length_n):
            if result_n[m][0] == '老船夫':
                result_n[m] = ('老船夫', result_n[m][1], result_n[m], 2)
            elif result_n[m][0] == '顺顺':
                result_n[m] = ('顺顺', result_n[m][1], result_n[m], 2)
            elif result_n[m][0] == '大老':
                result_n[m] = ('天保', result_n[m][1], result_n[m], 2)
            elif result_n[m][0] == '二老':
                result_n[m] = ('傩送', result_n[m][1], result_n[m], 2)
            if result_n[m][0] == p1:
                if m >= 50:
                    start_n = m - 50
                else:
                    start_n = 0
                if j + 50 >= length_n:
                    end_n = length_n - 1
                else:
                    end_n = m + 50
                subresult_n = result_n[start_n:end_n:1]
                for tk in range(len(subresult_n)):
                    if subresult_n[tk][0] == p2:
                        count_n = count_n + 1
                        break
                if count_n == k:
                    for tk in range(len(subresult_n)):
                        if subresult_n[tk][0] == p1:
                            print('{' + str(subresult_n[tk][0]) + '}', end='')
                        elif subresult_n[tk][0] == p2:
                            print('[' + str(subresult_n[tk][0]) + ']', end='')
                        else:
                            print(subresult_n[tk][0], end='')
                    print() #换行

                    return 0

#随机选择一个人名
p1 = random.choice(people)
p2 = random.choice(people)
while p2 == p1:
    p2 = random.choice(people)
for i in range(3):
    k = random.randint(1, 10)
    find_co_occurrence(p1, p2, k)



