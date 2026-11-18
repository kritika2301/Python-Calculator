
import tkinter as tk
import math

# Main window
root = tk.Tk()
root.title("Minimal Calculator")
root.geometry("360x580")
root.configure(bg="#171717")
root.resizable(False, False)

# Colour theme
BG = "#171717"
DISPLAY_BG = "#222222"
NUMBER_BG = "#292929"
SPECIAL_BG = "#383838"
OPERATOR_BG = "#444444"
EQUAL_BG = "#e58a32"
TEXT_COLOR = "#ffffff"
HOVER_COLOR = "#555555"

# Calculator display
display = tk.Entry(
    root,
    font=("Segoe UI", 30),
    bg=DISPLAY_BG,
    fg=TEXT_COLOR,
    insertbackground="white",
    justify="right",
    bd=0
)

display.pack(
    pady=(35, 20),
    padx=20,
    fill="x",
    ipady=18
)


# Calculator functionality
def button_click(value):

    if value == "C":
        display.delete(0, tk.END)

    elif value == "DEL":
        current = display.get()
        if current:
            display.delete(len(current) - 1, tk.END)

    elif value in ["%", "√", "x²"]:

        try:
            number = float(display.get())

            if value == "%":
                result = number / 100
            elif value == "√":
                result = math.sqrt(number)
            else:
                result = number ** 2

            display.delete(0, tk.END)
            display.insert(tk.END, str(result))

        except Exception:
            display.delete(0, tk.END)
            display.insert(tk.END, "Error")

    elif value == "=":

        try:
            expression = display.get()
            allowed = "0123456789+-*/.() "

            if not expression or any(c not in allowed for c in expression):
                raise ValueError("Invalid expression")

            result = eval(expression, {"__builtins__": {}}, {})

            display.delete(0, tk.END)
            display.insert(tk.END, str(result))

        except ZeroDivisionError:
            display.delete(0, tk.END)
            display.insert(tk.END, "Cannot divide by zero")

        except Exception:
            display.delete(0, tk.END)
            display.insert(tk.END, "Error")

    else:
        display.insert(tk.END, value)


# Keyboard functionality
def keyboard_input(event):

    if event.char in "0123456789+-*/.":
        button_click(event.char)

    elif event.keysym == "Return":
        button_click("=")

    elif event.keysym == "BackSpace":
        button_click("DEL")

    elif event.keysym == "Escape":
        button_click("C")


# Button frame
button_frame = tk.Frame(root, bg=BG)
button_frame.pack(padx=15, pady=10, fill="both", expand=True)

# Button layout
buttons = [
    ["C", "DEL", "%", "√"],
    ["7", "8", "9", "/"],
    ["4", "5", "6", "*"],
    ["1", "2", "3", "-"],
    ["x²", "0", ".", "+"],
    ["="]
]


# Button hover effects
def on_enter(event):
    event.widget.config(bg=HOVER_COLOR)


def on_leave(event):
    event.widget.config(bg=event.widget.default_color)


# Create buttons
for row_index, row in enumerate(buttons):

    for col_index, value in enumerate(row):

        if value == "=":
            color = EQUAL_BG
        elif value in ["+", "-", "*", "/"]:
            color = OPERATOR_BG
        elif value in ["C", "DEL", "%", "√", "x²"]:
            color = SPECIAL_BG
        else:
            color = NUMBER_BG

        button = tk.Button(
            button_frame,
            text=value,
            font=("Segoe UI", 16, "bold"),
            bg=color,
            fg=TEXT_COLOR,
            activebackground=HOVER_COLOR,
            activeforeground=TEXT_COLOR,
            bd=0,
            relief="flat",
            cursor="hand2",
            command=lambda v=value: button_click(v)
        )

        button.default_color = color

        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)

        if value == "=":
            button.grid(
                row=row_index,
                column=0,
                columnspan=4,
                padx=5,
                pady=5,
                sticky="nsew"
            )
        else:
            button.grid(
                row=row_index,
                column=col_index,
                padx=5,
                pady=5,
                sticky="nsew"
            )


# Make buttons expand evenly
for i in range(4):
    button_frame.columnconfigure(i, weight=1)

for i in range(6):
    button_frame.rowconfigure(i, weight=1)


# Keyboard support
root.bind_all("<Key>", keyboard_input)

# Start calculator
root.mainloop()
