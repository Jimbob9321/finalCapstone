# Notes: 
# 1. Use the following username and password to access the admin rights 
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the 
# program will look in your root directory for the text files.

#=====importing libraries===========
import os
from datetime import datetime, date
import math

DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Functions ... 

def reg_user():

    '''Add a new user to the user.txt file'''
    # - Request input of a new username
    i = 1
    while i < 2:

        new_username = input("New Username: ")

        # Compares new username to usernames stored in file, iterates back over in order for user to re-enter new username
        with open("user.txt", "r") as file:
            lines = file.readlines()
            
            for line in lines:
                string = line.strip()
                string = string.split(";")
                string = string[0]

                if new_username == string:
                    print(string)
                    print("There is already a user with that username, please choose something else")
                    i = 1
                    break
                else:
                    i +=1 
                
    # - Request input of a new password
    new_password = input("New Password: ")

    # - Request input of password confirmation.
    confirm_password = input("Confirm Password: ")

    # - Check if the new password and confirmed password are the same.
    if new_password == confirm_password:
        # - If they are the same, add them to the user.txt file,
        username_password[new_username] = new_password
        
        print("New user added")
        with open("user.txt", "w") as out_file:
            user_data = []
            for k in username_password:
                user_data.append(f"{k};{username_password[k]}")
            out_file.write("\n".join(user_data))

    # - Otherwise you present a relevant message.
    else:
        print("Passwords do no match")

        
def add_task():
    '''Allow a user to add a new task to task.txt file
            Prompt a user for the following: 
             - A username of the person whom the task is assigned to,
             - A title of a task,
             - A description of the task and 
             - the due date of the task.'''
    task_username = input("Name of person assigned to task: ")
    if task_username not in username_password.keys():
        print("User does not exist. Please enter a valid username")
    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")
    while True:
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            break

        except ValueError:
            print("Invalid datetime format. Please use the format specified")

    # Then get the current date.
    curr_date = date.today()
    ''' Add the data to the file task.txt and
        Include 'No' to indicate if the task is complete.'''
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": False
    }

    task_list.append(new_task)
    with open("tasks.txt", "w") as task_file:
        task_list_to_write = []
        for t in task_list:
            str_attrs = [
                t['username'],
                t['title'],
                t['description'],
                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if t['completed'] else "No"
            ]
            task_list_to_write.append(";".join(str_attrs))
        task_file.write("\n".join(task_list_to_write))
    print("Task successfully added.")


def view_all():
    '''Reads the task from task.txt file and prints to the console in the 
        format of Output 2 presented in the task pdf (i.e. includes spacing
        and labelling) 
    '''

    for t in task_list:
        disp_str = f"Task: \t\t {t['title']}\n"
        disp_str += f"Assigned to: \t {t['username']}\n"
        disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Task Description: \n {t['description']}\n"
        print(disp_str)


def view_mine():

    '''Reads the task from task.txt file and prints to the console in the 
        format of Output 2 presented in the task pdf (i.e. includes spacing
        and labelling)
    '''

    # Function to rewrite new task list to file
    def write_to_file(message):
        with open("tasks.txt", "w") as task_file:
            new_task_list = []
            for t in task_list:
                str_attrs = [
                    t['username'],
                    t['title'],
                    t['description'],
                    t['due_date'].strftime(DATETIME_STRING_FORMAT),
                    t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                    "Yes" if t['completed'] else "No",
                    "\n"                                   
                ]
                new_task_list.append(";".join(str_attrs))
            task_file.write("".join(new_task_list))
        str(print(message))
    
    # Find specific task based on number, option to edit/confirm as completed
    while True:

        while True:
            try:

                task_number = int(input("Please select a task number you wish to view (input -1 to exit): "))
                break
            except ValueError:
                print("Please enter a number")

        num = 1
        count = 0

        if task_number != -1:

            for t in task_list:
                if t['username'] == curr_user and task_number == num:
                    decor = "______________________________________________________________"
                    print(decor)
                    task_num = f"\nTask {num}\n"
                    disp_str = f"Task: \t\t {t['title']}\n"
                    disp_str += f"Assigned to: \t {t['username']}\n"
                    disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
                    disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
                    disp_str += f"Task Description: \n {t['description']}\n"
                    disp_str += f"{decor}\n"
                    if t['completed'] == True:
                        disp_str += "Task completed:  Yes\n"
                        print(task_num + disp_str + f"{decor}")
                        break
                    else:
                        disp_str += "Task completed:  No\n"

                        print(task_num + disp_str + f"{decor}")
                        
                    
                        options = input('''y - Mark task as complete
edit - edit task
c - choose another task
: ''').lower()   
                        # If 'y' is selected, runs to rewrite task as completed 
                        if options == "y":
                            t["completed"] = True
                            new_t = t
                            task_list[count] = new_t
                            write_to_file("Task Marked as complete")
                            break

                        # Allows user to enter edits and checks certain inputs, while looping to ensure ease of use for user
                        elif options == "edit":
                            options_2 = str(input('''u - change username
d - change due date 
: ''')).lower()             # Requests new username input, rewrites to file
                            while True:
                                if options_2 == "u":
                                    t["username"] = input("New Username: ")
                                    new_username = t
                                    task_list[count] = new_username
                                    write_to_file("Username changed")
                                    break
                                
                                # Change date, checks for correct format and rewrites to file
                                elif options_2 == "d":
                                    while True:
                                        try:
                                            new_due_date_inp = input("New due date of task (YYYY-MM-DD): ")
                                            t["due_date"] = datetime.strptime(new_due_date_inp, DATETIME_STRING_FORMAT)
                                            new_due_date = t
                                            task_list[count] = new_due_date
                                            write_to_file("Date changed")
                                            break

                                        except ValueError:
                                            print("Invalid datetime format. Please use the format specified")
                                    break
                                
                                else:
                                    print("Please enter a valid option")
                            break
                        else:
                            break
                
                elif t['username'] == curr_user and task_number != num:
                    num += 1
                
                count += 1 

        else:
            break

def generate_reports():

    tasks = len(task_list)
    complete_tasks = 0
    incomplete_tasks = 0
    incomplete_overdue = 0

    # Iterates through task list to check conditions and write to file for a task overview report
    for task in task_list:
        if task["completed"] == False and task["due_date"] < datetime.today():
            incomplete_overdue += 1
            incomplete_tasks += 1 
        elif task["completed"] == True:
            complete_tasks += 1
        elif task["completed"] == False:
            incomplete_tasks +=1

    incomplete_percentage = math.floor(incomplete_tasks/tasks * 100)
    overdue_percentage = math.floor(incomplete_overdue/tasks * 100)

    with open("task_overview.txt","w") as file:
                 
        file.write(f'''Task submission report
    
Total number of tracked tasks: {tasks}
Completed tasks:               {complete_tasks}
incomplete tasks:              {incomplete_tasks}
Overdue tasks:                 {incomplete_overdue}
% incomplete:                  {incomplete_percentage}%
% overdue:                     {overdue_percentage}%''')
        
    # reads users from users.txt, pushes usernames only into a list of users to iterate through easier 
    no_users = len(username_password.keys())
    user_list = []
    with open("user.txt", 'r') as user_file:
        users = user_file.readlines()
        for line in users:
            lines = line.strip()
            lines = lines.replace(";", " ")
            user = lines.split()
            user = user[0]
            user_list.append(user)
    
    num_of_tasks = 0
    completed_tasks = 0
    to_complete = 0
    overdue = 0

    # Iterates through both tasks.txt and user.txt, comparing users and printing message to new text file giving user overview
    with open("user_overview.txt", "w") as file:
        file.write(f'''Total users:                {no_users}\n\n''')
        for user in user_list:
            for t in task_list:
                if user == t["username"]:
                    num_of_tasks += 1
                
                if user == t["username"] and t["completed"] == True:
                    completed_tasks +=1

                if user == t["username"] and t["completed"] == False:
                    to_complete += 1
                
                if user == t["username"] and t["completed"] == False and t["due_date"] < datetime.today():
                    overdue += 1

            file.write(
f'''User: {user} has {num_of_tasks} tasks remaining 

This accounts for {math.floor(num_of_tasks/tasks*100)}% of total tasks.
Percentage completed:           {math.floor(completed_tasks/num_of_tasks*100)}%
Percentage left to complete:    {math.floor(to_complete/num_of_tasks*100)}%
Percentage overdue:             {math.floor(overdue/num_of_tasks*100)}%
\n''')
                    
            num_of_tasks = 0
            completed_tasks = 0
            to_complete = 0
            overdue = 0

# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]


task_list = []
for t_str in task_data:
    curr_t = {}

    # Split by semicolon and manually add each component
    task_components = t_str.split(";")
    curr_t['username'] = task_components[0]
    curr_t['title'] = task_components[1]
    curr_t['description'] = task_components[2]
    curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
    curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
    curr_t['completed'] = True if task_components[5] == "Yes" else False

    task_list.append(curr_t)


#====Login Section====
'''This code reads usernames and password from the user.txt file to 
    allow a user to login.
'''
# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Read in user_data
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")

#Convert to a dictionary
username_password = {}
for user in user_data:
    username, password = user.split(';')
    username_password[username] = password

logged_in = False
while not logged_in:

    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password.keys():
        print("User does not exist")
        continue
    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
        continue
    else:
        print("Login Successful!")
        logged_in = True


while True:
    # presenting the menu to the user and 
    # making sure that the user input is converted to lower case.
    if curr_user == "admin":
        menu = menu = input('''Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my task
gr - generate reports
ds - Display statistics
e - Exit
: ''').lower()
        
        
    else:
        menu = input('''Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my task
ds - Display statistics
e - Exit
: ''').lower()

    if menu == 'r':
        reg_user()

    elif menu == 'a':
        add_task()
            
    elif menu == 'va':
        view_all()

    elif menu == 'vm':
        view_mine()

    elif menu == 'gr':
        generate_reports()  
                     
    elif menu == 'ds' and curr_user == 'admin': 
        '''If the user is an admin they can display statistics about number of users
            and tasks.'''
        num_users = len(username_password.keys())
        num_tasks = len(task_list)

        print("-----------------------------------")
        print(f"Number of users: \t\t {num_users}")
        print(f"Number of tasks: \t\t {num_tasks}")
        print("-----------------------------------")    

    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    else:
        print("You have made a wrong choice, Please Try again")