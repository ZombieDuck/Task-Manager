# Notes: 
# 1. Use the following username and password to access the admin rights 
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the 
# program will look in your root directory for the text files.

#=====importing libraries===========
import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"

 # Create relevant txt files if they doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

if not os.path.exists("task_overview.txt"):
    with open("task_overview.txt", "w") as default_file_1:
        pass

if not os.path.exists("user_overview.txt"):
    with open("user_overview.txt", "w") as default_file_2:
        pass

 # If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Then get the current date.
curr_date = date.today()

'''This code reads usernames and password from the user.txt file to 
    allow a user to login.
'''
# Read in user_data
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")

# Convert to a dictionary
username_password = {}
for user in user_data:
    username, password = user.split(';')
    username_password[username] = password
        
#===== Functions =====
    
    
def login():
#====Login Section====

    logged_in = False
    while not logged_in:
        print("~~~~~~~~~~~~~~~~~~~~~~ Welcome to Task Manager! ~~~~~~~~~~~~~~~~~~~~~~")
        print("\033[1m\033[4mLogin\033[0m")
        curr_user = input("Username: ").strip()
        curr_pass = input("Password: ").strip()
        
        if curr_user not in username_password.keys():
            print("User does not exist")
            continue
        elif username_password[curr_user] != curr_pass:
            print("Wrong password")
            continue
        else:
            print("-"*70)
            print(f"Hello {curr_user}, Welcome Back!")
            logged_in = True

    return curr_user


def reg_user():
    """
    The `reg_user` function adds a new user to a user.txt file after checking for username availability
    and matching passwords.
    :return: The `reg_user` function is returning a dictionary `username_password` which contains the
    new username as key and the corresponding password as the value.
    """
   
    while True:
        continue_while = False
        '''Add a new user to the user.txt file'''
        # - Request input of a new username
        new_username = input("New Username: ")

        for user in user_data:
            username, password = user.split(';')
            if new_username == username:
                print("Username taken. Please try again.")
                continue_while = True
                break
        if continue_while == True:
            continue

        # - Request input of a new password
        new_password = input("New Password: ")

        # - Request input of password confirmation.
        confirm_password = input("Confirm Password: ")

        # - Check if the new password and confirmed password are the same.
        if new_password == confirm_password:
            # - If they are the same, add them to the user.txt file,
            print("New user added")
            print("="*80)
            username_password[new_username] = new_password
            
            with open("user.txt", "w") as out_file:
                user_data = []
                for k in username_password:
                    user_data.append(f"{k};{username_password[k]}")
                out_file.write("\n".join(user_data))
            
        # - Otherwise you present a relevant message.
        else:
            print("Passwords do no match")
            continue      
        break

    return username_password


def add_task():
    """
    The `add_task` function allows a user to input task details, validates the input, adds the task to a
    task list, and writes the updated task list to a file.
    :return: The function `add_task()` is returning the following variables:
    - `task_title`
    - `task_description`
    - `task_due_date`
    - `due_date_time`
    - `task_username`
    """
    task_list = read_tasks()
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
    
    ''' Add the data to the file task.txt and
        Include 'No' to indicate if the task is complete.'''
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": "No"
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
                "Yes" if t['completed'] == "Yes" else "No"
            ]
            task_list_to_write.append(";".join(str_attrs))
        task_file.write("\n".join(task_list_to_write))
    print("Task successfully added.")

    return task_title, task_description, task_due_date, due_date_time, task_username


def view_all():
    """
    The `view_all` function reads tasks from a file and prints them in a formatted manner to the
    console.
    """
    # '''Reads the task from task.txt file and prints to the console in the 
    #     format of Output 2 presented in the task pdf (i.e. includes spacing
    #     and labelling) 
    #     '''
    task_list = read_tasks()
    task_dict = {} 

    if not task_dict:
        print("Task list empty! Try adding a task. Returning to main menu...")
    
    for count, t in enumerate(task_list, start=1):
        task_dict[count] = t

        disp_str = ("-"*80)
        disp_str += f"\nTask number {count}\n"
        disp_str += ("="*80)
        disp_str += f"\nTask: \t\t {t['title']}\n"
        disp_str += f"Assigned to: \t {t['username']}\n"
        disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Task Description: \n {t['description']}\n"
        disp_str += f"Task Completed?: \n {t['completed']}\n"
        disp_str += ("-"*80)
        print(disp_str)


def view_mine(curr_user, selected_task):
    """
    The `view_mine` function reads tasks assigned to the current user, displays them with options to
    mark as complete or edit, and allows for editing task details like assignment username and due date.
    
    :param curr_user: The `curr_user` parameter in the `view_mine` function represents the current user
    who is viewing their assigned tasks. This parameter is used to filter and display only the tasks
    assigned to the current user in the task list. The function then allows the user to interact with
    their tasks, such as editing the due date or marking a task as completed.
    :param selected_task: The `selected_task` parameter in the `view_mine` function is used to keep
    track of the task that the user has selected to view or potentially edit. It is a dictionary
    containing information about the selected task.
    """ 
    # Starting a task dictionary to store each task with 
    # it's unique task number
    
    task_list = read_tasks()
    task_dict = {} 

    if not task_dict:
        print("Task list empty! Try adding a task. Returning to main menu...")
    
    for count, t in enumerate(task_list, start=1):
        if t['username'] == curr_user:
            task_dict[count] = t

            disp_str = ("-"*80)
            disp_str += f"\nTask number {count}\n"
            disp_str += ("="*80)
            disp_str += f"\nTask: \t\t {t['title']}\n"
            disp_str += f"Assigned to: \t {t['username']}\n"
            disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Task Description: \n {t['description']}\n"
            disp_str += f"Task Completed?: \n {t['completed']}\n"
            disp_str += ("-"*80)
            print(disp_str)
            
    while True:
        task_select = input("""Please type the number of the task you want to select 
or type \033[1m-1\033[0m to return to the main menu: """)
        print("-"*80)
        if task_select == "-1":
            if curr_user == "admin":
                admin_menu(curr_user, selected_task)
            else:
                disp_menu(curr_user, selected_task)
                
        # if task_select.isdigit():
        task_number = int(task_select)
        if task_number in task_dict:
            selected_task = task_dict[task_number]
            if selected_task['completed'] == "Yes":
                print("Task complete. This task cannot be edited.\n")
                if curr_user == "admin":
                    admin_menu(curr_user, selected_task)
                else:
                    disp_menu(curr_user, selected_task)
            else:
                vm_menu = input("""Please choose from the following options:
1. Mark the task as complete
2. Edit the task
""")
            print("-"*80)
            if vm_menu == "1":
                # Checks if the task is already complete
                if selected_task['completed'] == "Yes":
                    print("This task has been completed.")
                    break
                else:
                    # Marks the task as complete
                    selected_task['completed'] = "Yes"
                # Updates the completion status in the file
                update_task(task_list)
                print("Task successfully completed. Well Done! 👏")
                print("-"*80)
            elif vm_menu == "2":
                while True:
                    edit_menu = input("""What would you like to edit?: 
1. Change task assignment username
2. Change due date of task
'\033[3m'Remember, a task can only be edited if it has not been completed'\033[0m'
""")    
                    if edit_menu == "1":
                        # Checks to see if the task is already complete
                        if selected_task['completed'] == "Yes":
                            print("This task has been completed and cannot be edited.")
                            # Sends the user back to the main menu if it is
                            break
                        else: 
                            # Displays current task assignment username
                            print(f"The current username this task is assigned to is: {selected_task['username']}")
                            # Utilizes function to update the task's assigned username in the txt file
                            change_user(task_list, selected_task)
                            break
                    elif edit_menu == "2":
                        # Display current due date
                        print(f"The current due date for this task is: {selected_task['due_date'].strftime(DATETIME_STRING_FORMAT)}")
                        # Utilizes function to update the task's due date in the txt file
                        change_duedate(task_list, selected_task)
                        break
                    else:
                        print("Invalid option. Please try again.")
            else:
                print("Invalid option. Please try again.")
        else:
            print("Invalid option. Please try again.")


def read_tasks():
    """
    The function `read_tasks` reads task data from the tasks.txt file and returns a list of dictionaries containing
    task details.
    :return: The function `read_tasks()` reads task data from a file named "tasks.txt", parses the data,
    and returns a list of dictionaries where each dictionary represents a task. Each task dictionary
    contains the following keys: 'username', 'title', 'description', 'due_date', 'assigned_date', and
    'completed'.
    """
    # Opens tasks.txt, reads it, splits it by line
    task_list = []
    with open("tasks.txt", 'r') as task_file:
        task_data = task_file.read().split("\n")
        task_data = [t for t in task_data if t != ""] # Removes empty lines

    for t_str in task_data:
        curr_t = {}

        # Split by semicolon and manually add each component
        task_components = t_str.split(";") 
        curr_t['username'] = task_components[0]
        curr_t['title'] = task_components[1]
        curr_t['description'] = task_components[2]
        curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
        curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
        completed_status = "Yes" if task_components[5] == "Yes" else "No"
        curr_t['completed'] = completed_status
        task_list.append(curr_t)
    
    return task_list


def change_duedate(task_list, selected_task):
    """
    The function `change_duedate` allows the user to update the due date of a selected task in a task
    list stored in a file, ensuring the new date is in the correct format.
    
    :param task_list: The `task_list` parameter in the `change_duedate` function is a list of
    dictionaries where each dictionary represents a task. Each task dictionary contains keys such as
    'username', 'title', 'description', 'due_date', 'assigned_date', and 'completed' to store
    information about each user.
    :param selected_task: The `selected_task` parameter in the `change_duedate` function represents the
    task that the user has selected to update the due date for. It is a dictionary containing
    information about the task, such as the username, title, description, due date, assigned date, and
    completion status. 
    """
    # Prompt user for updated due date
    # Exception handling to make sure it's in the correct format
    while True:
        try:
            updated_duedate = input("What would you like to change the due date to (YYYY-MM-DD): ")
            upd_due_date_time = datetime.strptime(updated_duedate, DATETIME_STRING_FORMAT)
            break

        except ValueError:
            print("Invalid datetime format. Please use the format specified")
    
    # Update the selected task's due date
    selected_task['due_date'] = upd_due_date_time

    # Rewrite the entire task list to the file with updated due date
    with open("tasks.txt", "w") as file:
        for task in task_list:
            file.write(f"{task['username']};{task['title']};{task['description']};"
                       f"{task['due_date'].strftime(DATETIME_STRING_FORMAT)};"
                       f"{task['assigned_date'].strftime(DATETIME_STRING_FORMAT)};"
                       f"{task['completed']}\n")
    print("Task due date updated successfully.")
    print("="*80)


def change_user(task_list, selected_task):
    """
    The function `change_user` allows the user to update the assigned user for a selected task in a task
    list stored in a file.
    
    :param task_list: A list containing dictionaries, where each dictionary represents a task with keys
    like 'username', 'title', etc.
    :param selected_task: The `selected_task` parameter in the `change_user` function represents the
    task that the user has selected to change the assigned user for. This task is a dictionary
    containing information such as the username of the current assignee.
    :return: The function `change_user` returns nothing explicitly, as there is no `return` statement
    after the print statement.
    """

    # Prompt user for new username
    updated_task_user = input("Who would you like to assign this task to?: ")
    if updated_task_user not in username_password.keys():
        print("User does not exist")
        return
    
    # Update the selected task's username
    selected_task['username'] = updated_task_user

    # Rewrite the entire task list to the file with updated username
    with open("tasks.txt", "w") as file:
        for task in task_list:
            file.write(f"{task['username']};{task['title']};{task['description']};"
                       f"{task['due_date'].strftime(DATETIME_STRING_FORMAT)};"
                       f"{task['assigned_date'].strftime(DATETIME_STRING_FORMAT)};"
                       f"{task['completed']}\n")
    print("Task assignment username updated successfully.")
    print("="*80)


def update_task(task_list):
    """
    The function `update_task` updates tasks in the 'tasks.txt' file with the updated completion status.
    
    :param task_list: A list of dictionaries where each dictionary represents a task with keys like
    'username', 'title', 'description', etc.
    """
    with open("tasks.txt", "w") as file:
        for task in task_list:
            # Convert the completion status to "Yes" or "No"
            completion_status = "Yes" if task['completed'] == "Yes" else "No"

            # Write task details to the file
            file.write(f"{task['username']};{task['title']};{task['description']};"
                       f"{task['due_date'].strftime(DATETIME_STRING_FORMAT)};"
                       f"{task['assigned_date'].strftime(DATETIME_STRING_FORMAT)};"
                       f"{completion_status}\n")


def gen_reps():
    """
    The function `gen_reps` generates task and user overviews based on task completion status and due
    dates.
    :return: The function `gen_reps()` does not explicitly return any value. However, it does print
    messages if there are no incomplete tasks or no overdue tasks. Additionally, it writes the task
    overview information to a file named "task_overview.txt" and the user overview information to a file
    named "user_overview.txt".
    """
    completed_tasks = 0
    incomplete_tasks = 0
    overdue_tasks = 0
    incomp_pc = 0
    overdue_pc = 0

    task_list = read_tasks()
    num_tasks = len(task_list)
    
    # Adds up all the complete and incomplete tasks and stores them
    for task in task_list:
        if task['completed'] == "Yes":
            completed_tasks += 1
        else:
            incomplete_tasks += 1
    
    # Checks for and adds up any tasks deemed 'overdue'
    for task in task_list:
        if not task['completed'] == "Yes" and task['due_date'].strftime(DATETIME_STRING_FORMAT) < curr_date.strftime(DATETIME_STRING_FORMAT):
            overdue_tasks += 1

    # Calculate percentage of 'incomplete' tasks
    try:
        incomp_pc = (incomplete_tasks / num_tasks)*100
    except ZeroDivisionError:
        print("There are no incomplete tasks.")
    
    # Calculate the percentage of 'overdue' tasks
    try:
        overdue_pc = (overdue_tasks / num_tasks)*100
    except ZeroDivisionError:
        print("There are no overdue tasks.")
        return "0"

    with open("task_overview.txt", "w") as task_o:
    
        task_o.write(f"Task Overview:\n"
             f" - Total tasks generated: {num_tasks}\n"
             f" - Completed tasks: {completed_tasks}\n"
             f" - Incomplete tasks: {incomplete_tasks}\n"
             f" - Overdue tasks: {overdue_tasks}\n"
             f" - Percentage of incomplete tasks: {incomp_pc}%\n"
             f" - Percentage of overdue tasks: {overdue_pc}%\n")

    user_ov_str = print_user_info()

    with open("user_overview.txt", "w") as user_o:
            user_o.write(user_ov_str)


def print_user_info():
    """
    The function `print_user_info` generates a summary of user information and task statistics.
    :return: The function `print_user_info` returns a formatted string containing user overview
    information. This includes the total number of users registered, total tasks generated, and detailed
    information for each user such as total tasks assigned, percentage of total tasks assigned,
    percentage of completed tasks, percentage of incomplete tasks, and percentage of overdue tasks.
    """
    user_info_dict = user_overview() 
    task_list = read_tasks()
    num_tasks = len(task_list)

    usr_o_str = (f"User Overview:\n"
                f" - Total users registered: {len(user_info_dict)}\n"
                f" - Total tasks generated: {num_tasks}\n\n")

    usr_str = ""
    for username, user_data in user_info_dict.items():
        usr_str += f"For the user {username}:\n"
        usr_str += f" - Total tasks assigned: {user_data['total_tasks']}\n"
        usr_str += f" - Percentage of total tasks assigned: {(user_data['total_tasks'] / num_tasks) * 100}%\n"
        usr_str += f" - Percentage of completed tasks: {user_data['percentage_completed']}%\n"
        usr_str += f" - Percentage of incomplete tasks: {user_data['percentage_incomplete']}%\n"
        usr_str += f" - Percentage of overdue tasks: {user_data['percentage_overdue']}%\n\n"

    user_ov_str = usr_o_str + usr_str

    return user_ov_str


def user_overview():
    """
    The function `user_overview` generates user-specific task statistics based on task completion status
    and due dates.
    :return: The function `user_overview()` is returning a dictionary `user_info_dict` containing
    user-specific information such as total tasks, percentage completed, percentage incomplete, and
    percentage overdue for each user in the system.
    """

    task_list = read_tasks()
    tot_users = 0
    user_info_dict = {}  # Store user-specific information

    # Looping through each username
    for key in username_password:
        tot_users += 1

        usr_tsk = 0
        compl_usr_tsk = 0
        incomp_usr_tsk = 0
        overdue_usr_tsk = 0

        for task in task_list: # Looping through tasks in the task list
            if task['username'] == key: # Finding if each task 'username' matches the current looping 'key' username
                usr_tsk += 1 # Adds one task to the counter if it matches
                if task['completed'] == "Yes":
                    compl_usr_tsk += 1
                else:
                    incomp_usr_tsk += 1
                if task['completed'] == "No" and task['due_date'].strftime(DATETIME_STRING_FORMAT) < curr_date.strftime(DATETIME_STRING_FORMAT):
                    overdue_usr_tsk += 1

        # Check if usr_tsk is zero before performing division
        if usr_tsk != 0:
            pc_compl_usr_tsk = (compl_usr_tsk / usr_tsk) * 100
            pc_incomp_usr_tsk = (incomp_usr_tsk / usr_tsk) * 100
            pc_ovrdue_usr_tsk = (overdue_usr_tsk / usr_tsk) * 100
        else:
            pc_compl_usr_tsk = 0
            pc_incomp_usr_tsk = 0
            pc_ovrdue_usr_tsk = 0

         # Store user-specific information in a dictionary for the current user
        user_info_dict[key] = {
            'total_tasks': usr_tsk,
            'percentage_completed': pc_compl_usr_tsk,
            'percentage_incomplete': pc_incomp_usr_tsk,
            'percentage_overdue': pc_ovrdue_usr_tsk}
        
    print("\nReports have been generated. "
            "\nPlease select '\033[1mDisplay Statistics\033[0m' to view them in the console.")
    print("="*80)

    return user_info_dict


def admin_menu(curr_user, selected_task):
    """
    The function `admin_menu` presents a menu of options to an admin user, allowing them to perform
    tasks such as registering a user, adding a task, viewing tasks, generating reports, displaying
    statistics, and exiting the program.
    
    :param curr_user: The `curr_user` parameter in the `admin_menu` function represents the current user
    who is accessing the admin menu. In this case, it is used to determine if the current user is an
    admin or not, and based on that, different options are presented in the menu. 
    :param selected_task: The `selected_task` parameter in the `admin_menu` function is used to
    keep track of the task that the current user has selected. It is used to pass the selected
    task information to other functions within the menu options, such as the `view_mine` function.
    """
    while True:
        print()
        # presenting the menu to the user and 
        # making sure that the user input is converted to lower case.
        if curr_user == "admin":
            menu = input('''Select one of the following Options below:
        r - Registering a user
        a - Adding a task
        va - View all tasks
        vm - View my task
        gr - generate reports
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
                view_mine(curr_user, selected_task)
            elif menu == 'ds':
                with open("task_overview.txt", "r") as task_file:
                    task_overview = task_file.read()
                    print("="*80)
                    print(task_overview)
                with open("user_overview.txt", "r") as user_file:
                    user_ov = user_file.read()
                    print("="*80)
                    print(user_ov)
                    print("="*80)
                    continue
            elif menu == "gr":
                gen_reps()
            elif menu == 'e':
                print(f'Good-bye {curr_user}, see you again soon! 😊')
                exit()

            else:
                print("You have made a wrong choice, Please Try again")


def disp_menu(curr_user, selected_task):
    """
    The function `disp_menu` presents a menu to the user, takes user input, and directs the program flow
    based on the selected option.
    
    :param curr_user: The `curr_user` parameter in the `disp_menu` function represents the current user
    who is interacting with the menu. This parameter is used to personalize the user experience by
    displaying messages or performing actions specific to the current user, such as displaying their
    username or tasks.
    :param selected_task: The `selected_task` parameter is used as an argument in the
    `view_mine` function. It is used to identify a specific task that the current user wants to
    view. This parameter could be an identifier or index of the task selected by the user.
    """
    print()
    # presenting the menu to the user and 
    # making sure that the user input is converted to lower case.
    menu = input('''Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my task
e - Exit
: ''').lower()

    if menu == 'r':
        reg_user()
    elif menu == 'a':
        add_task()
    elif menu == 'va':
        view_all()
    elif menu == 'vm':
        view_mine(curr_user,selected_task)
    elif menu == 'e':
        print(f'Good-bye {curr_user}, see you again soon! 😊')
        exit()
    else:
        print("You have made a wrong choice, Please Try again")


def main():
    """
    The main function in this Python code handles user login functionality and directs users to
    different menus based on their role.
    """
    while True:
        user_role = login()
        
        # Login check and then display menu according to relevant user
        if user_role == "admin":
            admin_menu(user_role, None)
        else:
            disp_menu(user_role, None)

if __name__ == "__main__":
    main()
