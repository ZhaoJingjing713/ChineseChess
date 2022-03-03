
class Rules:
    def __init__(self,pos,current_player,p1,p2):
        self.pos=pos
        self.player1=p1
        self.player2=p2
        self.current_player=current_player
        super().__init__()
    def judge(self,name,current,target):
        if(name=='zu' or name=='bin'):
            return self.bin_or_zu(name,current,target)
        elif(name=='pao'):
            return self.pao(current,target)
        elif(name=='ju'):
            return self.ju(current,target)
        elif(name=='xiang'):
            return self.xaing(current,target)
        elif(name=='ma'):
            return self.ma(current,target)
        elif(name=='shi'):
            return self.shi(current,target)
        elif(name=='iang' or name=='huai'):
            return self.jiang_or_shuai(name,current,target)
        else:
            return False
    def bin_or_zu(self,name,current,target):    #兵&卒
        if(name=='zu'):                         #卒
            if(current[0]>=5):                  #卒未过河
                if(target[1]!=current[1]):
                    return False
                elif(target[0]-current[0]!=-1):
                    return False
            else:                               #卒过河
                if(target[0]>current[0]):
                    return False
                elif(abs(target[1]-current[1])+target[0]-current[0]!=1):
                    return False
            return True
        elif(name=='bin'):                     #兵
            if(current[0]<5):                  #兵未过河
                if(target[1]!=current[1]):
                    return False
                elif(target[0]-current[0]!=1):
                    return False
            else:                              #兵过河
                if(target[0]<current[0]):
                    return False
                elif(abs(target[1]-current[1])+target[0]-current[0]!=1):
                    return False
            return True
    def pao(self,current ,target):              #炮
        num_of_rood_stone=0                                 #路径中遇到的棋子数
        if(current[0]!=target[0]and current[1]!=target[1]):
            return False
        if(current[0]==target[0]):                          #同一行移动     
            if(self.pos[target[0]][target[1]]==0):          #目标无棋子
                if(target[1]>current[1]):
                    for i in range(current[1]+1,target[1]):
                        if(self.pos[target[0]][i]!=0):      #中间遇到其他棋子
                            return False
                    return True
                else:
                    for i in range(target[1],current[1]):
                        if(self.pos[target[0]][i]!=0):      
                            return False
                    return True
            else:                                           #目标为对方棋子（由于Board类中判断了是否为敌方棋子，这里不用再判断）
                if(target[1]>current[1]):
                    for i in range(current[1]+1,target[1]):
                        if(self.pos[target[0]][i]!=0):      #中间遇到其他棋子
                            num_of_rood_stone+=1
                else:
                    for i in range(target[1]+1,current[1]):
                        if(self.pos[target[0]][i]!=0):      
                            num_of_rood_stone+=1
                if(num_of_rood_stone==1):
                    return True
                else:
                    return False
        elif(current[1]==target[1]):                        #同一列移动     
            if(self.pos[target[0]][target[1]]==0):          #目标无棋子
                if(target[0]>current[0]):
                    for i in range(current[0]+1,target[0]):
                        if(self.pos[i][target[1]]!=0):      #中间遇到其他棋子
                            return False
                    return True
                else:
                    for i in range(target[0],current[0]):
                        if(self.pos[i][target[1]]!=0):      
                            return False
                    return True
            else:                                           #目标为对方棋子（由于Board类中判断了是否为敌方棋子，这里不用再判断）
                if(target[0]>current[0]):
                    for i in range(current[0]+1,target[0]):
                        if(self.pos[i][target[1]]!=0):      #中间遇到其他棋子
                            num_of_rood_stone+=1
                else:
                    for i in range(target[0]+1,current[0]):
                        if(self.pos[i][target[1]]!=0):      
                            num_of_rood_stone+=1
                if(num_of_rood_stone==1):
                    return True
                else:
                    return False

    def ju(self,current,target):                            #车
        if(current[0]!=target[0]and current[1]!=target[1]):
            return False
        elif(current[0]==target[0]):                        #同一行
            if(current[1]>target[1]):
                for i in range(target[1]+1,current[1]):
                    if(self.pos[current[0]][i]!=0):
                        return False
                return True
            else:
                for i in range(current[1]+1,target[1]):
                    if(self.pos[current[0]][i]!=0):
                        return False
                return True
        elif(current[1]==target[1]):                        #同一列
            if(current[0]>target[0]):
                for i in range(target[0]+1,current[0]):
                    if(self.pos[i][current[1]]!=0):
                        return False
                return True
            else:
                for i in range(current[0]+1,target[0]):
                    if(self.pos[i][current[1]]!=0):
                        return False
                return True

    def xaing(self,current,target):             #象
        if(self.current_player==self.player1):  #myplayer
            if(target[0]>4):                    #不能过河
                return False
        else:
            if(target[0]<5):                    #不能过河
                return False
        if(abs(target[0]-current[0])==2 and abs(target[1]-current[1])==2):          #符合田子
            if(self.pos[(current[0]+target[0])//2][(current[1]+target[1])//2]!=0):  #堵象眼
                return False
            else:
                return True
        else:
            return False

    def ma(self,current,target):                                          #马
        if(abs(current[0]-target[0])+abs(current[1]-target[1])==3):
            if((current[0]-target[0])==2):
                if(self.pos[current[0]-1][current[1]]!=0):                #别马腿
                    return False
            elif((target[0]-current[0])==2):
                if(self.pos[current[0]+1][current[1]]!=0):
                    return False
            elif(current[1]-target[1]==2):
                if(self.pos[current[0]][current[0]-1]!=0):
                    return False
            elif(target[1]-current[1]==2):
                if(self.pos[current[0]][current[0]+1]!=0):
                    return False
            return True
        else:
            return False
    
    def shi(self,current,target):
        shi_rode=[
            #上方可走路线
            [[0,3],[1,4]],[[0,5],[1,4]],
            [[1,4],[0,5]],[[1,4],[0,3]],[[1,4],[2,3]],[[1,4],[2,5]], 
            [[2,3],[1,4]],[[2,5],[1,4]],
            #下方可走路线
            [[7,3],[8,4]],[[7,5],[8,4]],
            [[8,4],[7,5]],[[8,4],[7,3]],[[8,4],[9,3]],[[8,4],[9,5]], 
            [[9,3],[8,4]],[[9,5],[8,4]]
            #以下士可以走直线
            # [[7,3],[7,4]],[[7,3],[8,3]],[[7,3],[8,4]],[[7,4],[7,5]],[[7,4],[8,4]],[[7,4],[7,3]], [[7,5],[7,4]],[[7,5],[8,5]],[[7,5],[8,4]],
            # [[8,3],[8,4]],[[8,3],[7,3]],[[8,3],[9,3]],[[8,4],[8,5]],[[8,4],[7,4]],[[8,4],[8,3]],[[8,4],[9,4]],[[8,4],[7,5]],[[8,4],[7,3]],[[8,4],[9,3]],[[8,4],[9,5]], [[8,5],[8,4]],[[8,5],[7,5]],[[8,5],[9,5]],
            # [[9,3],[9,4]],[[9,3],[8,3]],[[9,3],[8,4]],[[9,4],[9,5]],[[9,4],[8,4]],[[9,4],[9,3]], [[9,5],[9,4]],[[9,5],[8,5]],[[9,5],[8,4]]
        ]
        rode=[current,target]
        if(shi_rode.count(rode)==0):
            return False
        else:
            return True
        #以下为替换
        # if(target[1]>5 or target[1]<3):         #横向出范围
        #     return False
        #                                         #纵向出范围
        # if(self.current_player==self.player1):  #my-player 上方
        #     if(target[0]>2):
        #         return False
        # else:                                   #op-player 下方
        #     if(target[0]<7):
        #         return False
        # if(abs(target[0]-current[0])==1 or abs(target[1]-current[1])==1):   #横纵各走一个距离为true
        #     if(self.current_player==self.player1):                          #上部
        #         if(target[0]>current[0]):

        #     return True
        # else :
        #     return False

    def jiang_or_shuai(self,name,current,target):
        if(target[1]>5 or target[1]<3):         #横向出范围
            return False
                                                #纵向出范围
        if(name=='huai'):                      #帅 上方
            if(target[0]>2):
                return False
        else:                                   #将 下方
            if(target[0]<7):
                return False
        if(abs(target[0]-current[0])+abs(target[1]-current[1])==1):   #横纵各走一个距离为true
            return True
        else :
            return False