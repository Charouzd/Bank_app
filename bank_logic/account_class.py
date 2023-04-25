import currency_class as c
class Account():
    
    list_of_currencies={}
    currencies=c.Currencies("./bank_logic/cnb.txt")
    
    def __init__(self, first_name, last_name,email):
        self.name = first_name
        self.surename=last_name
        self.mail=email
        self.list_of_currencies["CZK"]=0
    def add_curency(self,currency,ammount):
        self.list_of_currencies[currency]=ammount
    def dump_bank(self):
        for key in self.list_of_currencies:
            print(key+ (str)(self.list_of_currencies[key]))
    def income(self,currency,value):
        self.list_of_currencies[currency]= self.list_of_currencies[currency]+value
    def send_money(self,currency, value):
        if(self.list_of_currencies[currency]>=value):
            self.list_of_currencies[currency]= self.list_of_currencies[currency]-value
        else:
            expected_cost_in_czk=self.currencies.exchange_into_czk(currency,value)
            if(expected_cost_in_czk>=self.list_of_currencies["CZK"]):
                self.list_of_currencies[currency]= self.list_of_currencies[currency]-value
                return True
            else:
                print("poor as fuck")
                return False
    