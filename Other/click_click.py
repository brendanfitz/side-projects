import pyautogui
import time
import tkinter as tk

class App(tk.Frame):

    CLICK_SECONDS = 10

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent

        self.running = False

        self.time = -1

        self.create_timer_label()

        self.create_button_frame()
        self.create_start_button()
        self.create_stop_button()

        self.last_click_time = time.time()
    
    def click_start(self):
        self.running = True
        self.start_button.config(relief='sunken')
        self.stop_button.config(relief='raised')
        self.count()
    
    def click_stop(self):
        self.running = False 
        self.start_button.config(relief='raised')
        self.stop_button.config(relief='sunken')

    def create_timer_label(self):
        self.timer_label = tk.Label(self, text="Press Start", fg="black", font="Verdana 30 bold")
        self.timer_label.pack(padx=10, pady=10)
    
    def create_button_frame(self):
        self.button_frame = tk.Frame(self.parent)
        self.button_frame.pack(side="bottom")
    
    def create_start_button(self):
        self.start_button = tk.Button(self.button_frame, text="Start", command=self.click_start)
        self.start_button.pack(side="left", padx=5, pady=5, ipadx=25, ipady=5)
    
    def create_stop_button(self):
        self.stop_button = tk.Button(self.button_frame, text="Stop", command=self.click_stop, relief='sunken')
        self.stop_button.pack(side="left", padx=5, pady=5, ipadx=25, ipady=5)
    
    # def click(self):
    #     current_time = time.time()
    #     
    #     # check if minute has passed
    #     if current_time - self.last_click_time >= 60:
    #         self.last_click_time = current_time
    #         if self.running:
    #             pyautogui.click()
    #             print('clicked')
    #         else:
    #             print('no click')
    def count(self):
        if self.running:
            if self.time == 0:
                pyautogui.click()
                self.time = self.CLICK_SECONDS
            elif self.time == -1:
                self.time = self.CLICK_SECONDS
            else:
                self.time -= 1
            
            self.timer_label['text'] = self.time

            self.timer_label.after(1000, self.count)
        else:
            self.time = -1
            self.timer_label['text'] = 'Press Start'
        





    
if __name__ == '__main__':
    root = tk.Tk()
    frame = App(root)
    frame.pack()

    root.mainloop()

    # while True:
    #     try:
    #         if not root.winfo_exists():
    #             break
    #     except tk.TclError as e:
    #         break
    #     
    #     frame.click()
    #     root.update()


