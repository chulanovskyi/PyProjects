from tkinter import *
from tkinter.font import nametofont
import tkinter.ttk as ttk
import os
import ast
import time
import wave
import configparser
import pyaudio


if os.name == "posix":
    ROOT_WIDTH = 397
    ROOT_HEIGHT = 507
else:
    ROOT_WIDTH = 372
    ROOT_HEIGHT = 507

BASE_DIR = os.path.abspath(os.path.curdir)
SOUNDS_DIR = os.path.join(BASE_DIR, "soundBox/")
SOUNDS_LIST = [''] + os.listdir("soundBox")

OFF = "red"
ON = "lawngreen"


class AlarmClock:
    """AlarmClock docs"""
    plan_counter = 0
    # alarms = {}
    # alarm_time = {}

    def __init__(self):
        """
        alarms - row_num: [hh_widget, mm_widget, play_widget, combobox_widget]
        alarm_time - combo_widget: 'hh:mm:00'
        """
        self.alarms = {}
        self.alarm_time = {}

    @staticmethod
    def get_frame_counter():
        """get_frame_counter docs"""
        return AlarmClock.plan_counter

    def make_frame(self, window_to_place_in, row_position, col_position):
        """make_frame docs"""
        AlarmClock.plan_counter += 1

        def do_on(event):
            """do_on docs"""
            caller = event.widget.winfo_parent()
            if indicator["background"] == OFF:
                for row, widgets in self.alarms.items():
                    for item in widgets:
                        is_widget_parent = caller == item.winfo_parent()
                        is_entry_widget = item.winfo_class() == "Entry"
                        if is_widget_parent and is_entry_widget:
                            hour, minute = widgets[0].get(), widgets[1].get()
                            self.alarm_time[widgets[3]] = "{h}:{m}:00".format(
                                    h=hour,
                                    m=minute)
            indicator["background"] = ON

        def do_off(event):
            """do_off docs"""
            caller = event.widget.winfo_parent()
            temp_dict = self.alarm_time.copy()
            if indicator["background"] == ON:
                for row, widgets in temp_dict.items():
                    if caller == row.winfo_parent():
                        del self.alarm_time[row]
            indicator["background"] = OFF

        alarm_frame = Frame(window_to_place_in,
                            highlightthickness=1,
                            highlightbackground="black")

        plan_label = Label(alarm_frame, text=str(self.plan_counter), font=13)
        plan_label.grid(column=0, columnspan=4, row=0)

        on_off = StringVar()

        on_r_button = Radiobutton(alarm_frame,
                                  text="Вкл",
                                  variable=on_off,
                                  value=ON,
                                  indicatoron=False)
        on_r_button.grid(column=4, row=0, sticky="E", padx=39)
        on_r_button.bind("<Button-1>", do_on)

        off_r_button = Radiobutton(alarm_frame,
                                   text="Выкл",
                                   variable=on_off,
                                   value=OFF,
                                   indicatoron=False)
        off_r_button.grid(column=4, row=0, sticky="E")
        off_r_button.bind("<Button-1>", do_off)

        indicator = Label(alarm_frame, background=OFF, width=2)
        indicator.grid(column=4, row=0, sticky="W")

        self.add_alarm(alarm_frame)
        self.add_alarm(alarm_frame)
        self.add_alarm(alarm_frame)
        self.add_alarm(alarm_frame)
        alarm_frame.grid(column=col_position, row=row_position, padx=2, pady=2)

    def add_alarm(self, frame):
        row_num = len(self.alarms)+1
        """add_alarm docs"""
        hour_input = Entry(frame, width=2)
        hour_input.insert(0, "00")
        hour_input.bind("<Any-KeyRelease>", self.scan_entry)
        hour_input.bind("<FocusOut>", self.check_hour)
        hour_input.grid(column=0, row=row_num, pady=2)

        double_dot = Label(frame, text=":")
        double_dot.grid(column=1, row=row_num)

        minute_input = Entry(frame, width=2)
        minute_input.insert(0, "00")
        minute_input.bind("<Any-Key>", self.scan_entry)
        minute_input.bind("<FocusOut>", self.check_minute)
        minute_input.grid(column=2, row=row_num, pady=2)

        sound_icon = PhotoImage(file="images/speaker.gif")
        test_sound = Button(frame, image=sound_icon)
        test_sound.image = sound_icon
        test_sound.grid(column=3, row=row_num, padx=5, pady=5)
        test_sound.bind("<Button-1>", self.play_sound)

        sound = ttk.Combobox(frame,
                             values=SOUNDS_LIST,
                             state="readonly",
                             width=10)
        sound.grid(column=4, row=row_num)

        self.alarms[row_num] = [hour_input, minute_input, test_sound, sound]

    def check_hour(self, event):
        """check_hour docs"""
        caller = event.widget
        if not caller.get():
            caller.insert(0, "00")
        elif int(caller.get()) > 23:
            self.clean(caller)
            caller.insert(0, "23")
        if len(caller.get()) < 2:
            caller.insert(0, "0")

    def check_minute(self, event):
        """check_minute docs"""
        caller = event.widget
        if not caller.get():
            caller.insert(0, "00")
        if int(caller.get()) > 59:
            self.clean(caller)
            caller.insert(0, "59")
        if len(caller.get()) < 2:
            caller.insert(0, "0")

    @staticmethod
    def scan_entry(event):
        """scan_entry docs"""
        caller = event.widget
        count_char = len(caller.get())
        if not caller.get().isdigit():
            caller.delete(caller.index(END)-1)
        if count_char > 2:
            caller.delete(caller.index(END)-1)

    @staticmethod
    def clean(widget):
        """clean docs"""
        widget.delete("0", "end")

    def play_sound(self, event):
        """play_sound docs"""
        caller = event.widget
        for row_num, row_widgets in self.alarms.items():
            if caller in row_widgets:
                sound_name = row_widgets[3].get()
                if not sound_name:
                    return
                sound_path = os.path.join(SOUNDS_DIR, sound_name)
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
    screen_x_center = str(int(show_message.winfo_screenwidth()/2)-50)
    screen_y_center = str(int(show_message.winfo_screenheight()/2)-60)
    screen_center = screen_x_center + "+" + screen_y_center
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
    widget_size = widget_size_x + "x" + widget_size_y
    ok_button = Button(show_message, text="OK", command=show_message.destroy)
    ok_button.pack(pady=5)
    ok_button.focus_set()
    show_message.geometry(widget_size + "+" + screen_center)
    show_message.lift()
    show_message.wm_attributes('-topmost', 1)


def info_on(event):
    """info_on docs"""
    message_indicator['background'] = ON


def info_off(event):
    """info_iff docs"""
    message_indicator['background'] = OFF


def update_time():
    """ 
    update_time docs
    alarm_time - combo_widget: 'hh:mm:00'
    """
    clock.after(1000, update_time)
    clock['text'] = time.strftime('%H:%M:%S')
    if _clock_window:
        _clock_window.wm_attributes('-topmost', 1)
    if alarm_object.alarm_time:
        for combobox, alarm in alarm_object.alarm_time.items():
            if alarm == clock['text']:
                if message_indicator['background'] == ON:
                    alarm_info()
                sound_name = combobox.get()
                if not sound_name:
                    return
                sound_path = os.path.join(SOUNDS_DIR, sound_name)
                play_sound(sound_path)


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
    global _clock_window
    """add_clock_window docs"""
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
        clock_indicator['background'] = OFF

    def start_move(event):
        """start_move docs"""
        global _clock_window
        _clock_window.x = event.x
        _clock_window.y = event.y

    def on_motion(event):
        """on_motion docs"""
        global _clock_window
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
        clock_size = "160x30"
        screen_width = int((_clock_window.winfo_screenwidth()/2) - 80)
        screen_height = _clock_window.winfo_screenheight() - 30
        _clock_window.geometry(clock_size + "+" +
                               str(screen_width) + "+" + str(screen_height))

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
    clock_indicator['background'] = ON


def clock_off(event):
    """clock_off docs"""
    global _clock_window
    if _clock_window:
        _clock_window.destroy()
        _clock_window = None
    clock_indicator['background'] = OFF


def add_message(event):
    """add_message docs"""
    global _edit_message

    def send_text(event=None):
        """send_text docs"""
        global _edit_message
        _edit_message.destroy()
        _edit_message = None

    if not _edit_message:
        _edit_message = Toplevel(root)
        _edit_message.resizable(width=FALSE, height=FALSE)
        _edit_message.bind("<Alt-F4>", send_text)
        _edit_message.protocol("WM_DELETE_WINDOW", send_text)

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
        frame_size = "124x66"
        x_center = str(int((root.winfo_screenwidth()/2) - frame_width/2))
        y_center = str(int((root.winfo_screenheight()/2) - frame_height/2))
        screen_center = x_center + "+" + y_center
        _edit_message.geometry(frame_size + '+' + screen_center)


def read_cfg():
    """read_cfg docs"""
    config = configparser.ConfigParser()
    config.read_file(open('config.cfg'))
    for row, alarm in config.items('AlarmsCfg'):
        row = int(row)
        hour, minute, sound = ast.literal_eval(alarm)
        hour_widget = alarm_object.alarms[row][0]
        hour_widget.delete(0, END)
        hour_widget.insert(0, hour)
        minute_widget = alarm_object.alarms[row][1]
        minute_widget.delete(0, END)
        minute_widget.insert(0, minute)
        combo_widget = alarm_object.alarms[row][3]
        combo_widget.current(combo_widget['values'].index(sound))


def write_cfg():
    """write_cfg docs"""
    config = configparser.ConfigParser()
    config.add_section('AlarmsCfg')
    for row in range(1, len(alarm_object.alarms)+1):
        hour = alarm_object.alarms[row][0].get()
        minute = alarm_object.alarms[row][1].get()
        sound = alarm_object.alarms[row][3].get()
        config.set('AlarmsCfg', str(row), str([hour, minute, sound]))
    with open('config.cfg', 'w') as cfg_file:
        config.write(cfg_file)


def close_root():
    """close_root docs"""
    write_cfg()
    player.terminate()
    root.destroy()

if __name__ == '__main__':
    root = Tk()
    screen_size_x = str(int((root.winfo_screenwidth() / 2) - ROOT_WIDTH / 2))
    screen_size_y = str(int((root.winfo_screenheight() / 2) - ROOT_HEIGHT / 2))
    screen_size = str(ROOT_WIDTH)+'x'+str(ROOT_HEIGHT)
    root.title('Time')
    root.geometry(screen_size + '+' + screen_size_x + "+" + screen_size_y)
    root.resizable(width=FALSE, height=FALSE)
    icon = Image('photo', file=(os.path.join(BASE_DIR, 'images/icon.gif')))
    root.tk.call('wm', 'iconphoto', root._w, icon)

    default_font = nametofont("TkDefaultFont")
    default_font.configure(size=9)
    root.option_add("*Font", default_font)

    player = pyaudio.PyAudio()

    _edit_message = None
    _clock_window = None

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
                                     value=OFF,
                                     indicatoron=False)
    off_message_button.bind("<Button-1>", info_off)
    off_message_button.pack(side=RIGHT)

    on_message_button = Radiobutton(message_frame,
                                    text="Вкл",
                                    variable=_on_off_message,
                                    value=ON,
                                    indicatoron=False)
    on_message_button.bind("<Button-1>", info_on)
    on_message_button.pack(side=RIGHT, padx=(10, 0))

    message_indicator = Label(message_frame, background=OFF, width=2)
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

    clock_indicator = Label(clock_frame, background=OFF, width=2)
    clock_indicator.pack(side=RIGHT, padx=10, pady=10)

    clock = Label(clock_frame, text="time")
    clock.after_idle(update_time)
    clock.pack(side=RIGHT)

    # DEBUG_BUTTON = Button(clock_frame, text="?", command=alarm_info)
    # DEBUG_BUTTON.pack(side=BOTTOM)
    # _____________________________________________

    read_cfg()

    root.protocol("<Alt-F4>", close_root)
    root.protocol("WM_DELETE_WINDOW", close_root)
    root.mainloop()
