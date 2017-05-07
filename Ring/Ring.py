from tkinter import *
import tkinter.ttk as ttk
from itertools import count
import os
import ast
import time
import wave
import configparser
import pyaudio


if os.name == 'posix':
    ROOT_WIDTH = 397
    ROOT_HEIGHT = 507
else:
    ROOT_WIDTH = 372
    ROOT_HEIGHT = 507

BASE_DIR = os.path.abspath(os.path.curdir)
SOUNDS_DIR = os.path.join(BASE_DIR, "soundBox/")
SOUNDS_LIST = [''] + os.listdir("soundBox")


class AlarmClock:
    """AlarmClock docs"""
    frame_counter = 1
    # alarms = {}
    # alarm_time = {}

    def __init__(self):
        self.alarms = {}
        self.alarm_time = {}

    @classmethod
    def get_frame_counter(cls):
        return AlarmClock.frame_counter

    def make_frame(self, window_to_place_in, row_position, col_position):
        """make_frame docs"""
        AlarmClock.frame_counter += 1
        next(frame_id)

        def do_on(event):
            """do_on docs"""
            caller = event.widget.winfo_parent()
            if indicator["background"] == "red":
                for key, val in self.alarms.items():
                    for item in self.alarms[key]:
                        if caller in item.winfo_parent() and item.winfo_class() == "Entry":
                            self.alarm_time[val[3]] = val[0].get()+":"+val[1].get()+":00"
                        break
            indicator["background"] = "lawngreen"

        def do_off(event):
            """do_off docs"""
            caller = event.widget.winfo_parent()
            temp_dict = self.alarm_time.copy()
            if indicator["background"] == "lawngreen":
                for key, val in temp_dict.items():
                    if caller in key.winfo_parent():
                        del self.alarm_time[key]
            indicator["background"] = "red"

        alarm_frame = Frame(window_to_place_in,
                            width=20,
                            highlightthickness=1,
                            highlightbackground="black")

        plan_label = Label(alarm_frame, text=""+str(frame_id)[6], font=13)
        plan_label.grid(column=0, columnspan=4, row=0)

        on_off = StringVar()

        on_r_button = Radiobutton(alarm_frame,
                                  text="Вкл",
                                  variable=on_off,
                                  value="lawngreen",
                                  indicatoron=False)
        on_r_button.grid(column=4, row=0, sticky="E", padx=39)
        on_r_button.bind("<Button-1>", do_on)

        off_r_button = Radiobutton(alarm_frame,
                                   text="Выкл",
                                   variable=on_off,
                                   value="red",
                                   indicatoron=False)
        off_r_button.grid(column=4, row=0, sticky="E")
        off_r_button.bind("<Button-1>", do_off)

        indicator = Label(alarm_frame, background="red", width=2)
        indicator.grid(column=4, row=0, sticky="W")

        self.add_alarm(alarm_frame)
        self.add_alarm(alarm_frame)
        self.add_alarm(alarm_frame)
        self.add_alarm(alarm_frame)

        alarm_frame.grid(column=col_position, row=row_position, padx=2, pady=2)

    def add_alarm(self, frame):
        """add_alarm docs"""
        hour_input = Entry(frame, width=2)
        hour_input.insert(0, "00")
        hour_input.bind("<Any-KeyRelease>", self.scan_entry)
        hour_input.bind("<FocusOut>", self.check_hour)
        hour_input.grid(column=0, row=len(self.alarms)+1, pady=2)

        double_dot = Label(frame, text=":")
        double_dot.grid(column=1, row=len(self.alarms)+1)

        minute_input = Entry(frame, width=2)
        minute_input.insert(0, "00")
        minute_input.bind("<Any-Key>", self.scan_entry)
        minute_input.bind("<FocusOut>", self.check_minute)
        minute_input.grid(column=2, row=len(self.alarms)+1, pady=2)

        sound_icon = PhotoImage(file="images/speaker.gif")
        test_sound = Button(frame, image=sound_icon, name=str(frame_id)+str(len(self.alarms)))
        test_sound.image = sound_icon
        test_sound.grid(column=3, row=len(self.alarms)+1, padx=5, pady=5)
        test_sound.bind("<Button-1>", self.play_sound)

        sound = ttk.Combobox(frame, values=SOUNDS_LIST, state="readonly", width=10)
        sound.grid(column=4, row=len(self.alarms)+1)

        self.alarms[len(self.alarms)+1] = [hour_input, minute_input, test_sound, sound]

    def check_hour(self, event):
        """check_hour docs"""
        caller = event.widget
        if not caller.get():
            caller.insert(0, "00")
        elif int(caller.get()) > 23:
            self.clean(event)
            caller.insert(0, "23")
        if len(caller.get()) < 2:
            caller.insert(0, "0")

    def check_minute(self, event):
        """check_minute docs"""
        caller = event.widget
        if not caller.get():
            caller.insert(0, "00")
        if int(caller.get()) > 59:
            self.clean(event)
            caller.insert(0, "59")
        if len(caller.get()) < 2:
            caller.insert(0, "0")

    def scan_entry(self, event):
        """scan_entry docs"""
        caller = event.widget
        count_char = len(caller.get())
        if not caller.get().isdigit():
            caller.delete(caller.index(END)-1)
        if count_char > 2:
            caller.delete(caller.index(END)-1)

    def clean(self, event):
        """clean docs"""
        caller = event.widget
        caller.delete("0", "end")

    def play_sound(self, event):
        """play_sound docs"""
        caller = event.widget
        for row_num, row_widgets in self.alarms.items():
            if caller in row_widgets:
                combobox = row_widgets[3]
                sound_path = os.path.join(SOUNDS_DIR, combobox.get())
                sound = wave.open(sound_path, 'rb')

                def player_callback(in_data, frame_count, time_info, status):
                    data = sound.readframes(frame_count)
                    return data, pyaudio.paContinue

                stream = player.open(
                        format=player.get_format_from_width(
                                sound.getsampwidth()),
                        channels=sound.getnchannels(),
                        rate=sound.getframerate(),
                        output=True,
                        stream_callback=player_callback,
                )
                stream.start_stream()


def alarm_info():
    """alarm_info docs"""
    logo = PhotoImage(file="images/logo.gif")
    show_message = Toplevel(root, takefocus=True)
    show_message.title("!")
    screen_size_x = str(int(show_message.winfo_screenwidth()/2)-50)
    screen_size_y = str(int(show_message.winfo_screenheight()/2)-60)
    message = Label(
        show_message,
        compound=LEFT,
        text=_message.get(),
        background="white",
        image=logo,
        font=18)
    message.image = logo
    message.pack()
    widget_size_x = str(len(_message.get())+70+logo.width())
    widget_size_y = str(logo.height()+40)
    ok_button = Button(show_message, text="OK", command=show_message.destroy)
    ok_button.pack(pady=5)
    ok_button.focus_set()
    show_message.geometry(widget_size_x + "x" +
                          widget_size_y + "+" +
                          str(screen_size_x)[:-2] + "+" +
                          str(screen_size_y)[:-2])
    show_message.lift()
    show_message.wm_attributes('-topmost', 1)


def info_on(event):
    """info_on docs"""
    message_indicator['background'] = 'lawngreen'


def info_off(event):
    """info_iff docs"""
    message_indicator['background'] = 'red'


def update_time():
    """update_time docs"""
    clock.after(1000, update_time)
    clock['text'] = time.strftime('%H:%M:%S')
    if _clock_window:
        _clock_window.wm_attributes('-topmost', 1)
    if alarm_object.alarm_time:
        for k, v in alarm_object.alarm_time.items():
            print(alarm_object)
            if v == clock['text']:
                sound_path = os.path.join(SOUNDS_DIR, k.get())
                play_sound(sound_path)
                '''
                sound = wave.open(sound_path, 'rb')

                def player_callback(in_data, frame_count, time_info, status):
                    data = sound.readframes(frame_count)
                    return data, pyaudio.paContinue

                stream = player.open(
                        format=player.get_format_from_width(
                                sound.getsampwidth()),
                        channels=sound.getnchannels(),
                        rate=sound.getframerate(),
                        output=True,
                        stream_callback=player_callback,
                )
                stream.start_stream()
                '''
                if message_indicator['background'] == 'lawngreen':
                    alarm_info()


def play_sound(sound_path):
    sound = wave.open(sound_path, 'rb')

    def player_callback(in_data, frame_count, time_info, status):
        data = sound.readframes(frame_count)
        return data, pyaudio.paContinue

    stream = player.open(
        format=player.get_format_from_width(
            sound.getsampwidth()),
        channels=sound.getnchannels(),
        rate=sound.getframerate(),
        output=True,
        stream_callback=player_callback,
    )
    stream.start_stream()


def add_clock_window():
    """add_clock_window docs"""
    global _clock_window

    def update_time_widget():
        """update_time_widget docs"""
        clock_widget.after(1000, update_time_widget)
        clock_widget['text'] = time.strftime('%H:%M')

    def close_clock(event):
        """close_clock docs"""
        global _clock_window
        _clock_on_off.set(0)
        _clock_window.destroy()
        _clock_window = None
        clock_indicator['background'] = 'red'

    def start_move(event):
        """start_move docs"""
        _clock_window.x = event.x
        _clock_window.y = event.y

    def stop_move(event):
        """stop_move docs"""
        _clock_window.x = None
        _clock_window.y = None

    def on_motion(event):
        """on_motion docs"""
        delta_x = event.x - _clock_window.x
        delta_y = event.y - _clock_window.y
        res_x = _clock_window.winfo_x() + delta_x
        res_y = _clock_window.winfo_y() + delta_y
        _clock_window.geometry("+"+str(res_x)+"+"+str(res_y))

    if not _clock_window:
        _clock_window = Toplevel(root, background='white')
        _clock_window.wm_attributes('-topmost', 1)
        _clock_window.overrideredirect(True)
        _clock_window.bind("<Double-Button-1>", close_clock)
        _clock_window.bind("<ButtonPress-1>", start_move)
        _clock_window.bind("<B1-Motion>", on_motion)
        screen_width = (_clock_window.winfo_screenwidth()/2) - 80
        screen_height = _clock_window.winfo_screenheight() - 30
        _clock_window.geometry("160x30"+"+"+str(screen_width)[:-2]+"+"+str(screen_height))

        clock_widget = Label(_clock_window,
                             text=time.strftime('%H:%M'),
                             font=('Arial', 18),
                             background='white')
        clock_widget.pack(side=RIGHT)
        clock_widget.after_idle(update_time_widget)

        clock_date = Label(_clock_window,
                           text=time.strftime('%d.%m.%Y'),
                           font=('Arial', 13),
                           background='white')
        clock_date.pack(side=RIGHT)


def clock_on(event):
    """clock_on docs"""
    add_clock_window()
    clock_indicator['background'] = 'lawngreen'


def clock_off(event):
    """clock_off docs"""
    global _clock_window
    if _clock_window:
        _clock_window.destroy()
        _clock_window = None
    clock_indicator['background'] = 'red'


def add_message(event):
    """add_message docs"""
    global _edit_message

    def send_text(event):
        """send_text docs"""
        global _edit_message
        _message = message.get()
        _edit_message.destroy()
        _edit_message = None

    def close_cross():
        """close_cross docs"""
        global _edit_message
        _message = message.get()
        _edit_message.destroy()
        _edit_message = None

    if not _edit_message:
        _edit_message = Toplevel(root)
        _edit_message.resizable(width=FALSE, height=FALSE)
        _edit_message.bind("<Alt-F4>", send_text)
        _edit_message.protocol("WM_DELETE_WINDOW", close_cross)
        ask_enter = Label(_edit_message, text="Введите текст")
        ask_enter.pack()
        message = Entry(_edit_message, textvariable=_message)
        message.bind("<Return>", send_text)
        message.pack()
        message.focus_set()
        ok_button = Button(_edit_message, text="Ok")
        ok_button.bind("<Button-1>", send_text)
        ok_button.pack()

        frame_width = 124
        frame_height = 66
        _edit_message.geometry(str(frame_width)+'x'+str(frame_height)+'+' +
                               str((root.winfo_screenwidth()/2) -
                                   frame_width/2)[:-2] + "+" +
                               str((root.winfo_screenheight()/2) -
                                   frame_height/2)[:-2])


def read_cfg():
    """read_cfg docs"""
    config = configparser.ConfigParser()
    config.readfp(open('config.cfg'))
    for alarm in config.items('AlarmsCfg'):
        hour_minute_sound = ast.literal_eval(alarm[1])
        alarm_object.alarms[int(alarm[0])][0].delete(0, END)
        alarm_object.alarms[int(alarm[0])][0].insert(0, hour_minute_sound[0])
        alarm_object.alarms[int(alarm[0])][1].delete(0, END)
        alarm_object.alarms[int(alarm[0])][1].insert(0, hour_minute_sound[1])
        alarm_object.alarms[int(alarm[0])][3].current(
            alarm_object.alarms[int(alarm[0])][3]['values'].index(hour_minute_sound[2]))


def write_cfg():
    """write_cfg docs"""
    config = configparser.ConfigParser()
    config.add_section('AlarmsCfg')
    for alarm_num in range(1, len(alarm_object.alarms)+1):
        config.set('AlarmsCfg', str(alarm_num),
                   str([alarm_object.alarms[alarm_num][0].get(),
                        alarm_object.alarms[alarm_num][1].get(),
                        alarm_object.alarms[alarm_num][3].get()]))
    with open('config.cfg', 'w') as cfg_file:
        config.write(cfg_file)


def close():
    """close docs"""
    write_cfg()
    player.terminate()
    root.destroy()

if __name__ == '__main__':
    root = Tk()
    root.geometry(str(ROOT_WIDTH)+'x'+str(ROOT_HEIGHT)+'+' +
                  str((root.winfo_screenwidth()/2)-ROOT_WIDTH/2)[:-2]+"+" +
                  str((root.winfo_screenheight()/2)-ROOT_HEIGHT/2)[:-2])
    root.resizable(width=FALSE, height=FALSE)
    root.title('Time')
    icon = Image('photo', file=(os.path.join(BASE_DIR, 'images/icon.gif')))
    root.tk.call('wm', 'iconphoto', root._w, icon)

    player = pyaudio.PyAudio()

    _edit_message = None
    _clock_window = None

    frame_id = count(0)

    _on_off_message = StringVar()

    _message = StringVar()
    _message.set("Перерыв")

    _clock_on_off = IntVar()

    alarm_object = AlarmClock()
    alarm_object.make_frame(root, 0, 0)
    alarm_object.make_frame(root, 0, 1)
    alarm_object.make_frame(root, 1, 0)
    alarm_object.make_frame(root, 1, 1)
    alarm_object.make_frame(root, 2, 0)
    alarm_object.make_frame(root, 2, 1)

    # _________________________________________
    message_frame = Frame(root)
    message_frame.grid(column=0, row=3, ipadx=5)

    off_message_button = Radiobutton(message_frame,
                                     text="Выкл",
                                     variable=_on_off_message,
                                     value='red',
                                     indicatoron=False)
    off_message_button.bind("<Button-1>", info_off)
    off_message_button.pack(side=RIGHT)

    on_message_button = Radiobutton(message_frame,
                                    text="Вкл",
                                    variable=_on_off_message,
                                    value='lawngreen',
                                    indicatoron=False)
    on_message_button.bind("<Button-1>", info_on)
    on_message_button.pack(side=RIGHT, padx=(10, 0))

    message_indicator = Label(message_frame, background="red", width=2)
    message_indicator.pack(side=RIGHT, padx=(20, 10), pady=10)

    message_text_button = Button(message_frame, text="Текст")
    message_text_button.bind("<Button-1>", add_message)
    message_text_button.pack(side=RIGHT)

    clock_frame = Frame(root)
    clock_frame.grid(column=1, row=3, ipadx=7)

    off_clock_button = Radiobutton(clock_frame,
                                   text="Выкл",
                                   variable=_clock_on_off,
                                   value=1,
                                   indicatoron=False)
    off_clock_button.bind("<Button-1>", clock_off)
    off_clock_button.pack(side=RIGHT)

    on_clock_button = Radiobutton(clock_frame,
                                  text="Вкл",
                                  variable=_clock_on_off,
                                  value=2,
                                  indicatoron=False)
    on_clock_button.bind("<Button-1>", clock_on)
    on_clock_button.pack(side=RIGHT, padx=(10, 0))

    clock_indicator = Label(clock_frame, background="red", width=2)
    clock_indicator.pack(side=RIGHT, padx=10, pady=10)

    clock = Label(clock_frame, text="time")
    clock.after_idle(update_time)
    clock.pack(side=RIGHT)

    # DEBUGBUTTON = Button(clock_frame, text="DEBUG", command=alarm_info)
    # DEBUGBUTTON.grid(column=0, row=2)
    # _____________________________________________

    read_cfg()

    root.protocol("<Alt-F4>", close)
    root.protocol("WM_DELETE_WINDOW", close)
    root.mainloop()
