import datetime
from StorageManager import *
from ToDo import *
from tkinter import *

import sys


class GUI:

    def __init__(self, task_manager):
        self.task_manager = task_manager
        self.window = Tk()
        self.window.geometry('1280x720')  # set Window size
        self.window.title('Monty')  # set Window title

        self.input_box = Entry(self.window)  # create an input box
        self.input_box.pack(padx=5, pady=5, fill='x')  # make the input box fill the width of the Window
        self.input_box.bind('<Return>', self.command_entered)  # bind the command_entered function to the Enter key
        self.input_box.focus()  # set focus to the input box

        # add a text area to show the chat history
        self.history_area = Text(self.window, width="75")
        self.history_area.pack(padx=5, pady=5, side=LEFT, fill="both")
        self.output_font = ('Courier New', 12)
        self.history_area.tag_configure('error_format', foreground='red', font=self.output_font)
        self.history_area.tag_configure('success_format', foreground='green', font=self.output_font)
        self.history_area.tag_configure('normal_format', font=self.output_font)

        # add a text area to show the list of tasks
        self.list_area = Text(self.window, width = '82')
        self.list_area.pack(padx=5, pady=5, side=RIGHT, fill="both")
        self.list_area.tag_configure('normal_format',  font=self.output_font)
        self.list_area.tag_configure('pending_format', foreground='red', font=self.output_font)
        self.list_area.tag_configure('done_format', foreground='green', font=self.output_font)

        # show the welcome message and the list of tasks
        self.update_chat_history('start', 'Welcome to Monty!\n' + self.task_manager.get_help(), 'success_format')
        self.update_task_list(self.task_manager.menu)

    def update_chat_history(self, command, response, status_format):
        """
        status_format: indicates which color to use for the status message
          can be 'error_format', 'success_format', or 'normal_format'
        """
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        self.history_area.insert(1.0, '-' * 60 + '\n', 'normal_format')
        self.history_area.insert(1.0, '>>> ' + response + '\n', status_format)
        self.history_area.insert(1.0, 'You said: ' + command + '\n', 'normal_format')
        self.history_area.insert(1.0, current_time + '\n', 'normal_format')

    def update_task_list(self, tasks):
        self.list_area.delete('1.0', END)  # clear the list area
        self.list_area.insert(END, '''=================================================================
STATUS | INDEX | DESCRIPTION                 |     DEADLINE
-----------------------------------------------------------------'''+'\n', 'done_format')
        for b in tasks:
            if b.done == True:
                output_format = 'done_format'
            if b.done == False:
                output_format = 'pending_format'
            self.list_area.insert(END,b.value()+'\n', output_format)
            TaskManager.sm.write_csv(TaskManager.menu)

    def clear_input_box(self):
        self.input_box.delete(0, END)

    def command_entered(self, event):
        command = None
        try:
            input_value = self.input_box.get()
            command = input_value.lower().split()
            if input_value == 'exit':
                sys.exit()
            output = self.task_manager.execute_command(command)
            self.update_chat_history(input_value, output, 'success_format')
            self.update_task_list(self.task_manager.menu)
            self.clear_input_box()
        except Exception as e:
            self.update_chat_history(input_value, str(e) + '\n' + self.task_manager.get_help(), 'error_format')
            self.clear_input_box()

    def start(self):
        self.window.mainloop()


class TaskManager:
    menu =[]
    sm = StorageManager('Monty_list.csv')
    def __init__(self):
        TaskManager.menu = TaskManager.sm.menu

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
        if inp[0] == "add":
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
        elif inp[0] == 'help':
            return self.get_help()
        else:
            raise Exception('Command not recognized')

    def todo(self):
        if len(self.user_input[1:]) != 0:
            check = ' '.join(self.user_input[-1])
            d_check = ' '.join(self.user_input[-3:-1])
            if check.isdigit() and d_check == 'at index':
                status = ToDo(self.user_input[1:-3], len(TaskManager.menu) + 1, False)
                TaskManager.menu.insert(int(check) - 1, status)
                for i, b in enumerate(TaskManager.menu):
                    b.chg_idx(i + 1)
                out = 'Added {' + ' '.join(self.user_input[1:-3]) + '} as a task to do.'
            else:
                status = ToDo(self.user_input[1:], len(TaskManager.menu) + 1, False)
                TaskManager.menu.append(status)
                out = 'Added {' + ' '.join(self.user_input[1:]) + '} as a task to do.'
            return out
        else:
            return 'empty command'

    def completed(self):
        check = ' '.join(self.user_input[1:])
        if len(self.user_input[1:]) != 0:
            if check.isdigit():
                if int(check) <= len(TaskManager.menu):
                    TaskManager.menu[int(check) - 1].completed()
                    out = 'Congrats on completing {'+' '.join(TaskManager.menu[int(check) - 1].description)+'} :)'
                    return out
                else:
                    out = 'SORRY, I could not perform that command. \nProblem: No item at index '+self.user_input[1]
                    return out
            elif check == 'all':
                for b in TaskManager.menu:
                    b.completed()
                return 'all done'
            else:
                for b in TaskManager.menu:
                    if check == ' '.join(b.description):
                        b.completed()
                        out = 'Congrats on completing {' + check + '} :)'
                        return out
                out = "SORRY, I could not perform that command. \nProblem: " + check+ ' is not an item in the menu'
                return out
        else:
            return 'empty command'

    def remove(self):
        check = ' '.join(self.user_input[1:])
        if len(self.user_input[1:]) != 0:
            if check.isdigit():
                if int(self.user_input[1]) <= len(TaskManager.menu):
                    del TaskManager.menu[int(self.user_input[1]) - 1]
                    for i, b in enumerate(TaskManager.menu):
                        b.chg_idx(i + 1)
                    out = 'removed {'+check+'}'
                    return out
                else:
                    out = 'SORRY, I could not perform that command. \nProblem: No item at index '+ check
                    return out
            elif check == 'all':
                TaskManager.menu.clear()
                return 'Removed all'
            else:
                for i, b in enumerate(TaskManager.menu):
                    if check == ' '.join(b.description):
                        del TaskManager.menu[i]
                        for i, b in enumerate(TaskManager.menu):
                            b.chg_idx(i + 1)
                        out = 'removed {' + check + '}'
                        return out
                out = "SORRY, I could not perform that command. \nProblem: {" +check+ '} is not an item in the menu'
                return out
        else:
            return 'incomplete command'

    def pend(self):
        check = ' '.join(self.user_input[1:])
        if len(self.user_input[1:]) != 0:
            if check.isdigit():
                if int(check) <= len(TaskManager.menu):
                    TaskManager.menu[int(check) - 1].undone()
                    out = 'Marked {'+' '.join(TaskManager.menu[int(check) - 1].description)+'} as pending'
                    return out
                else:
                    out = 'SORRY, I could not perform that command. \nProblem: No item at index '+str(self.user_input[1])
                    return out
            elif check == 'all':
                for b in TaskManager.menu:
                    b.undone()
                return 'all undone'
            else:
                for b in TaskManager.menu:
                    if check == ' '.join(b.description):
                        b.undone()
                        out = 'Marked {' + check + '} as pending'
                        return out
                out = "SORRY, I could not perform that command. \nProblem: {" + check+ '} is not an item in the menu'
                return out
        else:
            return 'empty command'

    #create new deadline tasks and set deadlines for to do tasks
    def deadline(self):
        if 'by' in self.user_input:
            i = self.user_input.index('by')
            check = ' '.join(self.user_input[1:i])
            date = ' '.join(self.user_input[i + 1:])
            if self.user_input[0] == 'deadline':
                TaskManager.menu.append(Deadline(self.user_input[1:i], len(TaskManager.menu) + 1, self.user_input[i + 1:], False))
                out = 'Added {'+' '.join(self.user_input[1:i])+'} to be done by '+ str(date)
                return out
            else:
                if len(self.user_input[1:]) != 0:
                    if check.isdigit():
                        if int(check) <= len(TaskManager.menu):
                            change = [TaskManager.menu[int(check) - 1].description, TaskManager.menu[int(check) - 1].idx, date,
                                      TaskManager.menu[int(check) - 1].done]
                            TaskManager.menu[int(check) - 1] = Deadline(change[0], change[1], change[2], change[3])
                            out = 'Set {'+''.join(TaskManager.menu[int(check) - 1].description)+'} to be done by '+ str(date)
                            return out
                        else:
                            out = 'SORRY, I could not perform that command. Problem: No item at index '+str(self.user_input[1])
                            return out
                    else:
                        for i, b in enumerate(TaskManager.menu):
                            if check == ' '.join(b.description):
                                change = [TaskManager.menu[i].description, TaskManager.menu[i].idx, date, TaskManager.menu[i].done]
                                TaskManager.menu[i] = Deadline(change[0], change[1], change[2], change[3])
                                out = 'Added {' + check + '} to be done by ' + str(date)
                                return out
                        out = "SORRY, I could not perform that command. Problem: {" + check+'} is not an item in the menu'
                        return out
                else:
                    return 'empty command'
        else:
            return 'wrong format'

    #Check work done
    def progress(self):
        out = 'Progress for this session: ToDos '+str(ToDo.comTd)+' Deadlines '+str(Deadline.comDL)
        return out
GUI(TaskManager()).start()