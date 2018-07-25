import matplotlib.pyplot as plt
from wordcloud import WordCloud, ImageColorGenerator   #词云库
from PIL import Image
import numpy as np
import testing
import re

import xlrd
import xlwt


class Word: # 词云模块
    def __init__(self):
        #初始配置
        self.Picture_path=''#图片路径
        self.font_path=r"msyh.ttf" #字体路径
        self.background_color='white'
        self.max_font_size=50

        #文件句柄

        self.word_cutList = []  # 切分好之后的list

    #获取图片路径
    def Picture(self,picture_path=''):
        self.Picture_path=picture_path

    #获取字体路径
    def Font(self,font_path=''):
        self.font_path=font_path

    def cut_word(self,string): #分词,传入字符串
        self.sign_list=[]

        # 删除空格和换行
        re_result=re.findall(r'\S+',string)
        string = ''.join(re_result)


        self_origin_string=string  #没有被转换的字符串


        string_after=self.SBC(self_origin_string) #转成半角处理
        print(string_after)
        #删除空格和换行
        # re_result=re.findall(r'\S+',string)

        # string = ''.join(re_result)
        # print(string)

        #切分标点
        self.original_word_list=self.punctuation_cut(string_after) #原始数据经过标点切分以后产生的list

        print(self.original_word_list)
        print('****')
        print(len(self.original_word_list))

        for every_part in self.original_word_list:
            print(every_part)
            # x=input('******')
            _cutList=testing.start_cut(every_part) #开始切分
            print(_cutList)
            # x=input('end=======')
            self.sign_list.extend(_cutList[1])

        self.word_cutList=testing.cut(self_origin_string,self.sign_list)
        self.write_in_text('heheheh.txt',self.word_cutList)
        result = "/".join(self.word_cutList) #字符串形式的分词结果#####################################################
        return result

    def cut_file(self,file_patch):#读取文件内容
        with open(file_patch,'r') as file:
            data=file.read()
        return data

    # 因为训练的数据全是按半角训练的
    def SBC(self,string):
        # 全角转半角
        test = []
        for i in range(len(string)):
            word_code = ord(string[i])
            if word_code == 12288:  # 全角空格直接转换
                word_code = 32
            elif (word_code >= 65281 and word_code <= 65374):  # 全角字符（除空格）根据关系转化
                word_code -= 65248

            word = chr(word_code)
            test.append(word)
        return ''.join(test)

    def make_word_cloud(self):
        image = Image.open(self.Picture_path) # 打开图片作为底图

        graph=np.array(image)

        image.show()

        word_Cloud = WordCloud(
            font_path=self.font_path,
            background_color=self.background_color,
            max_font_size=self.max_font_size,
            mask=graph)  # ,min_font_size=10)#,mode='RGBA',colormap='pink')

        string=' '.join(self.word_cutList)
        print(string)
        print(type(string))

        word_Cloud.generate(string)

        # image_color = ImageColorGenerator(graph)#从背景图片生成颜色值
        # wc.recolor(color_func=image_color)

        word_Cloud.to_file(r"wordcloud_test2.png")  # 按照设置的像素宽高度保存绘制好的词云图，比下面程序显示更清晰

        # 4、显示图片
        plt.figure("词云图")  # 指定所绘图名称
        plt.imshow(word_Cloud)  # 以图片的形式显示词云
        plt.axis("off")  # 关闭图像坐标系
        plt.show()

    def  punctuation_cut(self,string):#按标点切分,仅仅用来切分标点
        # # 删除空格和换行
        # re_result = re.findall(r'\S+', string)
        # string_after = ''.join(re_result)
        # string = self.SBC(string_after)  # 转成半角处理


        ####################
        #传入的字符串是经过处理后的，无空白符的纯字符串

        after_cut = string.replace('。', '^。^')
        after_cut=after_cut.replace(',','^,^')
        after_cut=after_cut.replace('!','^!^')

        result=after_cut.split('^')
        if '' in result:
            result.remove('')

        return result


    def write_in_text(self,file_patch,cut_list):
        with open(file_patch,'w') as output:
            for i in cut_list:
                output.writelines(i+'\t')

# 从 excel 来的数据
class Excel_data_source:
    def __init__(self,handle=None): # 配置
        self.excel_name='' # excel 名
        self.sheet_name=[] # sheet 名，每个元素是字符串

        self.sheet_rows=0 # 行数
        self.sheet_cows=0 # 列数

        self.excel_handle=handle # 句柄
        self.sheet_handle=None

        self.data_row_start=1  #数据开始的行数,默认为1
        self.data_row_end=None  #数据结束的行数,默认为所有

        self.column=[0] # 默认第0 列 ,列表,要读取的列数,要进行处理的列数,列索引
        self.column_name_row=0 # 数据的列名 所在的行数
        self.column_name=[] # 读取到的列名

        self.excel_data={} # 读取到的数据

    def change_sheet_name(self,name_list): # 改变 excel 选取 的 sheetname
        self.sheet_name=name_list


    def change_excel_name(self, excel_name):
        self.sheet_name = excel_name

    def change_sheet_handle(self,index=-1,name=''):# 获得 sheet 句柄
        if index != -1 and type(index) == int:
            print('1')
            self.sheet_handle = self.excel_handle.sheet_by_index(index)
        elif name != '':
            self.sheet_handle = self.excel_handle.sheet_by_name(name)
        else:
            return 'Error','错误的sheet索引或者名字'

        self.sheet_cows = self.sheet_handle.ncols
        self.sheet_rows = self.sheet_handle.nrows

    def set_start_row(self,start_row):
        self.data_row_start = start_row
        return self.data_row_start

    def set_column(self,list): # 要读取的列数
        self.column = list
        return self.column

    def set_column_row(self,row):
        self.column_name_row=row
        self.column_name=self.sheet_handle.row_values(self.column_name_row)
        return self.column_name


    def open_excel(self,filename):
        self.excel_handle = xlrd.open_workbook(filename) # 打开excel 文件
        self.sheet_name=self.excel_handle.sheet_names() #获取所有的sheet名

    def close_excel(self):#关闭 excel
        pass

    def read_data(self): # 读取数据
        for i in self.column: # 对于每一个 被用户选择的列索引
            self.excel_data[i]=[] # 初始
            list=self.sheet_handle.col_values(i)
            self.excel_data[i].extend(list[self.data_row_start:])  # 读取一列所有的数据
        return self.excel_data # 格式为{列索引：【数据】}



#从 mysql 来的数据,还未写
class Mysql_data_source:
    def __init__(self):
        pass


if __name__ =='__main__':
    #测试分词和词云
    # p=Word()
    # data=p.cut_file('tr.txt')
    # p.cut_word(data)
    # p.Picture('3.png')
    #
    # p.make_word_cloud()

    #测试 excel
    ex=Excel_data_source()
    #打开
    ex.open_excel('character.xls')

    #获取sheet
    print(ex.sheet_name)
    x=ex.change_sheet_handle(0)
    print(x)
    print(type(x))

    #获取列名
    ex.set_column_row(4)
    print(ex.column_name)

    #设定要读取的列
    lit=[1,2]
    ex.set_column(lit)


    #设定数据开始的行数
    ex.set_start_row(5)

    #读取数据
    data=ex.read_data()
    print(ex.excel_data)







#
#
# image = Image.open(r'55.png')
#
# graph = np.array(image)
# # image.show()
#
#
# # 3、生成词云图，这里需要注意的是WordCloud默认不支持中文，所以这里需已下载好的中文字库
# # 无自定义背景图：需要指定生成词云图的像素大小，默认背景颜色为黑色,统一文字颜色：mode='RGBA'和colormap='pink'
# wc = WordCloud(font_path=r"msyh.ttf", background_color='white', max_font_size=50,mask=graph)  # ,min_font_size=10)#,mode='RGBA',colormap='pink')
#
#
#
#
# wc.generate(result)
#
#
# image_color = ImageColorGenerator(graph)#从背景图片生成颜色值
# wc.recolor(color_func=image_color)
#
# wc.to_file(r"wordcloud_test.png")  # 按照设置的像素宽高度保存绘制好的词云图，比下面程序显示更清晰
#
# # 4、显示图片
# plt.figure("词云图")  # 指定所绘图名称
# plt.imshow(wc)  # 以图片的形式显示词云
# plt.axis("off")  # 关闭图像坐标系
# plt.show()