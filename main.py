from Frontend import MainWindow
from server import server_init
from _thread import *

if __name__ == '__main__':
    start_new_thread(server_init, ())
    MainWindow.main()
