import tkinter
from tkinter import ttk, messagebox
import json
import multiprocessing
import time
import notifier
import datetime
import subprocess

frequency_mapping = {
    "1 minute": 1,
    "2 minutes": 2,
    "5 minutes": 5,
    "10 minutes": 10,
    "15 minutes": 15,
    "30 minutes": 30,
    "1 hour": 60,
    "2 hours": 120,
    "3 hours": 180,
    "6 hours": 360,
    "12 hours": 720,
    "Never": float('inf')
}

service_process = None


def start_service():
    messagebox.showinfo("Info", "Service started successfully.")


def stop_service():
    messagebox.showinfo("Info", "Service stopped successfully.")


def validate_data():
    terms_status = terms_status_var.get()
    firstname = first_name_entry.get().strip()
    lastname = last_name_entry.get().strip()
    start_hour = start_hour_spinbox.get().strip()
    start_minute = start_minute_spinbox.get().strip()
    end_hour = end_hour_spinbox.get().strip()
    end_minute = end_minute_spinbox.get().strip()
    frequency = frequency_combobox.get().strip()

    if (not firstname or not lastname or not start_hour or not start_minute
            or not end_hour or not end_minute or not frequency):
        messagebox.showwarning("Warning", "All fields must be completed.")
        return

    try:
        start_hour_int = int(start_hour)
        start_minute_int = int(start_minute)
        end_hour_int = int(end_hour)
        end_minute_int = int(end_minute)
        if (not (0 <= start_hour_int <= 23) or not (0 <= start_minute_int <= 59) or not (0 <= end_hour_int <= 23) or
                not (0 <= end_minute_int <= 59)):
            raise ValueError()
    except ValueError:
        messagebox.showwarning("Warning", "Invalid time input.")
        return

    start_time = start_hour_int * 60 + start_minute_int
    end_time = end_hour_int * 60 + end_minute_int

    if end_time < start_time:
        # Handle overnight intervals (e.g., 22:00 to 06:00)
        interval_minutes = (24 * 60 - start_time) + end_time
    else:
        interval_minutes = end_time - start_time

    frequency_minutes = frequency_mapping.get(frequency, float('inf'))

    if interval_minutes < frequency_minutes:
        messagebox.showwarning(
            "Warning",
            "The time interval is shorter than the selected frequency. You will not receive any notifications."
        )
        return

    if terms_status == "Not Accepted":
        messagebox.showwarning("Warning", "You must accept the terms and conditions.")
    else:
        preferences = {
            "terms_status": terms_status,
            "firstname": firstname,
            "lastname": lastname,
            "start_hour": start_hour,
            "start_minute": start_minute,
            "end_hour": end_hour,
            "end_minute": end_minute,
            "frequency": frequency
        }
        with open('user_preferences.json', 'w') as f:
            json.dump(preferences, f, indent=4)
        messagebox.showinfo("Info", "Settings saved successfully.")


if __name__ == '__main__':
    window = tkinter.Tk()
    window.title("Data Entry Form")

    frame = tkinter.Frame(window)
    frame.pack()  # pack, grid or place (geometry managers/ layout managers)

    # saving user info
    user_info_frame = tkinter.LabelFrame(frame, text="User information")
    user_info_frame.grid(row=0, column=0, sticky="news", padx=20, pady=10)

    first_name_label = tkinter.Label(user_info_frame, text="First Name:")
    first_name_label.grid(row=0, column=0)
    last_name_label = tkinter.Label(user_info_frame, text="Last Name:")
    last_name_label.grid(row=0, column=1)

    first_name_entry = tkinter.Entry(user_info_frame)
    last_name_entry = tkinter.Entry(user_info_frame)
    first_name_entry.grid(row=1, column=0)
    last_name_entry.grid(row=1, column=1)

    for widget in user_info_frame.winfo_children():
        widget.grid_configure(padx=35, pady=5)

    # notification preferences - time interval frame
    time_interval_frame = tkinter.LabelFrame(frame, text="Notification Time Interval")
    time_interval_frame.grid(row=1, column=0, sticky="news", padx=20, pady=10)

    from_label = tkinter.Label(time_interval_frame, text="From")
    from_label.grid(row=0, column=0)
    start_hour_spinbox = tkinter.Spinbox(time_interval_frame, from_=0, to=23)
    start_hour_spinbox.grid(row=0, column=1)
    colon_label = tkinter.Label(time_interval_frame, text=":")
    colon_label.grid(row=0, column=2)
    start_minute_spinbox = tkinter.Spinbox(time_interval_frame, from_=0, to=59)
    start_minute_spinbox.grid(row=0, column=3)

    to_label = tkinter.Label(time_interval_frame, text="To")
    to_label.grid(row=1, column=0)
    end_hour_spinbox = tkinter.Spinbox(time_interval_frame, from_=0, to=23)
    end_hour_spinbox.grid(row=1, column=1)
    colon_2_label = tkinter.Label(time_interval_frame, text=":")
    colon_2_label.grid(row=1, column=2)
    end_minute_spinbox = tkinter.Spinbox(time_interval_frame, from_=0, to=59)
    end_minute_spinbox.grid(row=1, column=3)

    for widget in time_interval_frame.winfo_children():
        widget.grid_configure(padx=10, pady=5)

    # notification preferences - frequency frame
    notification_frequency_frame = tkinter.LabelFrame(frame, text="Notification Frequency")
    notification_frequency_frame.grid(row=2, column=0, sticky="news", padx=20, pady=10)

    frequency_label = tkinter.Label(notification_frequency_frame, text="Frequency:")
    frequency_label.grid(row=0, column=0)
    frequency_combobox = ttk.Combobox(notification_frequency_frame, values=["1 minute", "2 minutes", "5 minutes",
                                                                            "10 minutes", "15 minutes",
                                                                            "30 minutes", "1 hour", "2 hours",
                                                                            "3 hours",
                                                                            "6 hours", "12 hours", "Never"],
                                      state="readonly")
    frequency_combobox.grid(row=0, column=1)

    for widget in notification_frequency_frame.winfo_children():
        widget.grid_configure(padx=10, pady=5)

    # accept terms
    terms_frame = tkinter.LabelFrame(frame, text="Terms & Conditions")
    terms_frame.grid(row=3, column=0, sticky="news", padx=20, pady=10)

    terms_status_var = tkinter.StringVar(value="Not Accepted")
    terms_check = tkinter.Checkbutton(terms_frame, text="I accept the terms and conditions.", variable=terms_status_var,
                                      onvalue="Accepted", offvalue="Not Accepted")
    terms_check.grid(row=0, column=0)

    # buttons
    save_button = tkinter.Button(frame, text="Save", command=validate_data)
    save_button.grid(row=4, column=0, sticky="news", padx=20, pady=10)

    start_button = tkinter.Button(frame, text="Start service", command=start_service)
    start_button.grid(row=5, column=0, sticky="news", padx=20, pady=10)

    stop_button = tkinter.Button(frame, text="Stop service", command=stop_service)
    stop_button.grid(row=6, column=0, sticky="news", padx=20, pady=10)

    window.mainloop()
