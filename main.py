import tkinter as tk
from tkinter import filedialog, messagebox
from fetch_parse_json import fetch_and_parse_json
from convert_csv import convert_to_csv


def on_convert_clicked():
    url = url_entry.get()
    if not url:
        messagebox.showwarning("Warning", "Please enter a URL")
        return

    data = fetch_and_parse_json(url)
    if data is not None:
        # Ask user for location and filename for saving the CSV file
        csv_file_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                                     filetypes=[("CSV Files", "*.csv")])
        if csv_file_path:
            convert_to_csv(data, csv_file_path)


def on_right_click(event):
    try:
        # Display the popup menu
        popup_menu.tk_popup(event.x_root, event.y_root)
    finally:
        # Make sure to release the grab (Tkinter grab_release is done automatically when using tk_popup)
        popup_menu.grab_release()


def paste(event=None):
    try:
        text = window.selection_get(selection='CLIPBOARD')
        url_entry.insert('insert', text)
    except tk.TclError:
        pass  # Handle the exception if there's no text in the clipboard


# Set up the Tkinter window
window = tk.Tk()
window.title("JSON to CSV Converter")

# URL entry
url_label = tk.Label(window, text="Enter URL:")
url_label.pack()
url_entry = tk.Entry(window, width=50)
url_entry.pack()

# Create a popup menu
popup_menu = tk.Menu(window, tearoff=0)
popup_menu.add_command(label="Paste", command=lambda: paste())

url_entry.bind("<Button-3>", on_right_click)

# Convert button
convert_button = tk.Button(window, text="Convert to CSV", command=on_convert_clicked)
convert_button.pack()

# Run the application
window.mainloop()