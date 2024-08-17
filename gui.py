import tkinter
from tkinter import ttk

window = tkinter.Tk()
window.title("Data Entry Form")

frame = tkinter.Frame(window)
frame.pack()  # pack, grid or place (geometry managers/ layout managers)

# saving user info
user_info_frame = tkinter.LabelFrame(frame, text="User information")
user_info_frame.grid(row=0, column=0, padx=20, pady=10)

first_name_label = tkinter.Label(user_info_frame, text="First Name:")
first_name_label.grid(row=0, column=0)
last_name_label = tkinter.Label(user_info_frame, text="Last Name:")
last_name_label.grid(row=0, column=1)

first_name_entry = tkinter.Entry(user_info_frame)
last_name_entry = tkinter.Entry(user_info_frame)
first_name_entry.grid(row=1, column=0)
last_name_entry.grid(row=1, column=1)

age_label = tkinter.Label(user_info_frame, text="Age:")
age_spinbox = tkinter.Spinbox(user_info_frame, from_=18, to=100)
age_label.grid(row=0, column=2)
age_spinbox.grid(row=1, column=2)

for widget in user_info_frame.winfo_children():
    widget.grid_configure(padx=10, pady=5)

# saving notification preferences
time_interval_frame = tkinter.LabelFrame(frame, text="Notification Time Interval")
time_interval_frame.grid(row=1, column=0, sticky="news", padx=20, pady=10)

from_label = tkinter.Label(time_interval_frame, text="From")
from_label.grid(row=0, column=0)
from_hour_spinbox = tkinter.Spinbox(time_interval_frame, from_=0, to=23)
from_hour_spinbox.grid(row=0, column=1)
colon_label = tkinter.Label(time_interval_frame, text=":")
colon_label.grid(row=0, column=2)
from_minute_spinbox = tkinter.Spinbox(time_interval_frame, from_=0, to=59)
from_minute_spinbox.grid(row=0, column=3)

to_label = tkinter.Label(time_interval_frame, text="To")
to_label.grid(row=1, column=0)
to_hour_spinbox = tkinter.Spinbox(time_interval_frame, from_=0, to=23)
to_hour_spinbox.grid(row=1, column=1)
colon_2_label = tkinter.Label(time_interval_frame, text=":")
colon_2_label.grid(row=1, column=2)
to_minute_spinbox = tkinter.Spinbox(time_interval_frame, from_=0, to=59)
to_minute_spinbox.grid(row=1, column=3)

for widget in time_interval_frame.winfo_children():
    widget.grid_configure(padx=10, pady=5)

# frequency frame
notification_frequency_frame = tkinter.LabelFrame(frame, text="Notification Frequency")
notification_frequency_frame.grid(row=2, column=0, sticky="news", padx=20, pady=10)

frequency_label = tkinter.Label(notification_frequency_frame, text="Frequency:")
frequency_label.grid(row=0, column=0)
frequency_combobox = ttk.Combobox(notification_frequency_frame, values=["5 minutes", "10 minutes", "15 minutes",
                                                                        "30 minutes", "1 hour", "2 hours", "3 hours",
                                                                        "6 hours", "12 hours", "Once a day", "Never"])
frequency_combobox.grid(row=0, column=1)

for widget in notification_frequency_frame.winfo_children():
    widget.grid_configure(padx=10, pady=5)

# accept terms
terms_frame = tkinter.LabelFrame(frame, text="Terms & Conditions")
terms_frame.grid(row=3, column=0, sticky="news", padx=20, pady=10)

terms_check = tkinter.Checkbutton(terms_frame, text="I accept the terms and conditions.")
terms_check.grid(row=0, column=0)

# button
button = tkinter.Button(frame, text="Enter data")
button.grid(row=4, column=0, sticky="news", padx=20, pady=10)

window.mainloop()
