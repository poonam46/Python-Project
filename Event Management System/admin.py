from datastore import DataStore
from user import User
from event import Event
import matplotlib.pyplot as plt
from utils import *

class Admin:
    def __init__(self, uid, passw):
        self.uid = uid
        self.passw= passw
        self.ds = DataStore()
        #self.user = User()
        # self.event =

        ch = 0
        while(ch != '8'):
            clear_screen()
            print("***** 🎉 ADMIN DASHBOARD 🎉 *****")
            print(f"\nWelcome 🧑‍💼{self.uid.upper()}...! 👩‍💼\n")

            print('''Select the Options :
                  1. Add Event
                  2. Update Event
                  3. Delete Event
                  4. View All Events
                  5. Search Event
                  6. View Participants
                  7. Event Analysis
                  8. Logout ''')
            
            ch = input("Enter the choice : ")

            if(ch == '1'):
                self.addEvent()
                input("\nPress Enter to continue...")
            elif(ch == '2'):
                print(self.updateEvent())
                input("\nPress Enter to continue...")
            elif(ch == '3'):
                print(self.deleteEvent())
                input("\nPress Enter to continue...")
            elif(ch == '4'):
                self.viewAllEvents()
                input("\nPress Enter to continue...")
            elif(ch == '5'):
                self.searchEvent()
                input("\nPress Enter to continue...")
            elif(ch == '6'):
                self.viewParticipants()
                input("\nPress Enter to continue...")
            elif(ch == '7'):
                self.eventAnalysis()
                input("\nPress Enter to continue...")
            elif(ch == '8'):
                print("Logout Successfully...! 👋")
                input("\nPress Enter to continue...")
                return
            else:
                print("Invalid choice")

    def addEvent(self):
        clear_screen()
        eid = input("Enter Event ID : ")
         # 🔷 Step 1: Check if ID already exists
        fp = self.ds.getFilePointer('eventDetails')

        for line in fp:
            data = line.strip().split(',')

            if data[0].strip() == eid:
                print("❌ Error: Event ID already exists!")
                return
        ename = input("Enter Event Name : ")
        reg_start_date = input("Enter Event Registration Start Date : ")
        reg_end_date = input("Enter Event Registration End Date : ")
        date = input("Enter Event Date : ")
        time = input("Enter Event Time : ")
        orgnizer_name = input("Enter Event Organizer Name : ")
        fee = input("Enter Fee of Event : ")
        parti_limit = input("Enter how many participants can registered : ")

        ev_obj = Event(eid, ename, reg_start_date, reg_end_date, date, time, orgnizer_name, fee, parti_limit)
        self.ds.addData('eventDetails', ev_obj)
        print("✅Event Added Successfully...!")
        

    def updateEvent(self):
        clear_screen()
        id = input('Enter ID : ')
        fp = self.ds.getFilePointer('eventDetails')
        chk_id = False
        all_eve_list = []
        print("NOTE : If don't want to change the field, leave field blank")
        for ev in fp:
            ev_list =  ev.split(', ')
            if(ev_list[0] == id):
                chk_id = True
                ev_list[1] = input(f'Enter new Name ({ev_list[1]}) : ') or ev_list[1]
                ev_list[2] = input(f'Enter new Registration Date ({ev_list[2]}) : ') or ev_list[2]
                ev_list[3] = input(f"Enter new Registration End Date ({ev_list[3]}) : ")  or ev_list[3]
                ev_list[4] = input (f'Enter new Date of Event ({ev_list[4]}) : ') or ev_list[4]
                ev_list[5] = input(f'Enter new Time of Event ({ev_list[5]}) : ')  or ev_list[5]
                ev_list[6] = input(f'Enter new Organizer Name ({ev_list[6]}) :')  or ev_list[6]
                ev_list[7] = input(f'Enter Fee of Event : ({ev_list[7]}) : ') or ev_list[7]
                ev_list[8] = (input(f"Enter new Participant Limit ({ev_list[8].strip('\n')}) : ") + '\n' ) or ev_list[8]

                ev_obj = Event(ev_list[0], ev_list[1], ev_list[2], ev_list[3], ev_list[4], ev_list[5], ev_list[6], ev_list[7], ev_list[8])
                all_eve_list.append(str(ev_obj))
            else:
                all_eve_list.append(ev)
        if(chk_id):
            res = self.ds.updateData('eventDetails',all_eve_list)
            return res
        else:
            return f'{id} event not exist.'

    def deleteEvent(self):
        clear_screen()
        id = input('Enter ID : ')
        fp = self.ds.getFilePointer('eventDetails')
        chk_id = False
        all_eve_list = []
        for ev in fp:
            ev_list =  ev.split(', ')
            if(ev_list[0] == id):
                chk_id = True
                continue
            else:
                all_eve_list.append(ev)
        if(chk_id):
            res = self.ds.deleteData('eventDetails',all_eve_list)
            return res
        else:
            return f'{id} event not exist.'

    def viewAllEvents(self):
        clear_screen()
        fp = self.ds.getFilePointer('eventDetails')

        print("\n📊 ALL EVENTS")
        print("-" * 150)
        print(f"{'ID':<8}{'Name':<25}{'Reg. Start Date':<20}{'Reg. End Date':<20}{'Event Date':<15}{'Time':<12}{'Organizer':<20}{'Fee':<10}{'Participants':<8}")
        print("-" * 150)

        for line in fp:
            data = line.strip().split(',')

            #if len(data) >= 7:
            print(f"{data[0]:<8}{data[1]:<25}{data[2]:<20}{data[3]:<20}{data[4]:<15}{data[5]:<12}{data[6]:<20}{data[7]:<10}{data[8]:<8}")

        print("-" * 150)
        #input("\nPress Enter to continue...")

    def searchEvent(self, id=None):
        clear_screen()
        if id is None:
            id = input("Enter Event ID: ")

        fp = self.ds.getFilePointer('eventDetails')

        print("\n📊 SEARCH RESULT")
        print("-" * 80)
        print(f"{'ID':<10}{'Name':<20}{'Date':<15}{'Time':<12}{'Fee':<10}")
        print("-" * 80)

        found = False

        for ev in fp:
            ev_list = ev.strip().split(',')

            if ev_list[0].strip() == id:
                print(f"{ev_list[0]:<10}{ev_list[1]:<20}{ev_list[4]:<15}{ev_list[5]:<12}{ev_list[7]:<10}")
                found = True
                break

        if not found:
            print("❌ Event not found")

        print("-" * 80)

        #input("\nPress Enter to continue...")


    def viewParticipants(self):
        clear_screen()
        try:
            reg_fp = self.ds.getFilePointer('eventRegistration')
            event_fp = self.ds.getFilePointer('eventDetails')
            user_fp = self.ds.getFilePointer('userDetails')

            # 🔷 Step 1: Event mapping
            events = {}
            for line in event_fp:
                data = line.strip().split(',')
                if len(data) >= 2:
                    events[data[0].strip()] = data[1].strip()

            # 🔷 Step 2: Username → Full Name mapping
            users = {}
            for line in user_fp:
                data = line.strip().split(',')
                if len(data) >= 5:
                    username = data[4].strip()
                    fullname = data[0].strip() + " " + data[1].strip()
                    users[username] = fullname

            # 🔷 Step 3: Initialize participants
            participants = {eid: [] for eid in events}

            # 🔷 Step 4: Fill participants
            for line in reg_fp:
                data = line.strip().split(',')

                if len(data) >= 2:
                    username = data[0].strip()
                    event_id = data[1].strip()

                    name = users.get(username, username)  # fallback if not found

                    if event_id in participants:
                        participants[event_id].append(name)

            # 🔷 Step 5: Display
            print("\n👥 PARTICIPANTS FOR ALL EVENTS")
            print("-" * 40)

            for eid, names in participants.items():
                print(f"\n🎯 Event: {events[eid]} (ID: {eid})")
                print("-" * 30)

                if names:
                    for n in names:
                        print(n)
                else:
                    print("❌ No participants found")

            #input("\nPress Enter to continue...")

        except Exception as e:
            print("❌ Error:", e)

       

    def eventAnalysis(self):
        ch = 0
        while(ch != '5'):
            clear_screen()
            print("\n📊 EVENT ANALYSIS")

            print('''Select:
            1. Participants per Event
            2. Revenue per Event
            3. Event Analysis Report
            4. View Feedback
            5. Back''')

            ch = input("Enter choice: ")

            if ch == '1':
                self.participants_graph()

            elif ch == '2':
                self.event_revenue_chart()

            elif ch == '3':
                self.event_analysis_report()

            elif ch == '4':
                self.viewFeedback()
            elif ch == '5':
                print("Exit")
            else:
                print("Invalid choice")


    def participants_graph(self):
        clear_screen()
        event_counts = {}

        f = self.ds.getFilePointer("eventRegistration")
        for line in f:
                user, eid = line.strip().split(",")

                if eid in event_counts:
                    event_counts[eid] += 1
                else:
                    event_counts[eid] = 1

        x = list(event_counts.keys())
        y = list(event_counts.values())

        plt.figure()
        plt.bar(x, y)
        plt.title("Participants per Event")
        plt.xlabel("Event ID")
        plt.ylabel("Participants")

        plt.show()

        input("\nPress Enter to continue...")


    def event_revenue_chart(self):
        clear_screen()
        revenue = {}

        fp = self.ds.getFilePointer("paymentDetails")

        for line in fp:
            data = line.strip().split(',')

            if len(data) >= 4:
                event_id = data[1].strip()
                amount = int(data[2].strip())
                status = data[3].strip()

                if status == "PAID":
                    if event_id in revenue:
                        revenue[event_id] += amount
                    else:
                        revenue[event_id] = amount

        if not revenue:
            print("❌ No revenue data available")
            return

        events = list(revenue.keys())
        amounts = list(revenue.values())

        plt.figure()
        plt.bar(events, amounts)
        plt.xlabel("Event ID")
        plt.ylabel("Revenue")
        plt.title("Event-wise Revenue")

        plt.show()

        input("\nPress Enter to continue...")


    def event_analysis_report(self):
        clear_screen()
        revenue = {}
        participants = {}

        # 🔷 Revenue Calculation
        pay_fp = self.ds.getFilePointer("paymentDetails")

        for line in pay_fp:
            data = line.strip().split(',')

            if len(data) >= 4:
                event_id = data[1].strip()
                amount = int(data[2].strip())
                status = data[3].strip()

                if status == "PAID":
                    if event_id in revenue:
                        revenue[event_id] += amount
                    else:
                        revenue[event_id] = amount

        # 🔷 Participant Count
        reg_fp = self.ds.getFilePointer("eventRegistration")

        for line in reg_fp:
            data = line.strip().split(',')

            if len(data) >= 2:
                event_id = data[1].strip()

                if event_id in participants:
                    participants[event_id] += 1
                else:
                    participants[event_id] = 1

        # 🔷 Merge Data
        all_events = set(list(revenue.keys()) + list(participants.keys()))

        event_list = []
        revenue_list = []

        print("\n📊 EVENT ANALYSIS REPORT")
        print("-" * 40)

        for eid in all_events:
            rev = revenue.get(eid, 0)
            part = participants.get(eid, 0)

            print(f"Event ID: {eid}")
            print(f"Revenue: ₹{rev}")
            print(f"Participants: {part}")
            print("-" * 30)

            event_list.append(eid)
            revenue_list.append(rev)

        input("\nPress Enter to continue...")
        
    
    def viewFeedback(self):
        clear_screen()
        fp = self.ds.getFilePointer('feedback')

        for line in fp:
            data = line.strip().split(', ')
            rating = float(data[3])

            stars = "⭐" * int(rating) + "☆" * (5 - int(rating))

            print(f"User: {data[0]}")
            print(f"Event: {data[1]}")
            print(f"Feedback: {data[2]}")
            print(f"Rating: {stars}")
            print("-" * 30)

            input("\nPress Enter to continue...")