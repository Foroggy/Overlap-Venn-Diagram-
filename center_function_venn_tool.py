# center_function_venn_tool.py
# This script creates two Venn diagrams:
# (1) Center-based overlaps by surface function.
# (2) Function-based overlaps by center participation.

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib_venn import venn3
import uuid
import tkinter as tk
from tkinter import ttk

def collect_data():
    """Open a GUI table for user to input center and surface functions."""
    def submit():
        rows = []
        for i in range(len(entries)):
            center = entries[i][0].get().strip()
            function = entries[i][1].get().strip()
            if center or function:
                rows.append([center, function])
        root.destroy()
        df = pd.DataFrame(rows, columns=['Center', 'Surface Function'])
        df['Surface Function'] = df['Surface Function'].str.split(',\s*')
        df = df.explode('Surface Function')
        df['Surface Function'] = df['Surface Function'].str.strip()
        return df[df['Surface Function'] != '']

    root = tk.Tk()
    root.title("Enter Center and Surface Function Data")
    instructions = tk.Label(root, text="Enter Center and Surface Functions (comma-separated if multiple):")
    instructions.grid(row=0, column=0, columnspan=3, pady=10)

    entries = []
    for i in range(15):  # default 15 rows
        center_entry = ttk.Entry(root, width=20)
        function_entry = ttk.Entry(root, width=50)
        center_entry.grid(row=i + 1, column=0, padx=5, pady=2)
        function_entry.grid(row=i + 1, column=1, padx=5, pady=2)
        entries.append((center_entry, function_entry))

    submit_btn = tk.Button(root, text="Submit", command=submit)
    submit_btn.grid(row=16, column=0, columnspan=2, pady=10)

    root.mainloop()
    return submit()

def make_center_venn(df):
    """Create Venn diagram of centers by surface function overlap."""
    center_sets = df.groupby('Center')['Surface Function'].apply(set).to_dict()
    centers = list(center_sets.keys())[:3]  # Limit to 3 for Venn3
    sets = [center_sets[c] for c in centers]

    plt.figure(figsize=(8, 6))
    venn3(sets, set_labels=centers)
    plt.title("Centers by Shared Surface Functions")
    filename = f"center_venn_{uuid.uuid4().hex}.png"
    plt.savefig(filename)
    print(f"Saved: {filename}")
    plt.show()

def make_function_venn(df):
    """Create Venn diagram of surface functions by participating centers."""
    func_sets = df.groupby('Surface Function')['Center'].apply(set).to_dict()
    functions = list(func_sets.keys())[:3]  # Limit to 3 for Venn3
    sets = [func_sets[f] for f in functions]

    plt.figure(figsize=(8, 6))
    venn3(sets, set_labels=functions)
    plt.title("Surface Functions by Participating Centers")
    filename = f"function_venn_{uuid.uuid4().hex}.png"
    plt.savefig(filename)
    print(f"Saved: {filename}")
    plt.show()

def main():
    print("Fill out the input table to generate Venn diagrams.")
    df_clean = collect_data()
    make_center_venn(df_clean)
    make_function_venn(df_clean)

if __name__ == '__main__':
    main()
