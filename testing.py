
import pickle

Status=['B','M','E','S'] # 隐含状态集
def load(filename):
    with open(filename,'rb') as pkl:
        data=pickle.load(pkl)

    return data


def viterbi(obs_, states, start_p, trans_p, emit_p):  # 维特比算法（一种递归算法）
    probablity_all = [{}] #前一个状态的概率
    path = {}
    if len(obs_) == 1:
        path['S']='S'
        return (start_p['S'],path['S'])

    for state_first in states:  # 初始值
        probablity_all[0][state_first] = start_p[state_first] + emit_p[state_first].get(obs_[0], 0)  # 在位置0，以y状态为末尾的状态序列的最大概率
        path[state_first] = [state_first]

    for t in range(1, len(obs_)):
        probablity_all.append({})
        newpath = {}
        for state_before in states:
            now=[]
            for state_now in states:
                    probablity=(probablity_all[t - 1][state_now] + trans_p[states.index(state_now)][states.index(state_before)] + emit_p[state_before].get(obs_[t], 0)) # 概率
                    now.append(probablity) # 将概率存入列表

            value,key_index=Max_line(now)
            newpath[state_before]=path[states[key_index]] + [state_before]
            probablity_all[t][state_before] = value

        path = newpath  # 记录状态序列

    (prob, state) = max([(probablity_all[len(obs_) - 1][y], y) for y in states])  # 在最后一个位置，以y状态为末尾的状态序列的最大概率

    return (prob, path[state])  # 返回概率和状态序列x

def Max_line(list):#寻找最大值
    Max=-3.14e100
    index=-1

    for i in range(len(list)):
        if list[i] > Max:
            Max = list[i]
            index = i
    return Max,index


def start_cut(obs):
    print(obs)
    Status = ['B', 'M', 'E', 'S']  # 隐含状态集
    InitStatus=load('InitStatus.pkl')
    print(InitStatus)
    TransferMatrix=load('TransferMatrix.pkl')
    print(TransferMatrix)
    Emit=load('emit.pkl')
    print(Emit)


    re=viterbi(obs,Status,InitStatus,TransferMatrix,Emit)
    print(re)

    return re

def cut(string,result):
    cut_list=[]
    for i in range(len(result)):
        word=string[i]
        if result[i] == 'E' or result[i] =='S':
            word=('{字}{标注}'.format(字=word, 标注='/'))

        cut_list.append(word)

    str=''.join(cut_list)
    print(str)

    cut_list_result=str.split('/')

    return cut_list_result



if __name__ =='__main__':

    string = '知否，知否，应是绿肥红瘦'
    res=start_cut(string)
    result=cut(string,res[1])
    print(result)

