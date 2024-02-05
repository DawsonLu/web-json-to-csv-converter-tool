import requests
import json
import socket
from tkinter import messagebox


def is_connected_to_corporate_network(domain_name):
    try:
        # Attempt to resolve the corporate domain name
        socket.gethostbyname(domain_name)
        return True
    except socket.gaierror:
        # The domain name could not be resolved
        return False


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
        messagebox.showinfo(
            "Success", f"JSON data successfully saved to {filename}")
    except Exception as e:
        messagebox.showerror(
            "Error", f"An error occurred while saving JSON: {e}")