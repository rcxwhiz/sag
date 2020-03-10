import os
import shutil
import sys
from os.path import join

import InstructorProgram as IP
from Config import cfg
from FileExecution import execute
from Navigation.structure import Dirs

dirs = Dirs()


def run(display_title=True):
    if display_title:
        print(IP.title.title_string)
    choice = IP.tools.input_num_range(1, 3)
    if choice == 1:
        grade()
    if choice == 2:
        make_dir()
    if choice == 3:
        print('\nExiting...')
        sys.exit()


def grade():
    if len(dirs.assignment_dirs) == 0:
        print('\nNo assignment directories created.')
        run()
    print('Select assignment to grade:')
    dirs.print_dirs()
    print('[0] - Cancel\n')
    assignment_num = IP.tools.input_num_range(0, len(dirs.assignment_dirs) + 1) - 1

    if assignment_num == -1:
        run()

    errors = dirs.check_full(assignment_num)
    if len(errors) > 0:
        print('\n'.join(errors))
        print('Returning to menu...')
        run()

    print('Options:')
    print('[1] - Generate key files')
    print('[2] - Export student testing program')
    print('[3] - Grade student code')
    print('[4] - View grading report')
    print('[0] - Cancel\n')
    assignment_option = IP.tools.input_num_range(0, 4)

    if assignment_option == 1:
        # check to see if there are already key files
        current_keys = os.listdir(join(dirs.base, dirs.assignment_dirs[assignment_num], 'key-output'))
        if len(current_keys) > 0:
            print('[1] - Overwrite current key files')
            print('[0] - Don\'t overwrite current key files')
            overwrite = IP.tools.input_num_range(0, 1)
            if overwrite == 1:
                shutil.rmtree(join(dirs.base, dirs.assignment_dirs[assignment_num], 'key-output'), ignore_errors=True)
                os.mkdir(join(dirs.base, dirs.assignment_dirs[assignment_num], 'key-output'))
            else:
                print('Returning to menu...')
                run()

        execute.run_key(join(dirs.base, dirs.assignment_dirs[assignment_num]))

    if assignment_option == 2:
        print('')
    if assignment_option == 3:
        print('')
    if assignment_option == 4:
        print('')
    if assignment_option == 0:
        run()

    # enter a menu with the following options
    # [1] generate key files
    # There needs to be some option to only have 1 test case I guess for problems where data will not be loaded
    # [2] export student's grading program
    # [3] run student code
    # [4] visually look at the code student's submitted (like my old program)
    # When running code on threads it might be the best idea to just clear the screen with a bunch of new lines?

    run()


def make_dir():
    print('\nCurrent directories:')
    dirs.print_dirs()
    print('\nCreate a new assignment directory in your base directory (can be changed in config.ini)')
    print('Enter a blank directory to stop\n')
    while True:
        new_dir = input(f'{cfg.base_directory}/')
        if new_dir == '':
            break
        else:
            dirs.create_new(new_dir)
    run()
