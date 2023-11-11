import tkinter as tk
from tkinter import PhotoImage, Toplevel, Scrollbar, Text
from PIL import Image, ImageTk
import math
import os
import re  # Import the regular expression module

class CalculatorApp:
    def __init__(self, root):
        self.root = root
        root.title("Calculator App")
        root.configure(bg='grey')
        
        self.operators = ["/", "*", "+", "-"]
        self.scientific_functions = ["sin", "cos", "tan", "exp", "log", "sqrt", "ln"]
        self.last_was_operator = None
        self.last_button = None
        self.solution = tk.StringVar()
        self.history = []  # Store history of calculations
        self.create_ui()
        self.last_number = ""  # To store the last entered number

    def create_ui(self):
        # Create the user interface
        
        # Entry widget to display the calculation
        self.solution_entry = tk.Entry(self.root, textvariable=self.solution, font=('Helvetica', 20), bd=10, insertwidth=4, borderwidth=6, bg='black', fg='black', state='readonly')
        self.solution_entry.grid(row=0, column=0, columnspan=4, sticky='nsew')
        
        # Define the layout of buttons
        buttons = [
            ["7", "8", "9", "/"],
            ["4", "5", "6", "*"],
            ["1", "2", "3", "+"],
            [".", "0", "DEL", "-"],
            ["sin", "cos", "tan", "exp"],
            ["log", "sqrt", "ln", "AC"],
            ["History", "(", ")", "="],
          # Add a "History" button
        ]
        
        for i, row in enumerate(buttons):
            for j, label in enumerate(row):
                if label == "=":
                    # Create an "=" button with specific properties
                    button = tk.Button(self.root, text=label, padx=20, pady=20, font=('Helvetica', 15), bg='grey', fg='white', command=lambda lbl=label: self.on_button_press(lbl))
                    button.grid(row=i + 1, column=j, columnspan=2, sticky='nsew')
                elif label == "History":
                    # Create a "History" button with specific properties
                    button = tk.Button(self.root, text=label, padx=20, pady=20, font=('Helvetica', 15), bg='grey', fg='white', command=self.show_history)
                    button.grid(row=i + 1, column=j, sticky='nsew')
                else:
                    # Create other buttons with specific properties
                    button = tk.Button(self.root, text=label, padx=20, pady=20, font=('Helvetica', 15), bg='grey', fg='white', command=lambda lbl=label: self.on_button_press(lbl))
                    button.grid(row=i + 1, column=j, sticky='nsew')
                
                # Configure grid weights for buttons to make them expand
                self.root.grid_rowconfigure(i + 1, weight=1)
                self.root.grid_columnconfigure(j, weight=1)
                
        # Configure grid weights for the display textbox
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
                
        self.solution_entry.focus_set()  # Set focus to the text entry
                
         # Set the application icon
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cal1_icon.png")
        if os.path.exists(icon_path):
            icon_image = Image.open(icon_path)
            icon_photo = ImageTk.PhotoImage(icon_image)
            self.root.iconphoto(True, icon_photo)
            
            
                
    def on_button_press(self, button_text):
        current = self.solution.get()
        
        if button_text == 'DEL':
            # Remove the last character from the current expression
            current = current[:-1]
            self.solution.set(current)
        elif button_text == 'AC':
            # Clear all (AC) - Clear the entire expression
            self.solution.set("")
        elif button_text in self.scientific_functions:
            self.solution.set(current + button_text + "(")
        elif button_text == "=":
            try:
                result = self.calculate_result(current)
                # Round the result to 4 decimal places
                result = round(result, 4)
                self.solution.set(result)
                self.history.append(f"{current} = {result}")  # Add to calculation history
            except:
                self.solution.set("Error")
        else:
            if button_text in self.operators:
                # Track the last entered number
                self.last_number = current.split()[-1]
            new_text = current + button_text
            self.solution.set(new_text)
        
        self.last_button = button_text
        self.last_was_operator = self.last_button in self.operators

    def show_history(self):
        history_window = Toplevel(self.root)
        history_window.title("Calculation History")
        
        # Create a Text widget to display the history
        history_text = Text(history_window, wrap=tk.WORD, height=20, width=50)
        history_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Add a scrollbar for the Text widget
        scrollbar = Scrollbar(history_window, command=history_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        history_text.config(yscrollcommand=scrollbar.set)
        
        # Populate the Text widget with the calculation history
        for entry in self.history:
            history_text.insert(tk.END, entry + "\n")
        history_text.config(state=tk.DISABLED)  # Disable editing of the history
        
    def calculate_result(self, expression):
        try:
            for func in self.scientific_functions:
                expression = expression.replace(func, "math." + func)
            result = eval(expression)
            return result
        except:
            return "Error"

if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()
