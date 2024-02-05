import pandas as pd
from tkinter import messagebox


def flatten_dict(d, parent_key='', sep='_'):
    """
    Recursively flattens a nested dictionary or dictionary containing lists.
    """
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            # If value is a dictionary, call recursively
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        elif isinstance(v, list):
            # If value is a list, add each item separately
            for i, item in enumerate(v):
                if isinstance(item, dict):
                    # If item in list is a dictionary, call recursively
                    items.extend(flatten_dict(
                        item, f"{new_key}{sep}{i}", sep=sep).items())
                else:
                    # If item is not a dictionary, add it directly
                    items.append((f"{new_key}{sep}{i}", item))
        else:
            items.append((new_key, v))
    return dict(items)


def flatten_json(y, parent_id=None):
    out = []

    def flatten(x, name='', parent_id=None):
        if type(x) is dict:
            for a in x:
                flatten(x[a], f'{name}{a}_', parent_id)
        elif type(x) is list:
            for i, a in enumerate(x):
                if type(a) is dict:
                    # Flatten the dictionary, including handling nested
                    # dictionaries and lists
                    flattened_dict = flatten_dict(a)
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
    except Exception as e:
        messagebox.showerror(
            "Error", f"An error occurred while converting to CSV: {e}")