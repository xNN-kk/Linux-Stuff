#!/usr/bin/env python2

#
# A simple Tasklist manager with openbox and conky integration.
#
# Openbox:
# Put an entry in ~/.config/openbox/menu.xml:
# <menu id="pipe-tasklist" label="Task List" execute="python /path/to/todo.py menu" />
#
# Then put the following wherever you'd like it to be displayed in your menu:
# <menu id="pipe-tasklist" />
#
# Conky:
# Place ${head /path/to/list 30 20} in your conkyrc
#

import sys, os

# File where tasks are to be stored. Use complete path
tasklistfile = os.path.expanduser('~') + '/.todo'

# tags = ['Important', 'Normal', 'Low']  # Array with possible tags to apply. Could be in later version

# Name and path the program. Used for certain actions that call system functions
selfname = sys.argv[0]

class Todo:
    def __init__(self):
        self.tasklist = []
        self.file = tasklistfile

        # Required for openbox menu
        self.add_action = 'xterm -geometry 50x1+520+350 -e "{} new"'.format(selfname)
        self.del_action = '{} del'.format(selfname)

        self.open()

    def open(self):
        """ Open and parse a todo file, or create a new one if it doesn't exist currently """
        try:
            f = open(self.file, 'rb')
            for line in f:
                self.tasklist.append(line)
            f.close()
        except IOError:
            f = open(self.file, 'w+')
            for line in f:
                self.tasklist.append(line)
            f.close()

    def save(self):
        """ Save tasklist to file """
        f = open(self.file, 'wb')
        for line in self.tasklist:
            f.write(line)
        f.close()

    def add_task(self, task):
        """ Append new item to task list and save the file """
        self.tasklist.append(task+'\n')
        self.save()

    def new_task(self):
        """ Get a new task from the command line """
        task = raw_input('New Task: ')
        self.add_task(task)

    def del_task(self, task):
        """ Remove a specific task """
        if len(self.tasklist) == 0:
            print('there are no tasks to remove')
        else:
            if task > len(self.tasklist) or task < 0:
                print('the task is out of range')
            else:
                del self.tasklist[task]
                self.save()

    def print_list(self):
        """ Print the task list """
        if len(self.tasklist) == 0:
            print('nothing to do!')
        else:
            for i, line in enumerate(self.tasklist):
                print(''.join([str(i+1), '. ', line.strip()]))

    def print_menu(self):
        """ Print an xml menu for openbox """
        print '<openbox_pipe_menu>'
        print '<item label="New Task">'
        print '<action name="Execute">'
        print '<command>%s</command>' % (self.add_action)
        print '</action>'
        print '</item>'
        print '<separator />'

        if self.tasklist == []:
            print '<item label="Nothing to do!">'
            print '</item>'
        else:
            for i, t in enumerate(self.tasklist):
                print '<item label="' + t + '">'
                print '<action name="Execute">'
                print '<command>%s</command>' % (self.del_action + ' ' + str(i))
                print '</action>'
                print '</item>'
        print '</openbox_pipe_menu>'

    def test(self):
        ''' Test some things about the class '''
        print('Add action: ' + self.add_action)
        print('Delete action: ' + self.del_action)

# Instantize classs
todo = Todo()

try:
    if sys.argv[1] == "new":
        # Add a task from the command line
        todo.new_task()

    elif sys.argv[1] == "del":
        # Remove a task based on it's location in the tasklist array
        t = int(sys.argv[2])
        todo.del_task(t)

    elif sys.argv[1] == "done":
        # Remove a task based on the corresponding number (1 + array location)
        try:
            t = int(sys.argv[2])-1
            todo.del_task(t)
        except ValueError:
            ans = raw_input('remove all tasks? (y/n): ')
            if ans.lower() in ['y', 'yes']:
                if sys.argv[2] == 'all':
                    for i, t in enumerate(todo.tasklist):
                        print('removing task "' + t.strip() + '"')
                        todo.del_task(i)
            else:
                exit(1)

        except IndexError:
            print('either you forgot to enter a number, or it is out of range')

    elif sys.argv[1] == "menu":
        # Print the openbox pipe menu
        todo.print_menu()

    elif sys.argv[1] == "add":
        # Turn everything after 'add' into the task from the command line
        try:
            task = sys.argv[2:]
            todo.add_task(' '.join(task))
        except IndexError:
            pass

    elif sys.argv[1] == 'test':
        # See what the actions are for the openbox menu
        todo.test()

    else:
        pass

# Otherwise assumes that there were no arguments passed
except IndexError:
    todo.print_list()
