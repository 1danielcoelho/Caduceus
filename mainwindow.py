from tkinter.filedialog import askopenfilenames
import dicom
import PIL.Image
import PIL.ImageTk

from statusbar import *
from imager import Imager


class MainWindow(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.parent = parent

        self.image = None
        self.photo = None
        self.canvas = None
        self.imager = None

        self.status = None
        self.right_click_menu = None

        self.mouse_wheel_down = False
        self.last_mouse_pos = None

        self.init_ui()

    def init_ui(self):
        self.parent.title("Caduceus")

        self.init_toolbar()

        # Image canvas
        self.canvas = Canvas(self.parent, bd=0, highlightthickness=0, bg="gray")
        self.canvas.pack(side=TOP, expand=1)
        self.canvas.bind("<Button-3>", self.show_right_click_menu)  # <Button-3> is the right click event
        self.canvas.bind("<MouseWheel>", self.scroll_images)
        self.canvas.bind("<B2-Motion>", self.on_mouse_wheel_drag)
        self.canvas.bind("<Button-2>", self.on_mouse_wheel_down)
        self.canvas.bind("<ButtonRelease-2>", self.on_mouse_wheel_up)
        #  self.canvas.bind("<Configure>", self.resize)

        # Status bar
        self.status = StatusBar(self.parent)
        self.status.pack(side=BOTTOM, fill=X)

        # Right-click menu
        self.right_click_menu = Menu(self.parent, tearoff=0)
        self.right_click_menu.add_command(label="Beep", command=self.bell)
        self.right_click_menu.add_command(label="Exit", command=self.on_exit)

    def init_toolbar(self):
        # Top level menu
        menubar = Menu(self.parent, bd=0)
        self.parent.config(menu=menubar, bd=0)

        # "File" menu
        filemenu = Menu(menubar, tearoff=False, bd=0)  # tearoff False removes the dashed line
        menubar.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="New", command=self.callback)
        filemenu.add_command(label="Open...", command=self.on_open)

        # Open recent submenu
        submenu = Menu(filemenu, tearoff=False)  # tearoff False removes the dashed line
        submenu.add_command(label="blah")
        filemenu.add_cascade(label="Open Recent", menu=submenu, underline=0)

        # Rest of the "File" menu
        filemenu.add_separator()
        filemenu.add_command(label="Save", command=self.callback)
        filemenu.add_command(label="Save As...", command=self.callback)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.on_exit)

    def show_image(self, numpy_array):
        if numpy_array is None:
            return

        # Convert numpy array into a PhotoImage and add it to canvas
        self.image = PIL.Image.fromarray(numpy_array)
        self.photo = PIL.ImageTk.PhotoImage(self.image)
        self.canvas.delete("IMG")
        self.canvas.create_image(0, 0, image=self.photo, anchor=NW, tags="IMG")
        self.canvas.configure(width=self.image.width, height=self.image.height)

        # We need to at least fit the entire image, but don't shrink if we don't have to
        width = max(self.parent.winfo_width(), self.image.width)
        height = max(self.parent.winfo_height(), self.image.height + StatusBar.height)

        # Resize root window and prevent resizing smaller than the image
        newsize = "{}x{}".format(width, height)
        self.parent.geometry(newsize)
        self.parent.minsize(self.image.width, self.image.height + StatusBar.height)

    def resize(self, event):
        if self.image is None:
            return

        # size = (event.width, event.height)
        # resized = self.image.resize(size, PIL.Image.NORMAL)
        # self.photo = PIL.ImageTk.PhotoImage(resized)
        # self.canvas.delete("IMG")
        # self.canvas.create_image(size[0]/2, size[1]/2, image=self.photo, anchor=CENTER, tags="IMG")

    def show_right_click_menu(self, e):
        self.right_click_menu.post(e.x_root, e.y_root)

    def scroll_images(self, e):
        self.imager.index += int(e.delta/120)
        self.show_image(self.imager.get_current_image())

    def on_mouse_wheel_down(self, e):
        self.last_mouse_pos = (e.x, e.y)
        self.mouse_wheel_down = True

    def on_mouse_wheel_up(self, e):
        self.last_mouse_pos = None
        self.mouse_wheel_down = True

    def on_mouse_wheel_drag(self, e):
        if self.mouse_wheel_down:
            delta = (e.x - self.last_mouse_pos[0], e.y - self.last_mouse_pos[1])
            self.last_mouse_pos = (e.x, e.y)

            self.imager.window_width += delta[0] * 5
            self.imager.window_center += delta[1] * 5

            self.show_image(self.imager.get_current_image())

    def on_open(self):
        filenames = list(askopenfilenames(filetypes=(("All files", "*.*"),
                                                     ("DICOM files", "*.dcm"))))

        num_total = len(filenames)
        num_bad = 0

        # Clear non-dicom files
        datasets = []
        for file in filenames:
            try:
                datasets.append(dicom.read_file(file))
            except dicom.errors.InvalidDicomError:
                num_bad += 1
                filenames.remove(file)
        num_ok = num_total - num_bad

        # Try to sort based on instance number then SOPInstanceUID
        sorted_method = "filenames"
        try:
            datasets.sort(key=lambda x: x.InstanceNumber)
            sorted_method = "instance number"
        except AttributeError:
            try:
                datasets.sort(key=lambda x: x.SOPInstanceUID)
                sorted_method = "SOP instance UID"
            except AttributeError:
                pass

        self.imager = Imager(datasets)

        self.status.set("Opened %d DICOM file(s) sorted on %s. Rejected %d bad file(s)", num_ok, sorted_method, num_bad)

        self.show_image(self.imager.get_current_image())

    def callback(self):
        self.status.set("Not implemented yet!")

    def on_exit(self):
        self.quit()
