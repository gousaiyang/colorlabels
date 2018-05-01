from __future__ import print_function

import sys
import time
import colorlabels as cl

def welcome():
    cl.section('ColorLabels Demo')
    print()
    cl.item('1. Overview of Labels')
    cl.item('2. Show Demo 1')
    cl.item('3. Show Demo 2')
    cl.item('4. Exit')
    print()

def get_menu_option():
    option = ''

    while option not in ['1', '2', '3', '4']:
        option = cl.input('Input your option: ').strip()

    return int(option)

def overview():
    cl.section('Overview of Labels')
    cl.success('Good job! All test cases passed!')
    cl.warning('Warning! Security update delayed!')
    cl.error('Error! Failed to write file!')
    cl.info('Server listening on port 8888.')
    cl.progress('Downloading package, please wait...')
    cl.plain('Nothing interesting.')
    cl.question('A new version is present, would you like to update? (Y/N)')

def demo1():
    cl.section('Demo 1')

    cl.info('Test program started.')

    time.sleep(1)
    cl.success('Test case 1: Passed')
    time.sleep(1)
    cl.success('Test case 2: Passed')
    time.sleep(1)
    cl.success('Test case 3: Passed')
    time.sleep(1)
    cl.error('Test case 4: Failed')
    cl.info('Input: 1111')
    cl.info('Expected output: 2222')
    cl.info('Got: 3333')

    cl.section('Test Result')
    cl.info('3 out of 4 test cases passed.')
    cl.info('Pass rate: 75%')

def demo2():
    cl.section('Demo 2')

    username = ''
    while not username:
        username = cl.input('Username: ').strip()

    password = ''
    while not password:
        password = cl.password('Password: ')

    cl.success('Successfully logged in.')

    cl.progress('Checking for update...')
    time.sleep(2)

    choice = ''
    while choice.lower() not in ['y', 'n']:
        choice = cl.question('A new version is present, would you like to update? (Y/N)').strip()

    if choice.lower() == 'y':
        cl.progress('Downloading package, please wait...')
        time.sleep(3)
        cl.error('Failed to download package. SSL handshake error.')
    else:
        cl.warning('Update delayed!')

def main():
    try:
        while True:
            welcome()
            option = get_menu_option()

            if option != 4:
                print()

            if option == 1:
                overview()
            elif option == 2:
                demo1()
            elif option == 3:
                demo2()
            else:
                cl.plain('Bye!')
                break

            print()
            cl.input('Press Enter to continue...')
            print()
    except KeyboardInterrupt:
        print()
        cl.warning('Ctrl-C received, quitting.')

if __name__ == '__main__':
    main()
