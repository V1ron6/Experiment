import tkinter as tk

todos = []

# Enhanced Color scheme
COLORS = {
    "bg": "#1a1a2e",
    "bg_light": "#16213e",
    "card_bg": "#0f3460",
    "card_complete": "#1e5128",
    "card_hover": "#1a4a5e",
    "primary": "#e94560",
    "primary_hover": "#ff6b6b",
    "secondary": "#0f3460",
    "danger": "#e74c3c",
    "danger_hover": "#ff5252",
    "success": "#4ecca3",
    "success_hover": "#7fff00",
    "warning": "#f39c12",
    "text": "#eaeaea",
    "text_light": "#a0a0a0",
    "text_dark": "#333333",
    "accent": "#00fff5",
    "border": "#533483"
}

root = tk.Tk()
root.title("T@PP - Todo App")
root.geometry("550x700")
root.configure(bg=COLORS["bg"])
root.resizable(True, True)

# ============= CUSTOM POPUP/DIALOG SYSTEM =============
class CustomDialog:
    """Custom styled dialog box to replace default messagebox"""
    
    def __init__(self, parent, title, message, dialog_type="info", buttons=None):
        self.result = None
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.configure(bg=COLORS["bg_light"])
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center the dialog - INCREASED HEIGHT for buttons
        dialog_width = 400
        dialog_height = 300
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (dialog_width // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (dialog_height // 2)
        self.dialog.geometry(f"{dialog_width}x{dialog_height}+{x}+{y}")
        self.dialog.resizable(False, False)
        
        # Icon and colors based on type
        icons = {
            "info": ("ℹ️", COLORS["primary"]),
            "success": ("✅", COLORS["success"]),
            "warning": ("⚠️", COLORS["warning"]),
            "error": ("❌", COLORS["danger"]),
            "confirm": ("❓", COLORS["accent"])
        }
        icon, accent_color = icons.get(dialog_type, icons["info"])
        
        # Main container with border effect
        border_frame = tk.Frame(self.dialog, bg=accent_color, padx=2, pady=2)
        border_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        main_frame = tk.Frame(border_frame, bg=COLORS["bg_light"])
        main_frame.pack(fill="both", expand=True)
        
        # Header with icon
        header = tk.Frame(main_frame, bg=COLORS["bg_light"], pady=10)
        header.pack(fill="x")
        
        icon_label = tk.Label(header, text=icon, font=("Segoe UI Emoji", 28),
                              bg=COLORS["bg_light"], fg=accent_color)
        icon_label.pack()
        
        # Title
        title_label = tk.Label(header, text=title, font=("Arial", 14, "bold"),
                               bg=COLORS["bg_light"], fg=COLORS["text"])
        title_label.pack(pady=(5, 0))
        
        # Message
        msg_frame = tk.Frame(main_frame, bg=COLORS["bg_light"], pady=8)
        msg_frame.pack(fill="x", padx=20)
        
        msg_label = tk.Label(msg_frame, text=message, font=("Arial", 11),
                             bg=COLORS["bg_light"], fg=COLORS["text_light"],
                             wraplength=320, justify="center")
        msg_label.pack()
        
        # Buttons - placed at BOTTOM
        btn_frame = tk.Frame(main_frame, bg=COLORS["bg_light"], pady=20)
        btn_frame.pack(side=tk.BOTTOM, fill="x")
        
        if buttons is None:
            buttons = [("OK", True)]
        
        for btn_text, btn_value in buttons:
            if btn_value is True or btn_text.lower() in ["ok", "yes", "confirm"]:
                btn_color = accent_color
                btn_fg = "white"
            else:
                btn_color = COLORS["danger"]
                btn_fg = "white"
            
            btn = tk.Button(btn_frame, text=btn_text, font=("Arial", 10, "bold"),
                           bg=btn_color, fg=btn_fg,
                           relief=tk.FLAT, cursor="hand2", width=12, pady=8,
                           command=lambda v=btn_value: self._on_button(v))
            btn.pack(side=tk.LEFT, padx=15, expand=True)
            
            # Hover effects with proper closure
            original_color = btn_color
            btn.bind("<Enter>", lambda e, b=btn: b.configure(bg=COLORS["primary_hover"]))
            btn.bind("<Leave>", lambda e, b=btn, c=original_color: b.configure(bg=c))
        
        # Handle window close
        self.dialog.protocol("WM_DELETE_WINDOW", lambda: self._on_button(False))
        
        # Focus dialog
        self.dialog.focus_set()
        
        # Wait for dialog to close
        self.dialog.wait_window()
    
    def _on_button(self, value):
        self.result = value
        self.dialog.destroy()

def show_info(title, message):
    """Show info dialog"""
    CustomDialog(root, title, message, "info")

def show_success(title, message):
    """Show success dialog"""
    CustomDialog(root, title, message, "success")

def show_warning(title, message):
    """Show warning dialog"""
    CustomDialog(root, title, message, "warning")

def show_error(title, message):
    """Show error dialog"""
    CustomDialog(root, title, message, "error")

def show_confirm(title, message):
    """Show confirmation dialog and return True/False"""
    dialog = CustomDialog(root, title, message, "confirm", 
                         buttons=[("Yes", True), ("No", False)])
    return dialog.result

# ============= TOAST NOTIFICATION SYSTEM =============
class Toast:
    """Floating toast notification"""
    
    def __init__(self, parent, message, toast_type="info", duration=2500):
        self.parent = parent
        
        colors = {
            "info": COLORS["primary"],
            "success": COLORS["success"],
            "warning": COLORS["warning"],
            "error": COLORS["danger"]
        }
        icons = {
            "info": "ℹ️",
            "success": "✓",
            "warning": "⚠",
            "error": "✗"
        }
        
        bg_color = colors.get(toast_type, colors["info"])
        icon = icons.get(toast_type, icons["info"])
        
        # Create toast frame
        self.toast = tk.Frame(parent, bg=bg_color, padx=15, pady=10)
        
        # Icon
        tk.Label(self.toast, text=icon, font=("Arial", 12, "bold"),
                bg=bg_color, fg="white").pack(side=tk.LEFT, padx=(0, 10))
        
        # Message
        tk.Label(self.toast, text=message, font=("Arial", 10),
                bg=bg_color, fg="white").pack(side=tk.LEFT)
        
        # Close button
        close_btn = tk.Label(self.toast, text="×", font=("Arial", 14, "bold"),
                            bg=bg_color, fg="white", cursor="hand2")
        close_btn.pack(side=tk.RIGHT, padx=(10, 0))
        close_btn.bind("<Button-1>", lambda e: self.hide())
        
        # Position at top center
        self.toast.place(relx=0.5, y=-50, anchor="n")
        
        # Animate in
        self._animate_in()
        
        # Auto hide after duration
        self.parent.after(duration, self.hide)
    
    def _animate_in(self, y=-50):
        if y < 10:
            y += 5
            self.toast.place(relx=0.5, y=y, anchor="n")
            self.parent.after(15, lambda: self._animate_in(y))
    
    def hide(self):
        try:
            self.toast.destroy()
        except:
            pass

def show_toast(message, toast_type="info", duration=2500):
    """Show a toast notification"""
    Toast(root, message, toast_type, duration)

# ============= PAGE SWITCHER =============
def switch_to_main():
    welcome.place_forget()
    welcome_btns.pack_forget()
    main_page.pack(fill="both", expand=True)
    show_toast("Welcome! Let's get productive! 🚀", "success")

def switch_to_welcome():
    main_page.pack_forget()
    welcome.place(relx=0.5, rely=0.4, anchor=tk.CENTER)
    welcome_btns.pack(side=tk.BOTTOM)

# ============= WELCOME PAGE =============
welcome = tk.Frame(root, bg=COLORS["bg"])

# Animated logo frame
logo_frame = tk.Frame(welcome, bg=COLORS["bg"])
logo_frame.pack(pady=20)

# App icon
app_icon = tk.Label(logo_frame, text="📝", font=("Segoe UI Emoji", 48),
                    bg=COLORS["bg"])
app_icon.pack()

# App title with gradient effect simulation
title_label = tk.Label(welcome, text="T@PP", font=("Arial", 36, "bold"), 
                       bg=COLORS["bg"], fg=COLORS["primary"])
title_label.pack()

subtitle = tk.Label(welcome, text="Your Personal Task Manager", 
                    font=("Arial", 12), bg=COLORS["bg"], fg=COLORS["accent"])
subtitle.pack(pady=(5, 0))

tagline = tk.Label(welcome, text="Part of the Curiosity Program", 
                   font=("Arial", 10, "italic"), bg=COLORS["bg"], fg=COLORS["text_light"])
tagline.pack(pady=(10, 0))

# Feature highlights
features_frame = tk.Frame(welcome, bg=COLORS["bg"], pady=30)
features_frame.pack()

features = [
    ("✓", "Organize your tasks"),
    ("✓", "Track your progress"),
    ("✓", "Stay productive")
]

for icon, text in features:
    feature_row = tk.Frame(features_frame, bg=COLORS["bg"])
    feature_row.pack(anchor="w", pady=3)
    tk.Label(feature_row, text=icon, font=("Arial", 10), 
             bg=COLORS["bg"], fg=COLORS["success"]).pack(side=tk.LEFT)
    tk.Label(feature_row, text=f"  {text}", font=("Arial", 10), 
             bg=COLORS["bg"], fg=COLORS["text_light"]).pack(side=tk.LEFT)

welcome.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

# Welcome buttons
welcome_btns = tk.Frame(root, pady=30, bg=COLORS["bg"])
welcome_btns.pack(side=tk.BOTTOM)

btnsinit = tk.Button(welcome_btns, text="🚀  Get Started", 
                     height=2, width=25, command=switch_to_main,
                     bg=COLORS["primary"], fg="white", font=("Arial", 12, "bold"),
                     relief=tk.FLAT, cursor="hand2", activebackground=COLORS["primary_hover"])
btnsinit.pack()

# Hover animation for start button
def on_start_hover(e):
    btnsinit.configure(bg=COLORS["primary_hover"])
def on_start_leave(e):
    btnsinit.configure(bg=COLORS["primary"])
btnsinit.bind("<Enter>", on_start_hover)
btnsinit.bind("<Leave>", on_start_leave)

# Version label
version_label = tk.Label(welcome_btns, text="v2.0", font=("Arial", 8),
                        bg=COLORS["bg"], fg=COLORS["text_light"])
version_label.pack(pady=(15, 0))

# ============= MAIN PAGE =============
main_page = tk.Frame(root, bg=COLORS["bg"])

# Header section with stats
header_frame = tk.Frame(main_page, bg=COLORS["bg_light"], pady=15)
header_frame.pack(fill="x")

header_inner = tk.Frame(header_frame, bg=COLORS["bg_light"])
header_inner.pack(fill="x", padx=20)

# Left side - title
title_section = tk.Frame(header_inner, bg=COLORS["bg_light"])
title_section.pack(side=tk.LEFT)

tk.Label(title_section, text="📋", font=("Segoe UI Emoji", 20),
         bg=COLORS["bg_light"]).pack(side=tk.LEFT)
tk.Label(title_section, text=" My Tasks", font=("Arial", 18, "bold"),
         bg=COLORS["bg_light"], fg=COLORS["text"]).pack(side=tk.LEFT)

# Right side - stats
stats_section = tk.Frame(header_inner, bg=COLORS["bg_light"])
stats_section.pack(side=tk.RIGHT)

td_total = tk.Label(stats_section, text="0 tasks", 
                    font=("Arial", 11), bg=COLORS["bg_light"], fg=COLORS["text_light"])
td_total.pack(side=tk.LEFT, padx=10)

td_complete = tk.Label(stats_section, text="0 done", 
                       font=("Arial", 11), bg=COLORS["bg_light"], fg=COLORS["success"])
td_complete.pack(side=tk.LEFT)

# Progress bar frame
progress_frame = tk.Frame(main_page, bg=COLORS["bg"], pady=10, padx=20)
progress_frame.pack(fill="x")

progress_label = tk.Label(progress_frame, text="Progress: 0%", font=("Arial", 9),
                          bg=COLORS["bg"], fg=COLORS["text_light"])
progress_label.pack(anchor="w")

progress_bg = tk.Frame(progress_frame, bg=COLORS["secondary"], height=8)
progress_bg.pack(fill="x", pady=(5, 0))

progress_bar = tk.Frame(progress_bg, bg=COLORS["success"], height=8, width=0)
progress_bar.place(x=0, y=0, relheight=1)

# Filter buttons
filter_frame = tk.Frame(main_page, bg=COLORS["bg"], pady=10)
filter_frame.pack(fill="x", padx=20)

current_filter = tk.StringVar(value="all")

def set_filter(filter_type):
    current_filter.set(filter_type)
    refresh_todos()
    # Update button styles
    for btn, f_type in filter_buttons:
        if f_type == filter_type:
            btn.configure(bg=COLORS["primary"], fg="white")
        else:
            btn.configure(bg=COLORS["secondary"], fg=COLORS["text_light"])

filter_buttons = []
for text, f_type in [("All", "all"), ("Active", "active"), ("Completed", "completed")]:
    btn = tk.Button(filter_frame, text=text, font=("Arial", 9),
                   bg=COLORS["primary"] if f_type == "all" else COLORS["secondary"],
                   fg="white" if f_type == "all" else COLORS["text_light"],
                   relief=tk.FLAT, cursor="hand2", width=10, pady=3,
                   command=lambda t=f_type: set_filter(t))
    btn.pack(side=tk.LEFT, padx=(0, 5))
    filter_buttons.append((btn, f_type))

# Scrollable todo display area
canvas_frame = tk.Frame(main_page, bg=COLORS["bg"])
canvas_frame.pack(fill="both", expand=True, padx=10)

canvas = tk.Canvas(canvas_frame, bg=COLORS["bg"], highlightthickness=0)
scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview,
                         bg=COLORS["bg_light"], troughcolor=COLORS["bg"])
todo_display = tk.Frame(canvas, bg=COLORS["bg"])

todo_display.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=todo_display, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

# Mouse wheel scrolling
def on_mousewheel(event):
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")
canvas.bind_all("<MouseWheel>", on_mousewheel)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Empty state message
empty_label = tk.Label(todo_display, text="🎯\n\nNo tasks yet!\nAdd your first task below.",
                       font=("Arial", 12), bg=COLORS["bg"], fg=COLORS["text_light"],
                       justify="center")

# Grid columns configuration
GRID_COLUMNS = 2

def delete_todo(todo_id):
    global todos
    if show_confirm("Delete Task", "Are you sure you want to delete this task?"):
        todos = [t for t in todos if t["id"] != todo_id]
        refresh_todos()
        show_toast("Task deleted!", "error", 1500)
        if len(todos) < 6:
            todo_btnsADD.pack(pady=5)

def mark_complete(todo_id):
    for todo in todos:
        if todo["id"] == todo_id:
            todo["status"] = not todo["status"]
            status_msg = "Task completed! 🎉" if todo["status"] else "Task marked as active"
            toast_type = "success" if todo["status"] else "info"
            show_toast(status_msg, toast_type, 1500)
            break
    refresh_todos()

def create_todo_card(parent, todo, row, col):
    """Create a styled todo card with action buttons"""
    is_complete = todo["status"]
    card_color = COLORS["card_complete"] if is_complete else COLORS["card_bg"]
    
    # Card frame with border
    card_border = tk.Frame(parent, bg=COLORS["border"], padx=1, pady=1)
    card_border.grid(row=row, column=col, padx=8, pady=8, sticky="nsew")
    
    card = tk.Frame(card_border, bg=card_color)
    card.pack(fill="both", expand=True)
    
    # Inner padding frame
    inner = tk.Frame(card, bg=card_color, padx=15, pady=12)
    inner.pack(fill="both", expand=True)
    
    # Priority indicator (optional visual)
    priority_bar = tk.Frame(inner, bg=COLORS["success"] if is_complete else COLORS["primary"], 
                           width=4, height=40)
    priority_bar.pack(side=tk.LEFT, padx=(0, 12), fill="y")
    
    # Content frame
    content = tk.Frame(inner, bg=card_color)
    content.pack(side=tk.LEFT, fill="both", expand=True)
    
    # Task number badge
    task_num = tk.Label(content, text=f"#{todo['id']}", font=("Arial", 8),
                        bg=card_color, fg=COLORS["text_light"])
    task_num.pack(anchor="w")
    
    # Task text
    task_text = todo["text"]
    display_text = task_text if len(task_text) <= 25 else task_text[:25] + "..."
    
    text_style = ("Arial", 11, "bold overstrike") if is_complete else ("Arial", 11, "bold")
    text_color = COLORS["text_light"] if is_complete else COLORS["text"]
    
    td_item = tk.Label(content, text=display_text, font=text_style,
                       bg=card_color, fg=text_color, wraplength=140, justify="left")
    td_item.pack(anchor="w", pady=(3, 5))
    
    # Status badge
    status_text = "✓ Completed" if is_complete else "○ In Progress"
    status_color = COLORS["success"] if is_complete else COLORS["warning"]
    
    status_frame = tk.Frame(content, bg=status_color, padx=6, pady=2)
    status_frame.pack(anchor="w", pady=(0, 8))
    
    td_status = tk.Label(status_frame, text=status_text, font=("Arial", 8, "bold"),
                         bg=status_color, fg="white")
    td_status.pack()
    
    # Buttons frame
    btn_frame = tk.Frame(content, bg=card_color)
    btn_frame.pack(fill="x", pady=(5, 0))
    
    # Complete/Undo button
    complete_text = "↩ Undo" if is_complete else "✓ Done"
    complete_color = COLORS["text_light"] if is_complete else COLORS["success"]
    btn_complete = tk.Button(btn_frame, text=complete_text, font=("Arial", 9, "bold"),
                             bg=complete_color, fg="white", relief=tk.FLAT,
                             cursor="hand2", width=7, pady=3,
                             activebackground=COLORS["success_hover"],
                             command=lambda tid=todo["id"]: mark_complete(tid))
    btn_complete.pack(side=tk.LEFT, padx=(0, 5))
    
    # Delete button
    btn_delete = tk.Button(btn_frame, text="🗑", font=("Arial", 10),
                           bg=COLORS["danger"], fg="white", relief=tk.FLAT,
                           cursor="hand2", width=3, pady=3,
                           activebackground=COLORS["danger_hover"],
                           command=lambda tid=todo["id"]: delete_todo(tid))
    btn_delete.pack(side=tk.LEFT)
    
    # Hover effects for card
    def on_card_enter(e):
        card.configure(bg=COLORS["card_hover"])
        inner.configure(bg=COLORS["card_hover"])
        content.configure(bg=COLORS["card_hover"])
        btn_frame.configure(bg=COLORS["card_hover"])
    
    def on_card_leave(e):
        card.configure(bg=card_color)
        inner.configure(bg=card_color)
        content.configure(bg=card_color)
        btn_frame.configure(bg=card_color)
    
    card.bind("<Enter>", on_card_enter)
    card.bind("<Leave>", on_card_leave)

def update_progress():
    """Update the progress bar and stats"""
    total = len(todos)
    completed = sum(1 for t in todos if t["status"])
    percentage = (completed / total * 100) if total > 0 else 0
    
    # Update labels
    td_total.config(text=f"{total} task{'s' if total != 1 else ''}")
    td_complete.config(text=f"{completed} done")
    progress_label.config(text=f"Progress: {int(percentage)}%")
    
    # Animate progress bar
    progress_width = int((percentage / 100) * progress_bg.winfo_width()) if progress_bg.winfo_width() > 1 else 0
    progress_bar.place(x=0, y=0, relheight=1, width=max(0, progress_width))

def refresh_todos():
    # Clear existing widgets
    for widget in todo_display.winfo_children():
        widget.destroy()
    
    # Get filtered todos
    filter_type = current_filter.get()
    if filter_type == "active":
        filtered_todos = [t for t in todos if not t["status"]]
    elif filter_type == "completed":
        filtered_todos = [t for t in todos if t["status"]]
    else:
        filtered_todos = todos
    
    # Show empty state if no todos
    if not filtered_todos:
        empty_msg = {
            "all": "🎯\n\nNo tasks yet!\nAdd your first task below.",
            "active": "🎉\n\nNo active tasks!\nAll caught up!",
            "completed": "📝\n\nNo completed tasks yet.\nKeep going!"
        }
        empty_label = tk.Label(todo_display, text=empty_msg.get(filter_type, empty_msg["all"]),
                               font=("Arial", 12), bg=COLORS["bg"], fg=COLORS["text_light"],
                               justify="center", pady=50)
        empty_label.grid(row=0, column=0, columnspan=GRID_COLUMNS, sticky="nsew")
    else:
        # Configure grid columns
        for i in range(GRID_COLUMNS):
            todo_display.columnconfigure(i, weight=1, uniform="col")
        
        # Create todo cards in grid layout
        for index, todo in enumerate(filtered_todos):
            row = index // GRID_COLUMNS
            col = index % GRID_COLUMNS
            create_todo_card(todo_display, todo, row, col)
    
    # Update progress after a short delay to ensure widgets are rendered
    root.after(50, update_progress)
    
    # Reset canvas scroll
    canvas.yview_moveto(0)

# ============= INPUT SECTION =============
input_frame = tk.Frame(main_page, bg=COLORS["bg_light"], pady=20)
input_frame.pack(side=tk.BOTTOM, fill="x")

input_inner = tk.Frame(input_frame, bg=COLORS["bg_light"])
input_inner.pack(fill="x", padx=20)

# Label with icon
label_frame = tk.Frame(input_inner, bg=COLORS["bg_light"])
label_frame.pack(fill="x", pady=(0, 10))

tk.Label(label_frame, text="✏️", font=("Segoe UI Emoji", 12),
         bg=COLORS["bg_light"]).pack(side=tk.LEFT)
tk.Label(label_frame, text=" Add New Task", font=("Arial", 12, "bold"),
         bg=COLORS["bg_light"], fg=COLORS["text"]).pack(side=tk.LEFT)

# Entry with styling
entry_frame = tk.Frame(input_inner, bg=COLORS["border"], padx=2, pady=2)
entry_frame.pack(fill="x")

entry_inner = tk.Frame(entry_frame, bg=COLORS["secondary"])
entry_inner.pack(fill="x")

todo_entry = tk.Entry(entry_inner, width=35, font=("Arial", 12), relief=tk.FLAT,
                      bg=COLORS["secondary"], fg=COLORS["text"], insertbackground=COLORS["text"])
todo_entry.pack(fill="x", ipady=10, padx=10)

# Placeholder text
placeholder_text = "What needs to be done?"

def on_entry_focus_in(e):
    if todo_entry.get() == placeholder_text:
        todo_entry.delete(0, tk.END)
        todo_entry.configure(fg=COLORS["text"])

def on_entry_focus_out(e):
    if not todo_entry.get():
        todo_entry.insert(0, placeholder_text)
        todo_entry.configure(fg=COLORS["text_light"])

todo_entry.insert(0, placeholder_text)
todo_entry.configure(fg=COLORS["text_light"])
todo_entry.bind("<FocusIn>", on_entry_focus_in)
todo_entry.bind("<FocusOut>", on_entry_focus_out)

def add_todo():
    text = todo_entry.get().strip()
    if text and text != placeholder_text:
        new_todo = {
            "id": len(todos) + 1 if not todos else max(t["id"] for t in todos) + 1,
            "text": text,
            "status": False
        }
        todos.append(new_todo)
        todo_entry.delete(0, tk.END)
        refresh_todos()
        show_toast("Task added successfully! ✨", "success", 1500)
        todoLimiter()
    else:
        show_warning("Empty Task", "Please enter a task description!")

def todoLimiter():
    if len(todos) >= 10:
        todo_btnsADD.pack_forget()
        show_warning("Limit Reached", "Maximum of 10 tasks reached!\nComplete some tasks first.")

def todo_deleter():
    if todos:
        if show_confirm("Clear All Tasks", "Are you sure you want to delete ALL tasks?\nThis cannot be undone."):
            todos.clear()
            refresh_todos()
            show_toast("All tasks cleared!", "info", 1500)
            todo_btnsADD.pack(side=tk.LEFT, padx=(0, 10))

# Buttons container
btn_container = tk.Frame(input_inner, bg=COLORS["bg_light"])
btn_container.pack(fill="x", pady=(15, 0))

todo_btnsADD = tk.Button(btn_container, text="➕ Add Task", command=add_todo,
                         bg=COLORS["primary"], fg="white",
                         font=("Arial", 11, "bold"), relief=tk.FLAT, cursor="hand2",
                         padx=20, pady=8, activebackground=COLORS["primary_hover"])
todo_btnsADD.pack(side=tk.LEFT, padx=(0, 10))

todo_reset = tk.Button(btn_container, text="🗑 Clear All", command=todo_deleter,
                       bg=COLORS["danger"], fg="white", font=("Arial", 10),
                       relief=tk.FLAT, cursor="hand2", padx=15, pady=8,
                       activebackground=COLORS["danger_hover"])
todo_reset.pack(side=tk.LEFT)

# Keyboard shortcut hint
hint_label = tk.Label(btn_container, text="Press Enter to add", font=("Arial", 9),
                      bg=COLORS["bg_light"], fg=COLORS["text_light"])
hint_label.pack(side=tk.RIGHT)

# Hover effects for buttons
def create_hover_effect(button, normal_color, hover_color):
    button.bind("<Enter>", lambda e: button.configure(bg=hover_color))
    button.bind("<Leave>", lambda e: button.configure(bg=normal_color))

create_hover_effect(todo_btnsADD, COLORS["primary"], COLORS["primary_hover"])
create_hover_effect(todo_reset, COLORS["danger"], COLORS["danger_hover"])

# Bind Enter key to add todo
def on_enter_key(e):
    if todo_entry.get() != placeholder_text:
        add_todo()

todo_entry.bind("<Return>", on_enter_key)

# ============= START APPLICATION =============
root.mainloop()
