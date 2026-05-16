class EventRegistration:
    def __init__(self, uname, event_id):
        self.uname = uname
        # self.name = name
        # self.age = age
        # self.email = email
        # self.phone = phone
        self.event_id = event_id

    def __str__(self):
        return f'{self.uname},  {self.event_id}'
    

if(__name__ == '__main__'):
    er1 = EventRegistration("E101", "Quiz Compitition", "17-March-2026", "19-March-2026","20-March-2026","11:00 AM", "Poonam Pawar", 50)
    print(er1)