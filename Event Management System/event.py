class Event:
    def __init__(self, eid, ename, reg_start_date, reg_end_date, date, time, orgnizer_name, fee, parti_limit):
        self.eid = eid
        self.ename = ename
        self.reg_start_date = reg_start_date
        self.reg_end_date = reg_end_date
        self.date = date
        self.time = time
        self.orgnizer_name = orgnizer_name
        self.fee = fee
        self.parti_limit = parti_limit

    def __str__(self):
        return f'{self.eid}, {self.ename}, {self.reg_start_date}, {self.reg_end_date}, {self.date}, {self.time}, {self.orgnizer_name}, {self.fee}, {self.parti_limit}'
    

if(__name__ == '__main__'):
    e1 = Event("E101", "Quiz Compitition", "17-March-2026", "19-March-2026","20-March-2026","11:00 AM", "Poonam Pawar", 100, 50)
    print(e1)