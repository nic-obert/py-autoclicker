#!/usr/bin/env python3
from time import sleep
from threading import Thread
import pynput.mouse as ms
import pynput.keyboard as kb
from tkinter import Entry, Label, Frame, Tk, StringVar, END, Button, LEFT, RIGHT


class AutoClicker(Thread):
    def __init__(self):
        super(AutoClicker, self).__init__()

        self.ctrl_pressed = False # true if ctrl is pressed
        self.cps_changed = False  # true if a change in cps count comes from inside the script
        self.auto_scrolled = False # true if scroll comes from inside the script

        self.b1_previous = 5  # default cps
        self.b1 = ms.Button.left
        self.b1_cps = self.b1_previous  # max 60 cps but not always \ comment out delay to max out cps
        self.b1_delay = (1 / self.b1_cps) - (1 / self.b1_cps) / 4.5
        self.b1_clicking = False
        self.b1_key = kb.Key.caps_lock # default b1 key: caps lock

        self.b2_previous = 3 # default cps
        self.b2 = ms.Button.right
        self.b2_cps = self.b2_previous
        self.b2_delay = (1 / self.b2_cps) - (1 / self.b2_cps) / 4.5
        self.b2_clicking = False
        self.b2_key = kb.Key.ctrl_r

        self.running = True
        self.on_top = False # True if always on top panel is displayed


    def run(self):
        b1_thread = Thread(target=self.b1_run) # start a thread for each button (left and right)
        b1_thread.start()
        b2_thread = Thread(target=self.b2_run)
        b2_thread.start()


    def b1_run(self):
        while self.running:
            sleep(0.00001)
            while self.b1_clicking:
                mouse.click(self.b1)
                sleep(self.b1_delay) # comment out this line for max cps

    def b2_run(self):
        while self.running:
            sleep(0.00001)
            while self.b2_clicking:
                mouse.click(self.b2)
                sleep(self.b2_delay)


    def back_to_main(self):
        self.on_top = False # on_top is false since always on top panel is being destroyed
        #self.root.destroy()
        self.main_draw() # redraw main window



    def top_panel_draw(self):
        self.on_top = True # on_top is True since always on top panel is being drawn
        self.root.destroy()
        self.root = Tk()
        self.root.attributes('-topmost', 'true') # always show this window on top
        self.root.title('GUI Autoclicker - by Obert')
        self.root.config(bg='#ffffff')

        self.b1_input_cps_var = StringVar()
        self.b1_clicks_entry = Entry(master=self.root, textvariable=self.b1_input_cps_var, width=3, font=('System', 12, 'bold'), fg='#000000')
        self.b1_clicks_entry.pack(side=LEFT)
        self.b1_clicks_entry.insert(0, autoclicker.b1_cps)

        self.b2_input_cps_var = StringVar()
        self.b2_clicks_entry = Entry(master=self.root, textvariable=self.b2_input_cps_var, width=3, font=('System', 12, 'bold'), fg='#000000')
        self.b2_clicks_entry.pack(side=RIGHT)
        self.b2_clicks_entry.insert(0, autoclicker.b2_cps)



    def main_draw(self):
        self.root = Tk()
        self.root.title('GUI Autoclicker - by Obert')
        self.root.config(bg='#ffffff')
        self.root.geometry('500x400')

        padding = Frame(self.root)
        padding.grid(row=0, columnspan=10, pady=30)
        padding = Frame(self.root)
        padding.grid(row=1, column=0, padx=20)
        b1_clicks_label = Label(self.root, text='(Button 1) CPS', bg='#ffffff', font=('System', 16, 'bold'))
        b1_clicks_label.grid(row=1, column=1)
        self.b1_input_cps_var = StringVar()
        self.b1_clicks_entry = Entry(master=self.root, textvariable=self.b1_input_cps_var, width=10, font=('System', 16, 'bold'))
        self.b1_clicks_entry.insert(0, str(autoclicker.b1_cps))
        self.b1_clicks_entry.grid(row=1, column=2, padx=5)

        b2_clicks_label = Label(self.root, text='(Button 2) CPS', bg='#ffffff', font=('System', 16, 'bold'))
        b2_clicks_label.grid(row=3, column=1)
        self.b2_input_cps_var = StringVar()
        self.b2_clicks_entry = Entry(master=self.root, textvariable=self.b2_input_cps_var, width=10, font=('System', 16, 'bold'))
        self.b2_clicks_entry.insert(0, str(autoclicker.b2_cps))
        self.b2_clicks_entry.grid(row=3, column=2, padx=5)

        self.b1_invalid_cps_input = Label(self.root, text='Invalid input cps', fg='#ffffff', bg='#ffffff')
        self.b1_invalid_cps_input.grid(row=2, column=2)

        self.b2_invalid_cps_input = Label(self.root, text='Invalid input cps', fg='#ffffff', bg='#ffffff')
        self.b2_invalid_cps_input.grid(row=4, column=2)

        on_top_button = Button(self.root, text='Show top panel', bg='#ffffff', font=('System', 16, 'bold'), command=self.top_panel_draw)
        on_top_button.grid(row=5, columnspan=2, pady=20)



class Listener:
    @staticmethod
    def on_scroll(x, y, dx, dy):

        if autoclicker.auto_scrolled: # if mouse wheel scroll comes from inside the script don't do anything, just set auto_scrolled to False
            autoclicker.auto_scrolled = False
        else: # if mouse wheel scroll comes from the user instead increase/decrease cps count
            autoclicker.auto_scrolled = True # set auto_scrolled to True so that the script ignores this
            mouse.scroll(dx=0, dy=dy*-1) # scroll the wheel to original position since you are not supposed to randomly scroll while changing cps count
            if autoclicker.b1_clicking: # change cps count of the button that is currently clicking
                autoclicker.b1_cps += dy # increase/decrease cps based on how much you scrolled
                if autoclicker.b1_cps <= 0: # if you reached the minimum amount of cps (1 cps) don't decrease it anymore
                    autoclicker.b1_cps = 1
                autoclicker.b1_delay = (1 / autoclicker.b1_cps) - (1 / autoclicker.b1_cps) / 4.5 # finally update the clicking speed
                autoclicker.cps_changed = True # set the cps_changed to True tell the gui's main loop to update the cps entry
            if autoclicker.b2_clicking:
                autoclicker.b2_cps += dy
                if autoclicker.b2_cps <= 0:
                    autoclicker.b2_cps = 1
                autoclicker.b2_delay = (1 / autoclicker.b2_cps) - (1 / autoclicker.b2_cps) / 4.5
                autoclicker.cps_changed = True

    @staticmethod
    def on_release(key):
        if key == kb.Key.ctrl: # when ctrl key is released set crtl_pressed to false
            autoclicker.ctrl_pressed = False


    @classmethod
    def mouse_listener(cls):
        with ms.Listener(on_scroll=cls.on_scroll) as l:
            while autoclicker.ctrl_pressed:
                sleep(0.05)

    @classmethod
    def on_press(cls, key):
        #key = str(key)
        #key = key.replace("'", '')

        if key == autoclicker.b1_key:
            autoclicker.b1_clicking = not autoclicker.b1_clicking
        elif key == autoclicker.b2_key:
            autoclicker.b2_clicking = not autoclicker.b2_clicking
        elif key == kb.Key.ctrl: # if ctrl is pressed start listening for mouse wheel scrolling
            autoclicker.ctrl_pressed = True
            m_listener = Thread(target=cls.mouse_listener)
            m_listener.start() # start mouse listener thread


    @classmethod
    def keyboard_listen(cls): # keyboard listener
        with kb.Listener(on_press=cls.on_press, on_release=cls.on_release) as l:
            while autoclicker.running:
                sleep(0.1)

    @classmethod
    def init(cls):
        k_listener = Thread(target=cls.keyboard_listen)
        k_listener.start()  # start listener thread



mouse = ms.Controller() # define mouse controller
autoclicker = AutoClicker() # create autoclicker
autoclicker.start() # start autoclicker thread

autoclicker.main_draw()

Listener.init()

run = True
while run: # gui main loop
    try:
        try:
            b1_cps = int(autoclicker.b1_input_cps_var.get()) # get input cps
            if autoclicker.on_top: # if displaying the always on top panel
                autoclicker.b1_clicks_entry['fg'] = '#000000'
            else: # if displaying the main non-on-top window
                autoclicker.b1_invalid_cps_input['fg'] = '#ffffff' # don't show the invalid input label

            if autoclicker.cps_changed: # if current cps changed from inside the script --> update the gui
                autoclicker.b1_clicks_entry.delete(0, END)
                autoclicker.b1_clicks_entry.insert(0, str(autoclicker.b1_cps))

        except ValueError:
            if autoclicker.on_top: # if on_top is True change the color of the text, do not display anything else to save space
                autoclicker.b1_clicks_entry['fg'] = '#ff0000'
            else:
                autoclicker.b1_invalid_cps_input['fg'] = '#ff0000' # if input cps invalid --> show error label

        try:
            b2_cps = int(autoclicker.b2_input_cps_var.get())
            if autoclicker.on_top:  # if displaying the always on top panel
                autoclicker.b2_clicks_entry['fg'] = '#000000' # don't show text as red if input is valid
            else:  # if displaying the main non-on-top window
                autoclicker.b2_invalid_cps_input['fg'] = '#ffffff'  # don't show the invalid input label

            if autoclicker.cps_changed:
                autoclicker.b2_clicks_entry.delete(0, END)
                autoclicker.b2_clicks_entry.insert(0, str(autoclicker.b2_cps))

        except ValueError:
            if autoclicker.on_top:
                autoclicker.b2_clicks_entry['fg'] = '#ff0000'
            else:
                autoclicker.b2_invalid_cps_input['fg'] = '#ff0000'

        autoclicker.cps_changed = False # finally set this bool to false

        if autoclicker.b1_previous != b1_cps: # if input cps different from current cps --> change cps count
            autoclicker.b1_cps = b1_cps
            autoclicker.b1_delay = (1 / autoclicker.b1_cps) - (1 / autoclicker.b1_cps) / 4.5
            autoclicker.b1_previous = b1_cps

        if autoclicker.b2_previous != b2_cps:
            autoclicker.b2_cps = b2_cps
            autoclicker.b2_delay = (1 / autoclicker.b2_cps) - (1 / autoclicker.b2_cps) / 4.5
            autoclicker.b2_previous = b2_cps


        sleep(0.07) # gui refresh rate
        autoclicker.root.update() # update the gui


    except: # if there is any problem just end the process
        if autoclicker.on_top: # if displaying the always on top panel then return to main window
            autoclicker.back_to_main()
        else: # if displaying the main window then close the program
            run = False # kill the gui refreshing loop
            autoclicker.running = False # stop the autoclicker
            autoclicker.b1_clicking = False # stop clicking
            autoclicker.b2_clicking = False
            break # break the loop just in case "run = False" for some reason did not work


quit(0) # quit the program
