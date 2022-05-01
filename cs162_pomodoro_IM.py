"""
Izayah Marchand
CS162
5/1/2022

This program is based off of the pomodoro study method where it is four 25 minute study sessions,
three 5 minute breaks between, and after the last study period there is a 15 minute break.
This can be split up into 8 intervals. So I made a list of the interval that one of those
periods would be on, and if the current interval is in one of those lists it would set the timer
to be that i.e. interval 2 makes the timer a 5 minute study break. This is all within
the Pomo class and the methods within that are the commands that the buttons do.
So it uses start_timer: starts the timer, pause_time: pauses the time, and next_b: goes to the 
next interval. 

"""

import tkinter as tk

YELLOW = "#FCF69C"
FONT = "Helvetica"
STUDY_TIME = 25
SHORT_BREAK = 5
LONG_BREAK = 15


class Pomo:

    def __init__(self):
        self.root = tk.Tk()

    def main(self):
        """This holds most of the components for the program, it initializes the window,
            buttons, note widget, and the mainloop."""

        self.canvas = tk.Canvas(self.root,bg = YELLOW, height= 600, width= 600 )
        #the side= argument in the pack() function pushes the button/label to the 
        #specified side in order recieved.
        self.canvas.pack(side=tk.BOTTOM)

        tomato_img = tk.PhotoImage(file="./pomo.png")
        self.canvas.create_image(300, 300, image=tomato_img)

        self.start_button = tk.Button(self.root, text="Start Timer",width=10, bd=10, command= self.start_timer)
        self.start_button.pack(side=tk.LEFT)

        self.root.title("POMODORO APP")
        self.intervals = 1
        self.timer = None

        self.interval_label = tk.Label(text="WELCOME", bg=YELLOW, font=(FONT, 50))
        self.interval_label.pack(side=tk.BOTTOM)

        self.pause_button = tk.Button(text = 'Pause', width=10, bd=10, command=self.pause_time)
        self.pause_button.pack(side=tk.TOP)

        self.next_button = tk.Button(text="Next Interval", width=10, bd=10, command= self.next_b)
        self.next_button.pack(side=tk.RIGHT )

        self.timer_text = self.canvas.create_text(300, 350, text="00:00", fill="white", font=(FONT, 35, "bold"))

        #lists of the intervals used to study. If the interval is in one of 
        #these lists it will call the countdown method to set the timer to 
        #it's respected interval. 
        self.study_list = [1,3,5,7]
        self.Sbreak_list = [2,4,6]
        self.Lbreak = 8

        self.study_sec = STUDY_TIME  * 60
        self.short_break = SHORT_BREAK * 60
        self.long_break = LONG_BREAK * 60

        self.note_label = tk.Label(text= "Notes", bg = "white", font=(FONT, 25))
        self.note_label.pack(side=tk.TOP)

        #a widget that allows the user to create notes if they wanted to.
        #it is prefilled with text implying that it is to reflect on the study period.
        u_notes = tk.Text(self.root, height= 10)
        u_notes.insert("1.0", "1st Study Period: \n2nd Study Period: \
                        \n3rd Study Period: \n4th Study Period: ")
        u_notes.pack()

        self.root.mainloop()

    def count_down(self, count):
        """This counts down the seconds, it also formats the timer text, the count 
            that is passed through is breaks/study time"""

        self.count_mins = count // 60 
        self.count_secs = count % 60 

        #f{ :02d} formats either side of the timer text to have two digits at all times.
        if self.count_secs < 10: 
            self.count_secs = f"{self.count_secs:02d}"

        if self.count_mins < 10:
            self.count_mins = f"{self.count_mins:02d}"

        self.canvas.itemconfig(self.timer_text, text=f"{self.count_mins}:{self.count_secs}") 

        if count > 0:
            self.timer = self.root.after(1000, self.count_down, count - 1) ## 5 - 1 = 4, pass 4,3,2,1 to count_down

    def start_timer(self):
        """This starts the timer. Sets all other buttons to 'activate' when start button
            is clicked, it will also change the type of timer if the timer text is 00:00"""

        self.start_button["state"] = "disabled"
        self.pause_button["state"] = "active"
        self.next_button["state"] = "active"
        

        self.current_timer = self.canvas.itemcget(self.timer_text, "text")

        
        if self.current_timer != "00:00" and self.pause_button["state"] == "active":
            self.current_timer = int(self.current_timer[0:2]) * 60 + int (self.current_timer[3:])
            self.count_down(self.current_timer)
            print('hey')
        
        #depending on which interval is called, it will change the time and
        #text of the label
        elif self.intervals == self.Lbreak:
            self.count_down(self.long_break) 
            self.interval_label.config(text="15 MIN BREAK TIME", bg="blue", fg="red")

        elif self.intervals in self.Sbreak_list:
            self.count_down(self.short_break)
            self.interval_label.config(text="5 MIN BREAK TIME", bg="yellow", fg="black")

        elif self.intervals in self.study_list:
            self.count_down(self.study_sec)
            self.interval_label.config(text="WORK TIME", bg="cyan", fg="green")

        #resets the interval once long break is passed
        if self.intervals >= self.Lbreak:
            self.intervals = 0

    def pause_time(self):
        """Pauses time"""

        self.pause_button["state"] = "disabled"
        self.start_button["state"] = "active"

        if self.timer:

            self.root.after_cancel(self.timer)
            self.timer = None
            


    def next_b(self):
        """Changes label text, switches the interval and pauses time so it doesn't
            continue w/o the user wanting it to. This also resets the timer text
            to be 00:00 so the next interval is activated once the start button is clicked."""

        self.next_button["state"] = "disabled"
        self.start_button["state"] = "active"
        self.interval_label.config(text="NEXT INTERVAL", bg="magenta", fg="white")
        self.canvas.itemconfig(self.timer_text,text="00:00" )
        self.intervals += 1

        print(self.intervals)
        self.pause_time()

pomo = Pomo()
pomo.main()
