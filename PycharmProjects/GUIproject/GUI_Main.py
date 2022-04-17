import sys
from tkinter import *  # For the GUI
from TaskManager import *  # For The TaskManager Class and the datetime module


class GUI:

    def __init__(self, task_manager):


        self.task_manager = task_manager
        self.window = Tk()
        self.window.geometry('1280x1080')  # set Window size
        self.window.title('Monty Python!!')  # set Window title

        # Adding a Banner for decoration purposes
        global banner
        banner = PhotoImage(file="python.png",width=1080, height= 260)
        self.label = Label(self.window, image = banner)
        self.label.pack()

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
        self.list_area = Text(self.window, width='82')
        self.list_area.pack(padx=5, pady=5, side=RIGHT, fill="both")
        self.list_area.tag_configure('normal_format', font=self.output_font)
        self.list_area.tag_configure('pending_format', foreground='red', font=self.output_font)
        self.list_area.tag_configure('done_format', foreground='green', font=self.output_font)

        # Check list of tasks for any dued or overdued tasks
        due = self.task_manager.deadline_check(datetime.datetime.today())

        # show the welcome message, anything due, and the list of tasks
        self.update_chat_history('start', 'Welcome to Monty!\n\n' + self.task_manager.get_help(), 'success_format')
        self.update_chat_history('Check Deadlines', due, 'error_format')
        self.update_task_list(self.task_manager.menu)

    def update_chat_history(self, command, response, status_format):
        """
        status_format: indicates which color to use for the status message
          can be 'error_format', 'success_format', or 'normal_format'
        """

        current_time = datetime.datetime.now().strftime("%a:%d %b %y:%H:%M:%S")
        self.history_area.insert(1.0, '-' * 60 + '\n', 'normal_format')
        self.history_area.insert(1.0, '>>> ' + response + '\n', status_format)
        self.history_area.insert(1.0, 'You said: ' + command + '\n', 'normal_format')
        self.history_area.insert(1.0, current_time + '\n', 'normal_format')

    def update_task_list(self, tasks):
        self.list_area.delete('1.0', END)  # clear the list area
        # Insert Header everytime it prints the task list
        self.list_area.insert(END, '''=================================================================
STATUS | INDEX | DESCRIPTION                 |     DEADLINE
-----------------------------------------------------------------''' + '\n', 'done_format')
        # printing tasks
        for b in tasks:
            # Setting format for done tasks and undone tasks
            if b.done is True:
                output_format = 'done_format'
            else:
                output_format = 'pending_format'
            self.list_area.insert(END, b.value() + '\n', output_format)
        # Update tasks to CSV file
        self.task_manager.sm.write_csv(TaskManager.menu)

    def clear_input_box(self):
        self.input_box.delete(0, END)

    def command_entered(self, event):
        command = None
        try:
            input_value = self.input_box.get()  # getting user input
            command = input_value.lower().split()  # making user input caps insensitive
            if input_value == 'exit':  # checking for exit condition
                sys.exit()
            output = self.task_manager.execute_command(command)  # Execute command given if correct
            self.update_chat_history(input_value, output, 'success_format')
            self.update_task_list(self.task_manager.menu)
            self.clear_input_box()
        except Exception as e:  # if command is wrong format
            self.update_chat_history(input_value, str(e) + '\n' + self.task_manager.get_help(), 'error_format')
            self.clear_input_box()

    def start(self):
        self.window.mainloop()


GUI(TaskManager()).start()
