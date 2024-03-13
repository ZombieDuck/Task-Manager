# Capstone Project Task 1 Readme

## Summary
This project involves extending the functionality of the existing codebase in `task_manager.py` for the Capstone project. The goal is to refactor the code by implementing additional functions for tasks such as user registration, task addition, viewing all tasks, and viewing tasks assigned to a specific user. Additionally, modifications will be made to prevent duplicate usernames, allow task completion marking, task editing, and report generation.

## Steps to Follow

1. **Refactoring Code Using Abstraction**
   - Utilize abstraction to create and implement the following functions:
     - `reg_user`: Registers a new user without duplicating existing usernames.
     - `add_task`: Adds a new task.
     - `view_all`: Displays all tasks listed in `tasks.txt`.
     - `view_mine`: Displays tasks assigned to the current user.

2. **Functionality Enhancements**
   - Update `reg_user` function to prevent duplicate usernames.
   - Add functionality to `view_mine`:
     - Display tasks in a readable format with corresponding identification numbers.
     - Allow users to select a specific task for marking completion or editing.
       - If marking a task as complete, update completion status.
       - If editing a task, allow changes to username or due date if the task is not completed yet.

3. **Report Generation Option**
   - Integrate an option to generate reports in the main menu.
   - The admin menu should include:
     - Generate Reports
   - Upon selection, generate two text files:
     - `task_overview.txt`
       - Total number of tasks tracked.
       - Total completed tasks.
       - Total uncompleted tasks.
       - Total overdue tasks.
       - Percentage of incomplete tasks.
       - Percentage of overdue tasks.
     - `user_overview.txt`
       - Total number of registered users.
       - Total tasks tracked.
       - For each user:
         - Total tasks assigned.
         - Percentage of tasks assigned.
         - Percentage of completed tasks.
         - Percentage of tasks to be completed.
         - Percentage of overdue tasks.

4. **Displaying Statistics**
   - Modify the menu option to display statistics:
     - Read from `tasks.txt` and `users.txt`.
     - Display data in a user-friendly manner.
   - Generate text files if they don't exist before displaying statistics.

## Conclusion
This project aims to enhance the functionality of `task_manager.py` by implementing additional features and improving readability through abstraction. Additionally, it introduces report generation capabilities to provide valuable insights into task and user statistics.
