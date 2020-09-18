import time

import colorlabels as cl


def welcome():
    cl.section('ColorLabels Demo')
    cl.newline()
    cl.item('1. Overview of Labels')
    cl.item('2. Progress Animations')
    cl.item('3. Show Demo 1')
    cl.item('4. Show Demo 2')
    cl.item('5. Exit')
    cl.newline()


def get_menu_option():
    option = ''
    while option not in {'1', '2', '3', '4', '5'}:
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


def animations():
    cl.section('Progress Animations')

    cl.item('Static')
    cl.progress('Downloading...')
    time.sleep(3)

    cl.item('Spin')
    with cl.progress('Downloading...', mode=cl.PROGRESS_SPIN):
        time.sleep(3)

    cl.item('Expand')
    with cl.progress('Downloading', mode=cl.PROGRESS_EXPAND):
        time.sleep(6)

    cl.item('Move')
    with cl.progress('Downloading ', mode=cl.PROGRESS_MOVE):
        time.sleep(4)

    cl.item('Determinate')
    with cl.progress('Downloading ', mode=cl.PROGRESS_DETERMINATE) as p:
        time.sleep(1)
        p.update(0.2, ' 20% (1MB/5MB) ETA 4s')
        time.sleep(1)
        p.update(0.4, ' 40% (2MB/5MB) ETA 3s')
        time.sleep(1)
        p.update(0.6, ' 60% (3MB/5MB) ETA 2s')
        time.sleep(1)
        p.update(0.8, ' 80% (4MB/5MB) ETA 1s')
        time.sleep(1)
        p.update(1, ' 100% (5MB/5MB)')


def demo1():
    cl.section('Demo 1')

    cl.info('Test program started.')

    with cl.progress('Running test case 1...', cl.PROGRESS_SPIN, erase=True):
        time.sleep(3)
    cl.success('Test case 1: Passed')

    with cl.progress('Running test case 2...', cl.PROGRESS_SPIN, erase=True):
        time.sleep(3)
    cl.success('Test case 2: Passed')

    with cl.progress('Running test case 3...', cl.PROGRESS_SPIN, erase=True):
        time.sleep(3)
    cl.success('Test case 3: Passed')

    with cl.progress('Running test case 4...', cl.PROGRESS_SPIN, erase=True):
        time.sleep(3)
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

    with cl.progress('Checking for update...', mode=cl.PROGRESS_SPIN):
        time.sleep(3)

    choice = ''
    while choice.lower() not in {'y', 'n'}:
        choice = cl.question('A new version is present, would you like to update? (Y/N)').strip()

    if choice.lower() == 'y':
        with cl.progress('Downloading ', mode=cl.PROGRESS_DETERMINATE) as p:
            time.sleep(1)
            p.update(0.2, ' 20% (1MB/5MB) ETA 4s')
            time.sleep(2)
            p.update(0.4, ' 40% (2MB/5MB) ETA 3s')

        cl.error('Failed to download package. SSL handshake error.')
    else:
        cl.warning('Update delayed!')


def main():
    try:
        while True:
            welcome()
            option = get_menu_option()
            if option != 5:
                cl.newline()
            if option == 1:
                overview()
            elif option == 2:
                animations()
            elif option == 3:
                demo1()
            elif option == 4:
                demo2()
            else:
                cl.plain('Bye!')
                break
            cl.newline()
            cl.input('Press Enter to continue...')
            cl.newline()
    except (KeyboardInterrupt, EOFError):
        cl.newline()
        cl.warning('Ctrl-C or EOF received, quitting.')


if __name__ == '__main__':
    main()
