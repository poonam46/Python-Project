class Feedback:
    def __init__(self, username, event_id, feedback, rating):
        self.username = username
        self.event_id = event_id
        self.feedback = feedback
        self.rating = rating


    def __str__(self):
        return f'{self.username}, {self.event_id}, {self.feedback}, {self.rating}'

if(__name__ == '__main__'):
    f1 = Feedback("harshal2008",1001, "Excellent Event",4.5)
    print(f1)