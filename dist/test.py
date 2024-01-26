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

def flatten_json(y):
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], f'{name}{a}_')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, f'{name}{i}_')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(y)
    return out

def expand_nested_arrays(data, array_keys):
    expanded_data = []
    for entry in data:
        base_entry = {k: v for k, v in entry.items() if k not in array_keys}
        for key in array_keys:
            if key in entry and isinstance(entry[key], list):
                for item in entry[key]:
                    new_entry = base_entry.copy()
                    new_entry.update(flatten_json({key: item}))
                    expanded_data.append(new_entry)
            else:
                expanded_data.append(base_entry)
    return expanded_data

def convert_to_csv(data, filename):
    try:
        # Define keys that contain nested arrays
        array_keys = ['key_with_nested_array']  # Replace with your actual key(s)

        # Flatten data and expand nested arrays
        flat_data = [flatten_json(d) for d in data] if isinstance(data, list) else [flatten_json(data)]
        expanded_data = expand_nested_arrays(flat_data, array_keys)

        df = pd.DataFrame(expanded_data)
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

        # Ask user for location and filename for saving the JSON file
        json_file_path = filedialog.asksaveasfilename(defaultextension=".json",
                                                      filetypes=[("JSON Files", "*.json")])
        if json_file_path:
            save_json(data, json_file_path)


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