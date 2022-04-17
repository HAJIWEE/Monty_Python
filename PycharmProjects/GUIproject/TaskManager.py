import datetime
from StorageManager import *
from ToDo import *


def validate_date(date):
    try:
        datetime.datetime.strptime(date, '%d%b%y')
    except ValueError:
        raise ValueError('Incorrect Date format, input: DDMMMYY eg. 02May22')


class TaskManager:
    menu = []
    sm = StorageManager('Monty_list.csv')  # call storageManager class

    def __init__(self):
        TaskManager.menu = TaskManager.sm.menu  # get tasks from file

    def get_help(self):
        return '''help:
Add task without deadline ----------------------> add [task]
Add task at specific index ----> add [task] at index [index]
Add task with deadline ------> deadline [task] by [deadline]
Set deadline for task ----> set[index or task] by [deadline]
Remove task ------------------------> remove [index or task]
Remove all tasks -------------------------------> remove all
Mark task as completed ---------------> done [index or task]
Mark all tasks completed -------------------------> done all
Mark task as uncompleted ----------> pending [index or task]
Mark all tasks as uncompleted -----------------> pending all
**Case insensitive
'''

    def execute_command(self, inp):

        self.user_input = inp
        if inp[0] == 'help':
            return self.get_help()
        elif len(inp[1:]) == 0:
            raise Exception('Empty command')  # Checking if there is input after the add command
        elif inp[0] == "add":
            return self.todo()
        elif inp[0] == 'done':
            return self.completed()
        elif inp[0] == 'remove':
            return self.remove()
        elif inp[0] == 'pending':
            return self.pend()
        elif inp[0] == 'deadline' or inp[0] == 'set':
            return self.deadline()
        elif inp[0] == 'progress':
            return self.progress()
        else:
            raise Exception('Command not recognized')

    def todo(self):

        check = ' '.join(self.user_input[-1])
        d_check = ' '.join(self.user_input[-3:-1])

        # Adding task to specific index
        if check.isdigit() and d_check == 'at index':
            status = ToDo(self.user_input[1:-3], len(TaskManager.menu) + 1, False)
            TaskManager.menu.insert(int(check) - 1, status)
            for i, b in enumerate(TaskManager.menu):
                b.chg_idx(i + 1)
            out = 'Added {' + ' '.join(self.user_input[1:-3]) + '} as a task to do.'

        # Just adding to bottom of list
        else:
            status = ToDo(self.user_input[1:], len(TaskManager.menu) + 1, False)
            TaskManager.menu.append(status)
            out = 'Added {' + ' '.join(self.user_input[1:]) + '} as a task to do.'

        return out

    def completed(self):

        check = ' '.join(self.user_input[1:])

        # Mark completed by index
        if check.isdigit():

            out = 'SORRY, I could not perform that command. \nProblem: No item at index ' + self.user_input[1]

            # Check if index exists
            if int(check) <= len(TaskManager.menu):
                TaskManager.menu[int(check) - 1].completed()
                out = 'Congrats on completing {' + ' '.join(TaskManager.menu[int(check) - 1].description) + '} :)'

        # Check if command is to mark all as done
        elif check == 'all':
            for b in TaskManager.menu:
                b.completed()
            return 'all done'

            # Mark completed by description
        else:

            out = "SORRY, I could not perform that command. \nProblem: " + check + ' is not an item in the menu'

            # Checking objects in menu if description matches user input
            for b in TaskManager.menu:
                if check == ' '.join(b.description):
                    b.completed()
                    out = 'Congrats on completing {' + check + '} :)'

        return out

    def remove(self):
        check = ' '.join(self.user_input[1:])

        # remove by index
        if check.isdigit():

            out = 'SORRY, I could not perform that command. \nProblem: No item at index ' + check

            # Check if index exists
            if int(self.user_input[1]) <= len(TaskManager.menu):
                del TaskManager.menu[int(self.user_input[1]) - 1]
                for i, b in enumerate(TaskManager.menu):
                    b.chg_idx(i + 1)
                out = 'removed {' + check + '}'

        # Check if command is to remove all
        elif check == 'all':
            TaskManager.menu.clear()
            return 'Removed all'

        # remove by description
        else:

            out = "SORRY, I could not perform that command. \nProblem: {" + check + '} is not an item in the menu'

            # Checking objects in menu if description matches user input
            for i, b in enumerate(TaskManager.menu):
                if check == ' '.join(b.description):
                    del TaskManager.menu[i]
                    for i, b in enumerate(TaskManager.menu):
                        b.chg_idx(i + 1)
                    out = 'removed {' + check + '}'

        return out

    def pend(self):
        check = ' '.join(self.user_input[1:])

        # mark pending by index
        if check.isdigit():

            out = 'SORRY, I could not perform that command. \nProblem: No item at index ' + str(self.user_input[1])

            if int(check) <= len(TaskManager.menu):
                TaskManager.menu[int(check) - 1].undone()
                out = 'Marked {' + ' '.join(TaskManager.menu[int(check) - 1].description) + '} as pending'

        # Mark pending for all
        elif check == 'all':
            for b in TaskManager.menu:
                b.undone()
            return 'all undone'

        else:

            out = "SORRY, I could not perform that command. \nProblem: {" + check + '} is not an item in the menu'

            # Check if any object description matches user input
            for b in TaskManager.menu:
                if check == ' '.join(b.description):
                    b.undone()
                    out = 'Marked {' + check + '} as pending'

        return out

    # create new deadline tasks and set deadlines for to do tasks
    def deadline(self):
        out = 'wrong format'

        # checking if command is in the right format
        if 'by' in self.user_input:
            i = self.user_input.index('by')  # finding where the date starts
            check = ' '.join(self.user_input[1:i])
            date = ' '.join(self.user_input[i + 1:])

            # Checking if date entered is of the right format.
            validate_date(date)

            # Checking if is a new deadline object
            if self.user_input[0] == 'deadline':
                TaskManager.menu.append(
                    Deadline(self.user_input[1:i], len(TaskManager.menu) + 1, self.user_input[i + 1:], False))
                out = 'Added {' + ' '.join(self.user_input[1:i]) + '} to be done by ' + str(date)

            # check if trying to set deadline for existing todo task
            elif self.user_input[0] == 'set':

                # set by index
                if check.isdigit():
                    out = 'SORRY, I could not perform that command. Problem: No item at index ' + str(
                        self.user_input[1])

                    # check if index exists
                    if int(check) <= len(TaskManager.menu):
                        change = [TaskManager.menu[int(check) - 1].description,
                                  TaskManager.menu[int(check) - 1].idx,
                                  date,
                                  TaskManager.menu[int(check) - 1].done]
                        TaskManager.menu[int(check) - 1] = Deadline(change[0], change[1], change[2], change[3])

                        out = 'Set {' + ''.join(
                            TaskManager.menu[int(check) - 1].description) + '} to be done by ' + str(date)

                # set by description
                else:

                    out = "SORRY, I could not perform that command. Problem: {" + check + '} is not an item in the menu'

                    # check if object in list matches user input
                    for i, b in enumerate(TaskManager.menu):
                        if check == ' '.join(b.description):
                            change = [TaskManager.menu[i].description, TaskManager.menu[i].idx, date,
                                      TaskManager.menu[i].done]
                            TaskManager.menu[i] = Deadline(change[0], change[1], change[2], change[3])
                            out = 'Added {' + check + '} to be done by ' + str(date)

        return out

    # Check work done
    def progress(self):
        out = 'Progress for this session: ToDos ' + str(ToDo.comTd) + ' Deadlines ' + str(Deadline.comDL)
        return out

    def deadline_check(self, date):
        due = []
        out = 'nothing is due\n'

        # check if any item in tasks is soon due with respect to current date
        new_date = date - datetime.timedelta(days=5)
        for i, b in enumerate(TaskManager.menu):
            if isinstance(b, Deadline) and ''.join(b.deadline) >= new_date.strftime("%d%b%y"):
                due.append(b)

        # output if anything is due
        if len(due) != 0:
            out = 'These following items are due:\nIndex:\n'
            for i, b in enumerate(due):
                out = out + ' '.join(b.idx) + ' : ' + ' '.join(b.description) + '\n'
            out = out + '\n'

        return out