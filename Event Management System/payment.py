class Payment:
    def __init__(self, username, event_id, amount, status):
        self.username = username
        self.event_id  = event_id
        self.amount = amount
        self.status = status

    def __str__(self):
        return f'{self.username}, {self.event_id}, {self.amount}, {self.status}'
    
if(__name__ == '__main__'):
    p1 = Payment("harshal2008", 1001, 100)
    print(p1)