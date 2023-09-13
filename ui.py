import tkinter as tk
import video_downloader

# Function to be called when the "Submit" button is clicked
def on_submit():
    # Get the values entered in the entry fields
    username = username_entry.get()
    password = password_entry.get()
    lectureCount = int(count_entry.get())
    startFrom = int(start_entry.get()) - 1     # to get index

    # Store the values in variables (you can perform any further processing here)
    # username.set(username_value)
    # password.set(password_value)
    # lectureCount.set(count_value)
    # startFrom.set(start_value)

    # backward iteration
    # 4, 3, 2, 1, 0 - and index 0 is the final vid we download
    while( startFrom - lectureCount >= 0):
        video_downloader.start(username, password, lectureCount, startFrom)
        startFrom -= lectureCount

# Create the main application window
root = tk.Tk()
root.title("Basic Tkinter Project")

# Variables to store the user inputs
username = tk.StringVar(value='as3928')
password = tk.StringVar(value='Pokemon^2468')
lectureCount = tk.IntVar(value = '5')
startFrom = tk.IntVar(value = '250')

# Label and Entry widget for username
username_label = tk.Label(root, text="Username:")
username_label.pack()
username_entry = tk.Entry(root, textvariable=username)
username_entry.pack()

# Label and Entry widget for password
password_label = tk.Label(root, text="Password:")
password_label.pack()
password_entry = tk.Entry(root, show="*", textvariable=password)
password_entry.pack()

# Label and Entry widget for lecture count
count_label = tk.Label(root, text="Lecture Count:")
count_label.pack()
count_entry = tk.Entry(root, textvariable=lectureCount)
count_entry.pack()

# Label and Entry widget for starting lecture
start_label = tk.Label(root, text="Start From:")
start_label.pack()
start_entry = tk.Entry(root, textvariable=startFrom)
start_entry.pack()

# Submit Button
submit_button = tk.Button(root, text="Submit", command=on_submit)
submit_button.pack()

# Start the Tkinter event loop
root.mainloop()

