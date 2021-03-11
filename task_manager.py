# Program is a task manager that helps small business to manage tasks to assign new tasks to each member of the team, edit tasks,
# display statistics and generate reports for users and tasks
# Program works with 2 text files user.txt and tasks.txt



def user_reg():
    # Makes sure admin doesn't duplicate usernames when adding a new user to user.txt. If the admin tries to add a username
    # that already exists in user.txt, provides error message and asking to enter new username

    register_user = False
    
    while register_user == False:
        
        with open("user.txt", "r") as f:                     # Reads the file and compares existing usernames with the username that needs to be registered
            
            for line in f:                
                a,b = line.split(", ")                       # Splits the line in user.txt to check only first word in the line
                new_user_username = input("\nEnter new username: ")
                
                if a == new_user_username:
                    print("\nUsername already exists, add user with a different username.")   
                
                else:
                    register_user = True
                    

        if register_user == True:                            # If new username is unique, process to registered new user is followed
            f = open("user.txt", "a+")
                            
            new_user_password = input("Enter new password: ")
            confirm_password = input("Confirm the password: ")

            if new_user_password == confirm_password:        # New users are added only if new password and confirm password is identical
                f.write("\n" + new_user_username + ", " + new_user_password)
                print("\nNew user has been registered.")
                
            else:
                print("Value entered to confirm the password does not match the value of the password")
                
            f.close() 

                    

def add_task():
    # Adding new task to existing list of tasks in tasks.txt
    
    from datetime import datetime
    
    file = open("tasks.txt", "a+")                          # Asks user for input to populate the task data
    
    user_resp = input("\nEnter the username of the person the task is assigned to: ")   
    task_title = input("Enter the title of the task: ")    
    task_descrip = input("Enter description of the task: ")    
    task_due_date = input("Enter due date of the task: ")
    
    
    now = datetime.now()                                     # datetime function is used to set starting date of a new task as a current date
    now = now.strftime("%d %B %Y")

    
    file.write("\n" + user_resp + ", " + task_title + ", " + task_descrip + ", " + now + ", " + task_due_date + ", No")
    
    print("\nNew task has been assigned to the user.")
    
    file.close()


def view_all():
    # Accessing tasks.txt to extract information about all tasks in easy to read format
    
    with open("tasks.txt", "r+") as f:

        for line in f:
            a,b,c,d,e,f = line.split(", ")                   # lines in tasks.txt file are split to access required information

            print("")                                        # Prints info about all tasks in easy to read format
            print("User responsible          - " + a)
            print("Title of the task         - " + b)
            print("Description of the task   - " + c)
            print("Assignment date           - " + d)
            print("Due date                  - " + e)
            print("Has been completed        - " + f)

    
def view_mine():
    # Displays only tasks assigned to the user that is currently logged in
    
    line_num = 0
    
    with open("tasks.txt", "r") as f:

        for line in f.readlines():
            
            line_num +=1
            a,b,c,d,e,f = line.split(", ")                    # splits lines to access required information and displays in appropriate format                       
                  
            if a == username:                                 # only the information related to current user is displayed
                
                print("")
                print("Task {}".format(line_num))
                print("Title of the task         - " + b)
                print("Description of the task   - " + c)
                print("Assignment date           - " + d)
                print("Due date                  - " + e)
                print("Has been completed        - " + f)


    # Allows user to access and edit tasks assign to them or return to the main menu

    with open("tasks.txt", "r+") as f:
        
        data = f.readlines()
        choice = int(input("\nPlease select the task by entering the task number or enter '-1' to return to the main menu: "))

        # Different menues displayed for admin and users
        
        if choice == -1 and username == "admin":
            access_granted = input("\nPlease select one of the following options: \nr - register user \na - add task \nva - view all tasks \nvm - view my tasks \ngr - generate reports \ns - display statistics \ne - exit \n")

        elif choice == -1 and username != "admin":
            access_granted = input("\nPlease select one of the following options: \na - add task \nva - view all tasks \nvm - view my tasks \ne - exit\n")

            if access_granted == "a":
                add_task()
                
            if access_granted == "va":
                view_all()
                
            if access_granted == "vm":
                view_mine()
                
            if access_granted == "r":
                user_reg()
                
            if access_granted == "gr":
                generate_task_overview()
                generate_user_overview()
                
            if access_granted == "s":
                generate_statistics()
                
            if access_granted == "e":
                print("\nThank you for using Task Manager. Goodbye.")



        new_data = []
        
        for i,e in enumerate(data, start=1):                 # Enumerates the data to allow user to select the task to edit or mark as complete  

            if i == choice:
                
                complete_edit = input("\nPlease choose to mark the task as complete or edit the task (Reply mark or edit): ")
               
                if complete_edit == "mark":                  # Changes value of uncompleted task to "Yes" to mark as complete by spliting the line and 
                                                             # changing value of 'No' to 'Yes'
                    e = e.split(",")
                    e[5] = " Yes"
                    x = ",".join(e)                          # Joins list back with updated value
                    new_data.append(x.strip())

                elif complete_edit == "edit":                # Uses same logic as with 'Mark as complete code'
                    
                    print("\n***Only tasks that has not yet been completed can be edited.***")
                    
                    e = e.split(", ")
                    e[0] = input("\nEdit the username of the person to whom the task is assigned: ")
                    e[4] = input("Edit the due date of the task: ")
                    x = ", ".join(e)
                    new_data.append(x.strip())
               
            else:
                
                new_data.append(e.strip())   


    with open("tasks.txt", "w") as f:                         # Writes updated data into the tasks.txt
        
        for i in new_data:
            
            f.write(i + "\n")       
        



def generate_task_overview():
    # Generates report into task_overview.txt file based on info from tasks file
    
    from datetime import datetime

    now = datetime.now()                                     # Datetime function is used to identify overdue tasks
    now = now.strftime("%d %B %Y")

    file = open("task_overview.txt", "w")

    with open("tasks.txt", "r+") as f:                       # Loops through each line in tasks.txt, creates lists to generate report

        tasks, completed_tasks, uncompleted_tasks, overdue_tasks = [], [], [], []

        for line in f:

            line = line.strip()
            line = line.split(", ")
            
            task = line[1]
            completed = line[5]                              
            overdue = line[4]

            tasks.append(task)
            
            if completed == "Yes":                          # Identifies completed tasks
                completed_tasks.append(completed)
            else:
                uncompleted_tasks.append(completed)         # identifies uncompleted tasks
                
            if line[4] < now and line[5] == "No":
                overdue_tasks.append(overdue)


            
    # Writes information into the task_overview file to generate report
    
    file.write("The total number of tasks: {}".format(len(list(tasks))))
    file.write("\nThe total number of completed tasks: {}".format(len(list(completed_tasks))))
    file.write("\nThe total number of uncompleted tasks: {}".format(len(list(uncompleted_tasks))))
    file.write("\nThe total number of tasks that haven’t been completed and that are overdue: {}".format(len(list(overdue_tasks))))
    file.write("\nThe percentage of tasks that are incomplete: {}%".format(round((len(uncompleted_tasks)/len(tasks))*100)))
    file.write("\nThe percentage of tasks that are overdue: {}%".format(round((len(overdue_tasks)/len(tasks))*100)))
            
    file.close()


def generate_user_overview():
    # Generates report into user_overview.txt file based on info from tasks and user file
    
    from datetime import datetime

    now = datetime.now()                                     # Datetime function is used to identify overdue tasks
    now = now.strftime("%d %B %Y")
    
    with open("user.txt", "r") as f:                         # Reads user file to count users
        users = f.readlines()

    
    with open("tasks.txt", "r") as f:                        # Reads tasks file to count tasks
         data = f.readlines()
    
    total_task = len(data)

    

    f = open("user_overview.txt", "w")                       # Writes amount of users and tasks into user report
    
    f.write("\nThe total number of users: {}".format(len(users)))
    f.write("\nThe total number of tasks: {}".format(len(data)))

    
    for user in users:                                       # Creates nested loop to extract information for each user separatly. Creates lists
                                                             # for different requirements of the project.
        user, _ = user.split(", ")
        user_total_completed = 0
        user_total_uncompleted = 0
        overdue = 0
        
        for task in data:
            
            task = task.strip()
            
            if task.startswith(user) and task.endswith("Yes"):# Uses startswith and ednswith functions to extract required data from the tasks
                
                user_total_completed += 1
                
            elif task.startswith(user) and task.endswith("No"):
                
                user_total_uncompleted += 1
                task_s = task.split(", ")
                
                if task_s[4] < now:
                    overdue +=1
                    
        
       
        total = user_total_completed + user_total_uncompleted # Counts total amount of tasks assigned to the user
        
        
        if user_total_uncompleted == 0:                       # Conditions to avoid calculations with zero value as python will give error if divided by zero
            avg_unc = 0                                       # Some users may not have tasks assigned or not have completed tasks, therefore answer '0'
        else:                                                 # will be displayed in the output.
            avg_unc = (user_total_uncompleted/total)*100
            
        if user_total_completed == 0:
            avg_com = 0
        else:
            avg_com = (user_total_completed/total)*100

        if total == 0:
            total_avg = 0
        else:
            total_avg = (total/total_task)* 100
            
        if overdue == 0:
            over_avg = 0
        else:
            over_avg = ((overdue/total)*100)


        f.write("\n")                                          # Compilation of the report with information for each user displayed separately
        f.write("\nUser: {}".format(user))
        f.write("\nTotal number of tasks: {}".format(total))
        f.write("\nPercentage of the total tasks: {}%".format(round(total_avg)))
        f.write("\nPercentage of the tasks assigned to that user have been completed: {}%".format(round(avg_com)))
        f.write("\nPercentage of the tasks assigned to that user must still be completed: {}%".format(round(avg_unc)))
        f.write("\nPercentage of the tasks assigned to that user have not yet been completed and are overdue {}%".format(round(over_avg)))
        
    f.close() 


def generate_statistics():
    # Displays statistics from user_overview.txt and task_overview.txt. If files do not exist, functions generate new files with reports.

    generate_task_overview()
    generate_user_overview()
    
    print("\nOVERVIEW OF TASKS\n")                              # Prints overview of the tasks
    f = open("task_overview.txt", "r")
    print(f.read())

    print(" ")
    
    print("\nOVERVIEW OF USERS\n")                              # Prints overview of the users
    f = open("user_overview.txt", "r")
    print(f.read())

    
    

print("\nLogin")                                                # Login process using username and password
    
username = ""
password = ""
access_permitted = False


while access_permitted == False:                                # While loop to execute login process until correct credentials are entered


    username = input("\nEnter a valid username: ")
    password = input("Enter a valid password: ")
    login_details = username + ", " + password


    with open("user.txt","r") as f:                             # Program loops though each line of user.txt to verify credentials
        
       for line in f:

           line = line.strip()

        
           if line == login_details and username == "admin":     # For admin user additional functions are added 
               access_permitted = True

               if access_permitted == True:
                   access_granted = input("\nPlease select one of the following options: \nr - register user \na - add task \nva - view all tasks \nvm - view my tasks \ngr - generate reports \ns - display statistics \ne - exit\n")
                   

           elif line == login_details and username != "admin":   # For non-admin users function to register new user, generate reports and statistics are removed
               access_permitted = True

               if access_permitted == True:
                   access_granted = input("\nPlease select one of the following options: \na - add task \nva - view all tasks \nvm - view my tasks \ne - exit\n")


    if access_permitted == False:
        print("\nUsername or password is incorrect")
     


if access_granted == "r":                                         # To register new user program uses user_reg function
    user_reg()


if access_granted == "a":                                         # Adding new tasks to tasks.txt using add_task function 
    add_task()


if access_granted == "va":                                        # Displaying all tasks from tasks.txt using view_all function
    view_all()    


if access_granted == "vm":                                        # Displaying all tasks from tasks.txt assigned to the user that's  
    view_mine()                                                   # currently logged in using view_mine function


if access_granted == "gr":                                        # Generates report using task_overview.txt and user_overview.txt
    generate_task_overview()
    generate_user_overview()

                
if access_granted == "s":                                         # Shows statistics of all tasks and users in easy to read format
    generate_statistics()



if access_granted == "e":                                         # Exits Task Manager
    print("\nThank you for using Task Manager. Goodbye.")







# ******References*****

# Python DateTime, TimeDelta, Strftime(Format) with Examples. Retrieved 25 January 2021, from
# https://www.guru99.com/date-time-and-datetime-classes-in-python.html

# Checking a username and password from a text file. Retrieved 26 January 2021, from
# https://stackoverflow.com/questions/52337934/checking-a-username-and-password-from-a-text-file/52337976

# Python – Ways to remove duplicates from list. 23 June 2020. Retrieved 27 January 2021, from
# https://www.geeksforgeeks.org/python-ways-to-remove-duplicates-from-list/

# How to extract specific portions of a text file using Python. 30 June 2020. Retrieved 1 February 2021, from
# https://www.computerhope.com/issues/ch001721.htm
