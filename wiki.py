import wikipedia # type: ignore
import tkinter as tk
from tkinter import scrolledtext as st
import os
import subprocess
languages = {
    'EN':'en',
    'RU':'ru',
    'DE':'de',
    'FR':'fr',
    'ES':'es',
    'ZH':'zh',
    'JA':'ja',
    'KO':'ko'
}
lang = 'EN'
def open_search_file():
    if os.path.isfile("previous_search.txt"):
        subprocess.run(['notepad.exe', 'previous_search.txt'])
    else:
        text_area.delete("1.0", tk.END)
        text_area.insert(tk.END, "previous_search.txt not found.")
def switch_language(new_lang):
    global lang
    lang = new_lang
    wikipedia.set_lang(languages[lang.upper()])
def search_wikipedia():
    query = entry.get()
    try:
        current_content = text_area.get("1.0", tk.END)
        if current_content.strip():
            with open("previous_search.txt", "w", encoding="utf-8") as file:
                file.write(current_content)
        wikipedia.set_lang(languages[lang.upper()])  # Добавлено upper()
        result = wikipedia.page(query)
        text_area.delete(1.0, tk.END)
        text_area.insert(tk.END, result.content)
    except wikipedia.exceptions.DisambiguationError as e:
        options = ", ".join(e.options)
        text_area.delete(1.0, tk.END)
        text_area.insert(tk.END, f"Please specify your question, there are some options: {options}")
    except wikipedia.exceptions.PageError:
        text_area.delete(1.0, tk.END)
        text_area.insert(tk.END, "Nothing was found on Wikipedia.")
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
entry = tk.Entry(control_frame, width=50 , bg="#bfbfbf", fg="#000000", bd=0 , font=('Segoe Script', 12))
entry.grid(row=1, column=1,padx = 5)
entry.bind("<Return>", lambda event: search_wikipedia())
language_var = tk.StringVar(value=lang,)
language_menu = tk.OptionMenu(control_frame, language_var, *languages.keys(), command=switch_language)
language_menu.config(bg="#e0e0e0", fg="#000000",bd=0,highlightthickness=0)
language_menu.grid(row=1, column=12, padx=5)
search_button = tk.Button(control_frame, text="🔎", height=1 ,width= 2,command=search_wikipedia, bg="#e0e0e0", fg="#000000", bd=0)
search_button.grid(row=1, column=2,padx = 5)
open_file_button = tk.Button(control_frame, text="Open file with previous searches", command=open_search_file, bg="#e0e0e0", fg="#000000", bd=0,)
open_file_button.grid(row=1, column=4 , padx = 5)
text_area = st.ScrolledText(root, width=10000, height=5000, bg="#b3b3b3", fg="Black", bd=0, font=('Segoe Script', 12))
text_area.pack(padx=10, pady=5)
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
