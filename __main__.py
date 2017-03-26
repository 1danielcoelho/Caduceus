from tkinter import *
from mainwindow import MainWindow


def main():
    root = Tk()
    root.minsize(600, 400)
    root.geometry("600x400+300+300")
    app = MainWindow(root)

    root.mainloop()

if __name__ == '__main__':
    main()
