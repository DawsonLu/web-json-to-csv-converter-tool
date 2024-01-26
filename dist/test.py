import requests
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox
import json

def fetch_and_parse_json(url):
    try:
        response = requests.get(url, verify=False)
        response.raise_for_status()  # Raises an error for bad status codes

        # Parse JSON
        data = response.json()
        print(data)
        return data
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        return None

def save_json(data, filename):
    try:
        with open(filename, 'w') as json_file:
            json.dump(data, json_file, indent=4)
        messagebox.showinfo("Success", f"JSON data successfully saved to {filename}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while saving JSON: {e}")

def flatten_json(y, parent_id=None):
    out = []
    
    def flatten(x, name='', parent_id=None):
        if type(x) is dict:
            for a in x:
                flatten(x[a], f'{name}{a}_', parent_id)
        elif type(x) is list:
            for i, a in enumerate(x):
                if type(a) is dict:
                    # Concatenate values within the nested dictionary
                    flattened_dict = {f"{name[:-1]}_{key}": value for key, value in a.items()}
                    out.append({**flattened_dict, 'parent_id': parent_id})
                else:
                    out.append({name[:-1]: a, 'parent_id': parent_id})
        else:
            out.append({name[:-1]: x, 'parent_id': parent_id})
    
    flatten(y, parent_id=parent_id)
    return out

def convert_to_csv(data, filename):
    try:
        flat_data = flatten_json(data)
        df = pd.DataFrame(flat_data)
        df.to_csv(filename, index=False)
        messagebox.showinfo("Success", f"Data successfully saved to {filename}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while converting to CSV: {e}")

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

# Set up the Tkinter window
window = tk.Tk()
window.title("JSON to CSV Converter")

# URL entry
url_label = tk.Label(window, text="Enter URL:")
url_label.pack()
url_entry = tk.Entry(window, width=50)
url_entry.pack()

# Convert button
convert_button = tk.Button(window, text="Convert to CSV", command=on_convert_clicked)
convert_button.pack()

# Run the application
window.mainloop()