import wikipedia # type: ignore
import tkinter as tk
from tkinter import scrolledtext as st
import os
import subprocess
lang = 'RU'
def open_search_file():
    if os.path.isfile("previous_search.txt"):
        subprocess.run(['notepad.exe', 'previous_search.txt'])
    else:
        text_area.delete("1.0", tk.END)
        text_area.insert(tk.END, "previous_search.txt not found.")
def switch_language():
    global lang
    if lang == 'ru':
        lang = 'en'
        switch_button.config(text="ENG", bg="#e0e0e0", fg="#000000",)
    else:
        lang = 'ru'
        switch_button.config(text="RU", bg="#e0e0e0", fg="#000000",)
def search_wikipedia():
    query = entry.get()
    try:
        current_content = text_area.get("1.0", tk.END)
        if current_content.strip():
            with open("previous_search.txt", "w", encoding="utf-8") as file:
                file.write(current_content)
                file.close
        wikipedia.set_lang(lang)
        result = wikipedia.page(query)
        text_area.delete(1.0,tk.END)
        text_area.insert(tk.END, result.content)
    except wikipedia.exceptions.DisambiguationError as e:
        options = ", ".join(e.options)
        text_area.delete(1.0,tk.END)
        text_area.insert(tk.END, f"Please specify your question,there is some options: {options}")
    except wikipedia.exceptions.PageError:
        text_area.delete(1.0,tk.END)
        text_area.insert(tk.END, "Nothing was found on wikipedia.")
def on_closing():
    current_content = text_area.get("1.0", tk.END)
    if current_content.strip():
        with open("previous_search.txt", "w", encoding="utf-8") as file:
            file.write(current_content)
    root.destroy()
    file.close
root = tk.Tk()
root.title("WIKIPEDIA(made by xeon)")
root.geometry("1024x768")
root.configure(bg="#d1d1d1")
label = tk.Label(root, text="Enter request:\n(All your previous searchs saves in previous_search.txt)", bg=("#d1d1d1") , font=('Ink Free', 24))
label.pack(pady=10,)
entry = tk.Entry(root, width=50000, bg="#bfbfbf", fg="#000000", bd=0 , font=('Segoe Script', 12))
entry.pack(padx=10,pady=5)
switch_button = tk.Button(root, width=50000, text="RU", command=switch_language, bg="#e0e0e0", fg="#000000", bd=0,)
switch_button.pack(padx=10,pady=5)
search_button = tk.Button(root, text="Search", width=50000, command=search_wikipedia, bg="#e0e0e0", fg="#000000", bd=0)
search_button.pack(padx=10,pady=5)
open_file_button = tk.Button(root, text="Open file with previous searches",width=50000, command=open_search_file, bg="#e0e0e0", fg="#000000", bd=0,)
open_file_button.pack(padx=10,pady=5)
text_area = st.ScrolledText(root, width=10000, height=5000, bg="#b3b3b3", fg="Black", bd=0, font=('Segoe Script', 12))
text_area.pack(padx=10, pady=10)
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()