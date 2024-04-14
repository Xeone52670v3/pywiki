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
def switch_language(event=None):
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
root = tk.Tk()
root.title("WIKIPEDIA(made by xeon)")
root.geometry("1024x768")
root.configure(bg="#d1d1d1")
root.bind('<Control-Alt_L>', switch_language)
root.bind('<Control-Alt_R>', switch_language)
label = tk.Label(root, text="Enter request:\n(All your previous searchs saves in previous_search.txt)\nAlso you can swap language by CTRL+2xALT", bg=("#d1d1d1") , font=('Ink Free', 24))
label.pack(padx=10,pady=10)
control_frame = tk.Frame(root, bg="#d1d1d1")
control_frame.pack(padx=10, pady=5)
entry = tk.Entry(control_frame, width=50, bg="#bfbfbf", fg="#000000", bd=0 , font=('Segoe Script', 12))
entry.grid(row=1, column=1,padx = 5)
entry.bind("<Return>", lambda event: search_wikipedia())
switch_button = tk.Button(control_frame, text="RU", command=switch_language, bg="#e0e0e0", fg="#000000", bd=0,)
switch_button.grid(row=1, column=3,padx = 5)
search_button = tk.Button(control_frame, text="🔎", command=search_wikipedia, bg="#e0e0e0", fg="#000000", bd=0)
search_button.grid(row=1, column=2,padx = 5)
open_file_button = tk.Button(control_frame, text="Open file with previous searches", command=open_search_file, bg="#e0e0e0", fg="#000000", bd=0,)
open_file_button.grid(row=1, column=4 , padx = 5)
text_area = st.ScrolledText(root, width=10000, height=5000, bg="#b3b3b3", fg="Black", bd=0, font=('Segoe Script', 12))
text_area.pack(padx=10, pady=5)
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
