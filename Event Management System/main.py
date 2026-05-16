from user import User
from datastore import DataStore
from admin import Admin
from utils import *
import getpass
ds = DataStore()

def main():
    
    ch = 0
    while(ch != '3'):
        clear_screen()
        print("**** ✨🎊 Welcome To Event Management System 🎊✨ ****\n")
        print('''Select the appropriate option : 
              1. Registration
              2. Login 
              3. Exit''')
        
        ch = input("Enter the choice : ")
        if(ch == '1'):
            clear_screen()
            registration()
        elif(ch =='2'):
            clear_screen()
            login()
        elif(ch == '3'):
            print('🙏😊 Thank You for visiting our Event Management System! Visit Again! 😊🙏')
            break
        else:
            print('Invalid Choice')
            input("\nPress Enter to continue...")

        

#User registration function
def registration():
    clear_screen()
    fname = input("Enter the First Name : ")
    lname = input("Enter the Last Name : ")
    mob = input("Enter Mobile Number : ")
    email = input("Enter Email ID : ")
    username = input("Create your Username : ")
    fp = ds.getFilePointer('userDetails')
    for line in fp:
            data = line.strip().split(',')

            if data[0].strip() == username:
                print("❌ Error: Username already exists!")
                input("\nPress Enter to continue...")
                return
    password = getpass.getpass("Create your Password : ")
    password = hash_password(password)
    
    # here we need to create user class
    user_obj = User(fname, lname, mob, email, username, password)
    ds.addData('userDetails', user_obj)
    print('✅ Registration done successfully...')
    input("\nPress Enter to continue...")
    
    #return res

# Login function for admin and user
def login():
    ch = 0

    while(ch != '3'):
        clear_screen()
        print('''Select the Role for Login
                1. Admin
                2. User 
                3. Exit''')
            
        ch = input('Enter your choice : ')
        
        if(ch == '1'):
            clear_screen()
            adminLogin()
        elif(ch == '2'):
            clear_screen()
            userLogin()
        elif(ch == '3'):
            print("Thank You for Login...!😊")
        else:
            print('Invalid Choice')
            input("\nPress Enter to continue...")

# Admin login function
def adminLogin():
    uid = 'admin'
    passw = 'admin@123'

    count = 3
    username = input('Enter Username : ')
    password = getpass.getpass('Enter Password : ')
    #password = hash_password(password)

    if(uid == username and passw == password):
                print("✅ Login Successfully...")
                clear_screen()
                ad = Admin(uid, passw)
                
    else:
        print("❌ Invalid Credentials...")
        print("You get 3 more chances to login\n")
        while(count > 0):
            # clear_screen()
            username = input('Enter Username : ')
            password = getpass.getpass('Enter Password : ')
           #password = hash_password(password)

            if(uid == username and passw == password):
                print("✅ Login Successfully...")
                input("\nPress Enter to continue...")
                clear_screen()
                ad = Admin(uid, passw)
                break
            else:
                clear_screen()
                print("❌ Invalid Credentials...")
                count -= 1
                print(f"Remaining chances are {count}")

        print("🚫 Too many failed attempts!")
        input("\nPress Enter to continue...")

# User login function
def userLogin():
    username = input("Enter Username : ")
    password = getpass.getpass("Enter Password :  ")
    password = hash_password(password)

    fp = ds.getFilePointer('userDetails')
    for user in fp:
        user_list =  user.split(', ')
    
        if(user_list[4] == username and user_list[5].strip('\n') == password):
            print("✅ Login Successfully...")
            clear_screen()
            user_obj = User(user_list[0], user_list[1], user_list[2], user_list[3], user_list[4], user_list[5])
            user_obj.userDashboard()
            break
        else:
            # clear_screen()
            print("❌ Invalid Credentials...")
            print("You get 3 more chances to login\n")
            
            count = 3
            while(count > 0):
                # clear_screen()
                username = input('Enter Username : ')
                password = getpass.getpass('Enter Password : ')
                password = hash_password(password)
                # clear_screen()
                # for user in fp:
                #     user_list =  user.split(', ')
    
                if(user_list[4] == username and user_list[5].strip('\n') == password):
                        print("✅ Login Successfully...")
                        input("\nPress Enter to continue...")
                        clear_screen()
                        user_obj = User(user_list[0], user_list[1], user_list[2], user_list[3], user_list[4], user_list[5])
                        user_obj.userDashboard()
                else:
                        clear_screen()
                        print("❌ Invalid Credentials...")
                        count -= 1
                        print(f"Remaining chances are {count}")
            
            print("🚫 Too many failed attempts! Access denied.")
            input("\nPress Enter to continue...")
            return 

main()