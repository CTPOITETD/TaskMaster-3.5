# Importing stuff (there's lots of imports, y'know?)
import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog, colorchooser
import json
import os
import sys
import subprocess
from datetime import datetime
# Our main class
class TaskMaster:

    def __init__(self, root):
        self.root = root
        self.tasks_data = []
        self.selected_task_data = None
        self.MAX_TASKS = 1000
        self.MAX_CHARS = 200
        self.is_dirty = False
        self.timer_running = False
        self.is_readonly = False
        self.current_file_password = None
        self.seconds = 0
        self.current_lang = "EN"
        self.lang_data = {
            # Ukrainian Translation
            "UA": {
                "title": "Task Master",
                "file": "Файл", 
                "edit": "Редагування", 
                "view": "Вигляд", 
                "lang": "Мова",
                "timer": "Таймер", 
                "start": "Старт", 
                "stop": "Стоп", 
                "reset": "Скидання",
                "new_win": "Нове вікно", 
                "open": "Відкрити", 
                "save": "Зберегти",
                "open_prog": "Відкрити програму", 
                "clear": "Очистити все",
                "new_task": "Створити завдання", 
                "replace": "Замінити", 
                "del_sel": "Видалити",
                "sel_all": "Виділити все", 
                "theme_toggle": "Змінити тему", 
                "add_btn": "+ СТВОРИТИ",
                "unlock_btn": "ВВЕСТИ ПАРОЛЬ", 
                "ask_clear": "Видалити все?",
                "new_task_q": "Текст завдання:", 
                "add_win_title": "Додати", 
                "repeat_lab": "Повторити:",
                "color_btn": "Колір тексту", 
                "is_sec": "Це РОЗДІЛ?", 
                "empty": "(Пусто)",
                "size_lab": "Розмір:", 
                "help": "Допомога", 
                "hotkeys": "Гарячі клавіші", 
                "about": "Про програму",
                "hk_title": "Список гарячих клавіш:",
                "hk_msg": "Delete - видалити вибране\nCtrl+Delete - видалити всі завдання\nAlt+F4 - закрити програму (але ти сеодно маєш зробити завдання)\nCtrl+Alt+F4 - швидке закриття програми\nCtrl+K - виділити всі завдання\nCtrl+S - створити нове завдання\nCtrl+F - Почати/Остановити таймер",
                "about_msg": "Оригінальний сувій TaskMaster:\n \nСей код писав @CTPOITETD-5_0\nРоку Божого 2026\nВерсії: 3.5\nСтатус: Ретро\n\nАщо ж ти, смертний, що берешся правити код сей,\nНе забудь ім'я своє вписати,\nБо інакше предки програмування проклянуть!",
                "limit_err": "Досягнуто ліміт у 1000 завдань!", 
                "ro_msg": "РЕЖИМ ПЕРЕГЛЯДУ",
                "pass_ask": "Введіть пароль:", 
                "pass_set": "Встановіть пароль (Залишіть пустим щоб не додавати пароль):",
                "wrong_pass": "Невірний пароль!",
                "exit_q": "Ви точно хочете вийти? Незбережені зміни будуть втрачені!"
            },
            # English Translation
            "EN": {
                "title": "Task Master",
                "file": "File", 
                "edit": "Edit", 
                "view": "View", 
                "lang": "Language",
                "timer": "Timer", 
                "start": "Start", 
                "stop": "Stop", 
                "reset": "Reset",
                "new_win": "New Window", 
                "open": "Open .task", 
                "save": "Save .task",
                "open_prog": "Open Program", 
                "clear": "Clear All",
                "new_task": "Create Task", 
                "replace": "Replace", 
                "del_sel": "Delete Selected",
                "sel_all": "Select All", 
                "theme_toggle": "Toggle Theme", 
                "add_btn": "+ CREATE",
                "unlock_btn": "ENTER PASSWORD", 
                "ask_clear": "Clear all?",
                "new_task_q": "Task text:", 
                "add_win_title": "Add Task", 
                "repeat_lab": "Repeat times:",
                "color_btn": "Text Color", 
                "is_sec": "Is SECTION?", 
                "empty": "(Empty)",
                "size_lab": "Size:", 
                "help": "Help", 
                "hotkeys": "Hotkeys", 
                "about": "Info",
                "hk_title": "There are all Hot-keys in project:",
                "hk_msg": "Delete - delete (selected)\nCtrl+Delete - delete (all)\nAlt+F4 - close program\nCtrl+Alt+F4 - close program (without warning)\nCtrl+K - Select all\nCtrl+S - create new task\nCtrl+F - start/stop timer",
                "about_msg": "Task Master\n \nOriginally created by: @CTPOITETD-5_0\n(You can find me on Scratch/YouTube)\nCreated in: Python\nVersion: 3.5\nStatus: Retro\nRemember - if you made any changes in this project, change this text to your credits (As a modificator)",
                "limit_err": "Limit of 1000 tasks reached!", 
                "ro_msg": "READ-ONLY MODE",
                "pass_ask": "Enter password for full access:", 
                "pass_set": "Set password (leave empty for none):",
                "wrong_pass": "Wrong password!",
                "exit_q": "Are you sure you want to exit? Unsaved changes will be lost!"
            }
        }
        # Icon load
        try:
            
            current_dir = os.path.dirname(os.path.abspath(__file__))
            icon_file = os.path.join(current_dir, "icon.ico")
            
            if os.path.exists(icon_file):
                
                try:
                    self.root.iconbitmap(default=icon_file)
                
                except Exception as e:
                    print(f"Icon load error: {e}")
            
            else:
                print("Icon file not found, using default icon.")
        
        except Exception as e:
            print(f"Icon load error: {e}")
        
        # Diffrent themes' colors sets
        self.themes = {
            "Black": {"bg": "#000000", "fg": "#ffffff", "item_bg": "#0a0a0a", "sel": "#1e3a5f", "sec_fg": "#4E4E4E"},
            "White": {"bg": "#acacac", "fg": "#000000", "item_bg": "#666666", "sel": "#d1e8ff", "sec_fg": "#666666"}
        }
        # Starting settings
        self.current_theme = "Black"
        self.setup_ui()
        self.apply_theme("Black")
        self.switch_lang("EN")
        self.add_task_item('Say "Hello World!"', self.themes["Black"]["fg"])
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.bind_hotkeys()
    # Just read the name...
    def setup_ui(self):
        self.top_bar = tk.Frame(self.root)
        self.top_bar.pack(fill="x")
        self.timer_label = tk.Label(self.top_bar, text="00:00:00", font=("Consolas", 20, "bold"), fg="#0000FF")
        self.timer_label.pack(side="left", padx=20)
        self.size_label = tk.Label(self.top_bar, text="43 B", font=("Arial", 9), fg="gray")
        self.size_label.pack(side="right", padx=10)
        self.empty_label = tk.Label(self.root, text="", font=("Arial", 10), fg="gray")
        self.empty_label.pack(pady=0)
        self.btn_main = tk.Button(self.root, bg="#4CAF50", fg="white", font=("Arial", 11, "bold"), pady=15, command=self.handle_main_button)
        self.btn_main.pack(side="bottom", fill="x")
        self.canvas = tk.Canvas(self.root, highlightthickness=0)
        self.scroll_frame = tk.Frame(self.canvas)
        self.scrollbar = tk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        self.scroll_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind_all("<MouseWheel>", lambda e: self.canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
    # Just controls main buttons I guess?
    def handle_main_button(self):
        if self.is_readonly: self.try_unlock()
        else: self.open_add_window()
    # Shows messange when you try to unlock locked message
    def try_unlock(self):
        L = self.lang_data[self.current_lang]
        attempt = simpledialog.askstring("Security", L["pass_ask"], show='*')
        if attempt == self.current_file_password: self.set_readonly_mode(False)
        elif attempt is not None: messagebox.showerror("Error", L["wrong_pass"])
    # Sets "Read Only" mode
    def set_readonly_mode(self, state):
        self.is_readonly = state
        L = self.lang_data[self.current_lang]
        if state:
            self.btn_main.config(text=L["unlock_btn"], bg="#0056b3", fg="white")
            self.empty_label.config(text=L["ro_msg"], fg="red")

        else:
            self.btn_main.config(text=L["add_btn"], bg="#4CAF50", fg="white")
            self.check_empty()

        for t in self.tasks_data:
            if "cb" in t: t["cb"].config(state="disabled" if state else "normal")

        self.create_menu()
    # Creates menu's UI
    def create_menu(self):
        self.menu_bar = tk.Menu(self.root); self.root.config(menu=self.menu_bar); L = self.lang_data[self.current_lang]
        ro = "disabled" if self.is_readonly else "normal"
        f_m = tk.Menu(self.menu_bar, tearoff=0)
        f_m.add_command(label=L['new_win'], command=self.open_new_instance)
        f_m.add_separator()
        f_m.add_command(label=L['open'], command=self.load_from_file)
        f_m.add_command(label=L['save'], command=self.save_to_file, state=ro)
        f_m.add_separator()
        f_m.add_command(label=L['clear'], command=self.clear_all, state=ro)
        self.menu_bar.add_cascade(label=L["file"], menu=f_m)
        e_m = tk.Menu(self.menu_bar, tearoff=0)
        e_m.add_command(label=L['new_task'], command=self.open_add_window, state=ro)
        e_m.add_command(label=L["replace"], command=self.edit_selected, state=ro)
        e_m.add_separator()
        e_m.add_command(label=L['del_sel'], command=self.delete_selected, state=ro)
        e_m.add_command(label=L['sel_all'], command=self.select_all_tasks, state=ro)
        self.menu_bar.add_cascade(label=L["edit"], menu=e_m)
        v_m = tk.Menu(self.menu_bar, tearoff=0)
        v_m.add_command(label=L["theme_toggle"], command=self.toggle_theme)
        l_m = tk.Menu(v_m, tearoff=0)
        l_m.add_command(label="English", command=lambda: self.switch_lang("EN"))
        l_m.add_command(label="Українська", command=lambda: self.switch_lang("UA"))
        v_m.add_cascade(label=L["lang"], menu=l_m)
        self.menu_bar.add_cascade(label=L["view"], menu=v_m)
        t_m = tk.Menu(self.menu_bar, tearoff=0)
        t_m.add_command(label=L["start"], command=self.start_timer, state=ro)
        t_m.add_command(label=L["stop"], command=self.stop_timer, state=ro)
        t_m.add_command(label=L["reset"], command=self.reset_timer, state=ro)
        self.menu_bar.add_cascade(label=L["timer"], menu=t_m)
        h_m = tk.Menu(self.menu_bar, tearoff=0)
        h_m.add_command(label=L["hotkeys"], command=lambda: messagebox.showinfo(L["hk_title"], L["hk_msg"]))
        h_m.add_command(label=L["about"], command=lambda: messagebox.showinfo(L["about"], L["about_msg"]))
        self.menu_bar.add_cascade(label=L["help"], menu=h_m)
        self.menu_bar.add_command(label=L["open_prog"], command=self.open_external_program, state=ro)
    # For loading .task files (not in program)
    def load_from_file(self):
        p = filedialog.askopenfilename(filetypes=[("Task files", "*.task")])
        
        if p:
            with open(p, "r", encoding="utf-8") as f: data = json.load(f)
            self.current_file_password = data.get("password")
            self.set_readonly_mode(False)
            
            if self.current_file_password:
                attempt = simpledialog.askstring("Security", self.lang_data[self.current_lang]["pass_ask"], show='*')
                
                if attempt != self.current_file_password: self.set_readonly_mode(True)

            for t in self.tasks_data: t["frame"].destroy()
            self.tasks_data = []
            for itm in data["tasks"]: self.add_task_item(itm["text"], itm["color"], itm.get("is_sec", False), itm.get("time"))
            self.is_dirty = False
    # Saves .task files
    def save_to_file(self):
        p = filedialog.asksaveasfilename(defaultextension=".task")

        if p:
            pwd = simpledialog.askstring("Security", self.lang_data[self.current_lang]["pass_set"], show='*')
            self.current_file_password = pwd
            d = {"password": pwd, "tasks": [{"text": t["text"], "color": t["custom_color"], "is_sec": t["is_sec"], "time": t["time"]} for t in self.tasks_data]}
            with open(p, "w", encoding="utf-8") as f: json.dump(d, f)
            self.is_dirty = False
    # Loads .task files (in program)
    def load_from_path(self, p):
        try:
            with open(p, "r", encoding="utf-8") as f: 
                data = json.load(f)
            
            self.current_file_password = data.get("password")
            self.set_readonly_mode(False)
            if self.current_file_password:
                L = self.lang_data[self.current_lang]
                attempt = simpledialog.askstring("Security", L["pass_ask"], show='*')
                if attempt != self.current_file_password: 
                    self.set_readonly_mode(True)

            for t in self.tasks_data: 
                t["frame"].destroy()
            self.tasks_data = []
            
            for itm in data["tasks"]: 
                self.add_task_item(itm["text"], itm["color"], itm.get("is_sec", False), itm.get("time"))
            
            self.is_dirty = False
            self.check_empty()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open .task file: {e}")
    # Adds task
    def add_task_item(self, text, color, is_sec=False, timestamp=None):
        
        if len(self.tasks_data) >= self.MAX_TASKS:

            messagebox.showwarning("Limit", self.lang_data[self.current_lang]["limit_err"])
            return False

        if not timestamp: timestamp = datetime.now().strftime("%H:%M:%S")
        safe_text = text[:self.MAX_CHARS]
        c = self.themes[self.current_theme]
        f = tk.Frame(self.scroll_frame); f.pack(fill="x", padx=5, pady=1)
        entry = {"text": safe_text, "is_sec": is_sec, "time": timestamp, "frame": f, "custom_color": color}

        if is_sec:
            lbl = tk.Label(f, text=self.center_section_text(safe_text), font=("Arial", 10, "bold"), anchor="center")
            lbl.pack(side="left", fill="x", expand=True)
            cnt = tk.Label(f, text="(0)", font=("Arial", 9), width=5, anchor="w"); cnt.pack(side="right")
            entry.update({"label": lbl, "cnt_lab": cnt, "var": tk.BooleanVar()})

        else:
            num = tk.Label(f, text="", font=("Arial", 8), width=5, anchor="e"); num.pack(side="left")
            var = tk.BooleanVar(); cb = tk.Checkbutton(f, variable=var, command=lambda: self.fade_out(f))
            cb.config(state="disabled" if self.is_readonly else "normal")
            cb.pack(side="left")
            lbl = tk.Label(f, text=safe_text, font=("Arial", 10), anchor="w", fg=color); lbl.pack(side="left")
            t_lab = tk.Label(f, text=" [" + timestamp + "]", font=("Arial", 7), fg="gray"); t_lab.pack(side="left")
            entry.update({"label": lbl, "num": num, "cb": cb, "t_lab": t_lab, "var": var})

        self.tasks_data.append(entry)
        lbl.bind("<Button-1>", lambda e: self.select_task(entry) if not self.is_readonly else None)
        self.style_task(entry, c); self.mark_changed(); self.check_empty()
        return True
    # Opens second window
    def open_add_window(self, e=None):

        if self.is_readonly: return
        L = self.lang_data[self.current_lang]
        win = tk.Toplevel(self.root); win.title(L["add_win_title"]); win.geometry("300x280"); win.grab_set()
        self.temp_color = self.themes[self.current_theme]["fg"]
        tk.Label(win, text=L["new_task_q"]).pack(pady=5)
        e_txt = tk.Entry(win, width=30); e_txt.pack(); e_txt.focus_set()
        is_sec_v = tk.BooleanVar(); tk.Checkbutton(win, text=L["is_sec"], variable=is_sec_v).pack(pady=5)
        tk.Button(win, text=L["color_btn"], command=self.pick_clr).pack(pady=5)
        e_cnt = tk.Spinbox(win, from_=1, to=10, width=5); e_cnt.pack(pady=5)
        def sub():
            for _ in range(int(e_cnt.get())): self.add_task_item(e_txt.get() or "New Task", self.temp_color, is_sec_v.get())
            win.destroy()
        tk.Button(win, text="OK", command=sub, width=10).pack(pady=15)
    # Changes UI's language
    def switch_lang(self, code):

        self.current_lang = code; L = self.lang_data[code]
        self.root.title(L["title"])
        self.btn_main.config(text=L["unlock_btn"] if self.is_readonly else L["add_btn"])
        if self.is_readonly: self.empty_label.config(text=L["ro_msg"])
        else: self.check_empty()
        self.create_menu()
    # Timer's functions
    def update_timer(self):
        if self.timer_running:
            self.seconds += 1; m, s = divmod(self.seconds, 60); h, m = divmod(m, 60)
            self.timer_label.config(text=f"{h:02}:{m:02}:{s:02}"); self.root.after(1000, self.update_timer)

    def start_timer(self):
        if not self.timer_running and not self.is_readonly: self.timer_running = True; self.update_timer()

    def stop_timer(self): self.timer_running = False
    def reset_timer(self): self.timer_running = False; self.seconds = 0; self.timer_label.config(text="00:00:00")
    def toggle_timer_hk(self, e=None): self.start_timer() if not self.timer_running else self.stop_timer()
    def center_section_text(self, text):
        clean = text.strip(); side = "-" * max(5, (40 - len(clean)) // 2)
        return side + " " + clean + " " + side
    # Updates file size display
    def update_file_size_display(self):
        L = self.lang_data[self.current_lang]
        to_calc = [{"t": t["text"], "s": t["is_sec"]} for t in self.tasks_data]
        b = len(json.dumps(to_calc).encode('utf-8'))
        s_txt = f"{b} B" if b < 1024 else f"{round(b/1024, 2)} KB"
        self.size_label.config(text=L['size_lab'] + " " + s_txt)
    # I tired to write description for all of those functions, ok?
    def mark_changed(self): self.update_file_size_display(); self.update_section_counters()
    def update_section_counters(self):
        curr = 1
        for i, t in enumerate(self.tasks_data):
            if t["is_sec"]:
                count = 0
                for j in range(i + 1, len(self.tasks_data)):
                    if self.tasks_data[j]["is_sec"]:
                        break
                    count += 1
                
                t["cnt_lab"].config(text=f"({count})")
            else:
                if "num" in t:
                    if t["text"].startswith("S.-"):
                        t["num"].config(text="") 
                    else:
                        t["num"].config(text=f"{curr}.")
                        curr += 1

    def open_external_program(self):
        if self.is_readonly: return
        f_path = filedialog.askopenfilename()

        if f_path:
            try:
                if os.name == 'nt': os.startfile(f_path)
                else: subprocess.Popen(['open' if sys.platform == 'darwin' else 'xdg-open', f_path])
            except Exception as e: messagebox.showerror("Error", str(e))

    def select_task(self, t):
        if not self.is_readonly: self.selected_task_data = t; self.apply_theme(self.current_theme)

    def apply_theme(self, name):
        self.current_theme = name; c = self.themes[name]
        self.root.config(bg=c["bg"]); self.canvas.config(bg=c["bg"]); self.scroll_frame.config(bg=c["bg"])
        self.timer_label.config(bg=c["bg"]); self.top_bar.config(bg=c["bg"]); self.size_label.config(bg=c["bg"]); self.empty_label.config(bg=c["bg"])
        for t in self.tasks_data: self.style_task(t, c)

    def style_task(self, t, c):
        is_sel = (t == self.selected_task_data); bg = c["sel"] if is_sel else c["item_bg"]
        t["frame"].config(bg=bg); t["label"].config(bg=bg)

        if t["is_sec"]: t["label"].config(fg=t["custom_color"] if t["custom_color"] != c["fg"] else c["sec_fg"]); t["cnt_lab"].config(bg=bg, fg=c["sec_fg"])

        else:
            t["label"].config(fg=t["custom_color"] if not is_sel else c["fg"]); t["num"].config(bg=bg, fg="gray")
            t["cb"].config(bg=bg, selectcolor=c["bg"]); t["t_lab"].config(bg=bg)

    def check_empty(self):
        
        if not self.is_readonly:
            msg = self.lang_data[self.current_lang]["empty"] if not self.tasks_data else ""
            self.empty_label.config(text=msg, fg="gray")

    def fade_out(self, f):
        if not self.is_readonly: f.config(bg="#330000"); self.root.after(200, lambda: self.final_remove(f))

    def final_remove(self, f):
        self.tasks_data = [t for t in self.tasks_data if t["frame"] != f]; f.destroy(); self.mark_changed(); self.check_empty()

    def select_all_tasks(self, e=None):
        if not self.is_readonly and self.tasks_data: self.select_task(self.tasks_data[0])

    def edit_selected(self):

        if not self.is_readonly and self.selected_task_data:
            res = simpledialog.askstring("Edit", "Text:", initialvalue=self.selected_task_data["text"])

            if res:
                self.selected_task_data["text"] = res
                self.selected_task_data["label"].config(text=self.center_section_text(res) if self.selected_task_data["is_sec"] else res)
                self.mark_changed()

    def delete_selected(self, e=None):
        if not self.is_readonly and self.selected_task_data: self.final_remove(self.selected_task_data["frame"]); self.selected_task_data = None

    def clear_all(self): self.delete_all_hk()
    def delete_all_hk(self, e=None):

        if not self.is_readonly and messagebox.askyesno("Clear", self.lang_data[self.current_lang]["ask_clear"]):
            for t in self.tasks_data: t["frame"].destroy()
            self.tasks_data = []; self.mark_changed(); self.check_empty()

    def open_new_instance(self): subprocess.Popen([sys.executable, sys.argv[0]])
    def on_closing(self):
        L = self.lang_data[self.current_lang]

        if messagebox.askyesno(L["title"], L["exit_q"]): 
            self.root.destroy()
        else:
            pass
    
    def fast_exit(self, e=None): os._exit(0)
    def pick_clr(self):

        c = colorchooser.askcolor()[1]

        if c: self.temp_color = c

    def toggle_theme(self): self.current_theme = "White" if self.current_theme == "Black" else "Black"; self.apply_theme(self.current_theme)
    def bind_hotkeys(self):
        self.root.bind("<Control-s>", lambda e: self.handle_main_button())
        self.root.bind("<Delete>", lambda e: self.delete_selected() if not self.is_readonly else None)
        self.root.bind("<Control-Delete>", lambda e: self.delete_all_hk() if not self.is_readonly else None)
        self.root.bind("<Control-k>", lambda e: self.select_all_tasks() if not self.is_readonly else None)
        self.root.bind("<Control-f>", self.toggle_timer_hk)
        self.root.bind("<Control-Alt-F4>", self.fast_exit)

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskMaster(root)
    
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        
        if os.path.exists(file_path) and file_path.lower().endswith(".task"):
            app.load_from_path(file_path)

    root.mainloop()

# What are we doing here?)
