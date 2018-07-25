import xlrd
import re
import pickle
import os
import math


# 只使用训练数据
class HMM_Training:
    def __init__(self):
        self.transferMatrix = []  # 转移概率矩阵
        self.emitProbMatrix = {}  # 发射概率 混淆矩阵
        self.Status = ['B', 'M', 'E', 'S']  # 状态集合
        self.InitStatus_dict={} # 初始状态

        #*********以上为参数

        #训练数据
        self.symbols=[]  # 正则匹配好之后的文本 包括 中文和标点
        self.TrainingData_length=0 # 训练数据 长度

        self.sign_list_str=''# BMES 字符串 对应训练数据


        #********运行中
        self.readTrainingData('pku_training.txt')
        self.InitStatus()
        self.TransferProbablity_BMES()

        self.Emit()
        # self.InitStatus()
        # self.TransferProbablity_BMES()


        self.save(self.InitStatus_dict, 'InitStatus.pkl')
        self.save(self.transferMatrix, 'TransferMatrix.pkl')
        self.save(self.emitProbMatrix, 'emit.pkl')

    def read_file_patch(self,file_patch_name):
        file_name_list = os.listdir(file_patch_name)  # the file_name list
        return file_name_list

    #读入训练数据
    def readTrainingData(self, fileName=""): #filename  为文件名
        self.Allpart_from_word=[]
        name = self.read_file_patch('training_data')
        for fileName in name:
            with open('training_data/'+fileName,'rb') as file:
                data = file.read()
            try:
                code = data.decode('utf-8') # 解码后

                symbols = re.findall(r'[^\s/]+', code)  # 获取所有的符号 除了标注 [^\s/\a-z]+
                self.symbols.extend(symbols)


                Allpart_from_word = re.findall(r'/\w+', code)  # 获取所有标注
                self.Allpart_from_word.extend(Allpart_from_word)


            except:
                pass

        self.trainingData_status = "".join(self.Allpart_from_word)  # 连接所有的标注
        self.TrainingData_length = len(''.join(self.symbols))

        self.data_analyze()



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
        return test

    def data_analyze(self):  # 对数据进行处理 和BMES 进行对照
        # BMES  该函数得出 self.sign_list
        self.sign_list=[]

        for i in self.symbols:
            word_length = len(i)

            if word_length == 1:
                self.sign_list.append('S')
                # print(self.sign_list)
            elif word_length >= 2:
                temp_length = word_length - 2
                append_str = 'B' + temp_length * 'M' + 'E'



                self.sign_list.append(append_str)
        self.sign_list_str = ''.join(self.sign_list)

        word_=list(''.join(self.symbols))
        word_list=[]

        for i in range(len(self.symbols)):
            word_list.append('{字}{标注}'.format(字=word_[i],标注=self.sign_list_str[i]))
        print(word_list)

        self.dataANDstatus_list=word_list
        self.dataANDstatus=''.join(word_list)


    # 状态概率
    def InitStatus(self): # 初始状态分布
        self.InitStatus_dict = {}
        print(self.TrainingData_length)
        print(self.trainingData_status)

        for state in self.Status:
            self.InitStatus_dict[state] = math.log(self.sign_list_str.count(state) / self.TrainingData_length,2)
        # self.InitStatus_dict={'E':-3.14e100,'M':-3.14e100}
        # BS=['B','S']
        # print(self.TrainingData_length)
        # print(self.trainingData_status)
        #
        # S=self.sign_list_str.count('S')/self.TrainingData_length
        # B=1-S
        # self.InitStatus_dict['B']=math.log(B)
        # self.InitStatus_dict['S']=math.log(S)
        # print(self.InitStatus_dict[state])
        #对数



    def TransferProbablity_BMES(self):
        # 算BMES 转移概率 已标注

            for i in range(len(self.Status)): #行
                Matrix=[]
                for j in range(len(self.Status)):#列
                    count_before=self.sign_list_str.count(self.Status[i]) #从哪个状态开始转移

                    count_after=self.sign_list_str.count(self.Status[i]+self.Status[j]) # 同时出现的次数 且 i在前，j在后

                    if(count_before == 0):
                        probablity=3.14444 #文档中不存在该状态时
                        print("Status error")
                    elif count_after == 0:
                        probablity = -3.14e100
                    else:
                        probablity=math.log(count_after/count_before,2)



                    Matrix.append(probablity)
                    #对数
                self.transferMatrix.append(Matrix)



    def Emit(self):
        count_status={} #BMES 分别出现的次数

        new_str=''

        #初始化
        for i in self.Status:
            count_status[i] = self.sign_list_str.count(i)
            self.emitProbMatrix[i] = {}
        # print(self.emitProbMatrix)


        word_str=list(''.join(self.symbols))

        print(len(word_str))
        word_str=list(set(word_str))

        word_str = self.SBC(word_str) #全角转半角

        print(len(word_str))




        for state in self.Status:

            for k in word_str:
                add_s=('{字}{标注}'.format(字=k,标注=state))
                self.emitProbMatrix[state][k] = math.log((self.dataANDstatus_list.count(add_s)+1)/count_status[state],2)
                print(add_s)



            # count=self.sign_list_str.count()

    def save(self,file,file_name):
        with open(file_name,'wb') as output:
            pickle.dump(file,output)
            output.close()








p=HMM_Training()
# print(p.InitStatus_dict)
# print(p.transferMatrix)
# # print(p.sign_list_str[:20])
# # print(p.dataANDstatus)
# for i in p.emitProbMatrix:
#     print(i)
#     print(p.emitProbMatrix[i])








