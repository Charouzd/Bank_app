class Currencies():
    def __init__(self,path):
        self.file_path=path
        self.new_dataset()
        
    def exchange_into_czk(self,currency, ammount):
        if self.courses.keys().__contains__(currency):
            return ammount*self.courses[currency]
        else:
            return -1
        
    def exchange_czk_to(self,currency,ammount):
        if self.courses.keys().__contains__(currency):
            return ammount/self.courses[currency]
        else:
            return -1
        
    def new_dataset(self):
        with open(self.file_path,"r",encoding="utf8")as f:
            raw_data=f.read() # data+heading
            tmp=raw_data.split('\n')
            tmp.pop(0)
            tmp.pop(0)
            self.courses={}
            for line in tmp:#unseparated data
                temp=line.split('|')#separated data in form (0)země,(1)měna,(2)množství,(3)kód,(4)kurz
                cur=temp[3]
                val=temp[4].replace(",",".")
                if tmp[2] != "1":
                    x=float(temp[4].replace(",","."))
                    y=float(temp[2].replace(",","."))
                    val=x/y
                self.courses[cur]= val