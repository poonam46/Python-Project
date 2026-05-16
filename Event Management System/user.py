from datastore import DataStore
from event_reg import EventRegistration
from feedback import Feedback
from payment import Payment
import time
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import os
from datetime import datetime
from utils import *

class User:
    def __init__(self, fname=None, lname=None, mob=None, email=None, username=None, password=None):
        self.fname = fname
        self.lname = lname
        self.mob = mob
        self.email = email
        self.username = username
        self.password = password
        self.ds = DataStore()
        self.fullname = "User"
    
    def userDashboard(self):
        ch = 0
        while(ch != '7'):
                clear_screen()
                user_fp = self.ds.getFilePointer('userDetails')
                for line in user_fp:
                    data = line.strip().split(',')
                    if data[4] == self.username:
                        self.fullname = data[0].strip() + " " + data[1].strip()
                        break
                    
                print("***** 🎊 User DASHBOARD 🎊 *****")
                print(f"\nWelcome 🧑‍💼 {self.fullname}...! 👩‍💼\n")

                print('''Select the Options :
                    1. View All Events
                    2. Search Event
                    3. Register for Event
                    4. View My Events
                    5. Payment 
                    6. Give feedback
                    7. Logout ''')
                
                ch = input("Enter the choice : ")

                if(ch == '1'):
                    self.viweAllEvents()
                elif(ch == '2'):
                    self.searchEvent()
                elif(ch == '3'):
                    self.registerForEvent()
                elif(ch == '4'):
                    self.viewMyEvents()
                elif(ch == '5'):
                    self.makePayment()
                elif(ch == '6'):
                    self.giveFeedback()
                elif(ch == '7'):
                    print("Logout Successfully...! 👋")
                    input("\nPress Enter to continue...")
                    break
                else:
                    print("Invalid choice")
                    input("\nPress Enter to continue...")

    
    def viweAllEvents(self):
        clear_screen()
        fp = self.ds.getFilePointer('eventDetails')

        print("\n📊 ALL EVENTS")
        print("-" * 150)
        print(f"{'ID':<8}{'Name':<25}{'Reg. Start Date':<20}{'Reg. End Date':<20}{'Event Date':<15}{'Time':<12}{'Organizer':<20}{'Fee':<10}{'Participants':<8}")
        print("-" * 150)

        for line in fp:
            data = line.strip().split(',')

            if len(data) >= 7:
                print(f"{data[0]:<8}{data[1]:<25}{data[2]:<20}{data[3]:<20}{data[4]:<15}{data[5]:<12}{data[6]:<20}{data[7]:<10}{data[8]:<8}")

        print("-" * 150)
        input("\nPress Enter to continue...")


   
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
        input("\nPress Enter to continue...")

    def registerForEvent(self):
        clear_screen()
        try:
            self.viweAllEvents()   

            event_id = input("\nEnter Event ID to register: ")

            # res = self.searchEvent(event_id)

            # if res:
                #uname = self.username 
                # name = input("Enter NAME : ")
                #email = self.email
                #phone = self.mob

            ev_reg = EventRegistration(self.username,  event_id)

            self.ds.addData('eventRegistration', ev_reg)

            print("✅ Registration Successful...!")

            # else:
            #     print("❌ Invalid Event ID")

        except Exception as e:
            print("❌ Error:", e)

        input("\nPress Enter to continue...")

    
    def viewMyEvents(self):
        clear_screen()
        reg_fp = self.ds.getFilePointer('eventRegistration')
        event_fp = self.ds.getFilePointer('eventDetails')

        # Event map
        event_map = {}
        for line in event_fp:
            data = line.strip().split(',')
            event_map[data[0].strip()] = data

        print("\n📊 MY EVENTS")
        print("-" * 80)
        print(f"{'ID':<8}{'Name':<25}{'Date':<20}{'Time':<10}{'Fee':<8}")
        print("-" * 80)

        for line in reg_fp:
            data = line.strip().split(',')

            if  data[0].strip() == self.username:
                event_id = data[1].strip()
                ev = event_map.get(event_id)

                if ev:
                    print(f"{ev[0]:<8}{ev[1]:<25}{ev[4]:<20}{ev[5]:<10}{ev[8]:<8}")

        print("-" * 80)
        input("\nPress Enter to continue...")

    def makePayment(self):
        clear_screen()
        try:
            print("\n💰 PAYMENT GATEWAY")

            event_id = input("Enter Event ID: ")
            amount = input("Enter Amount: ")

            print("\nSelect Payment Method:")
            print("1. Card 💳")
            print("2. UPI 📱")

            choice = input("Enter choice: ")

            if choice == '1':
                card = input("Enter Card Number: ")
                cvv = input("Enter CVV: ")
                expiry = input("Enter Expiry Date: ")

            elif choice == '2':
                upi = input("Enter UPI ID: ")

            else:
                print("❌ Invalid Payment Method")
                return

            # Simulate processing
            for i in range(3):
                print("\r⏳Processing" + "." * (i+1), end="")
                time.sleep(1)

            confirm = input("\nConfirm Payment? (yes/no): ").lower()

            if confirm == "yes":
                print("✅ Payment Successful!")
                status = "PAID"
                pay_obj = Payment(self.username, event_id, amount, status)
                self.ds.addData('paymentDetails', pay_obj)

                # 🎫 Generate Ticket
                self.generate_pdf_ticket(self.username, event_id)
            else:
                print("❌ Payment Cancelled")

        except Exception as e:
            print("❌ Error:", e)

        input("\nPress Enter to continue...")

    def generate_pdf_ticket(self, username, event_id):
                    try:
                        folder = "Tickets"

                        if not os.path.exists(folder):
                            os.makedirs(folder)

                        filename = f"{folder}/{username}_{event_id}.pdf"

                        # Create PDF
                        doc = SimpleDocTemplate(filename)
                        styles = getSampleStyleSheet()

                        content = []

                        content.append(Paragraph("🎫 EVENT TICKET", styles['Title']))
                        content.append(Spacer(1, 20))

                        content.append(Paragraph(f"<b>User:</b> {username}", styles['Normal']))
                        content.append(Paragraph(f"<b>Event ID:</b> {event_id}", styles['Normal']))
                        content.append(Paragraph(f"<b>Date:</b> {datetime.now().strftime('%d-%m-%Y')}", styles['Normal']))
                        content.append(Spacer(1, 20))

                        content.append(Paragraph("Thank you for registering!", styles['Normal']))

                        # Build PDF
                        doc.build(content)

                        print("✅ PDF Ticket Generated:", filename)

                    except Exception as e:
                        print("❌ Error:", e)

                    print("🎫 Ticket Generated Successfully!")


            
    def giveFeedback(self):
        clear_screen()
        try:
            print("\n💬 GIVE FEEDBACK")

            event_id = input("Enter Event ID: ")
            feedback = input("Enter your feedback: ")

            try:
                rating = float(input("Enter rating (1-5): "))

                if rating < 1 or rating > 5:
                    print("❌ Invalid rating")
                    return

            except ValueError:
                print("❌ Please enter a valid number (e.g., 4 or 4.5)")
                return

            feed_obj = Feedback(self.username, event_id, feedback, rating)

            self.ds.addData('feedback',feed_obj)

            print("✅ Feedback submitted successfully!")

        except Exception as e:
            print("❌ Error:", e)

        input("\nPress Enter to continue...")

    def __str__(self):
        return f'{self.fname}, {self.lname}, {self.mob}, {self.email}, {self.username}, {self.password}'
    

if(__name__ == '__main__'):
    e1 = User('Harshal','Pawar', '5241635478', 'harshal@gmail.com','harshal2008', 'harshal@123')
    print(e1)