# Import the necessary libraries
import tkinter as tk  # GUI library
# A "GUI" stands for "Graphical User Interface", which is a type of interface that allows users to interact with a
# computer program or system through visual elements such as buttons, menus, and icons.
from tkinter import messagebox  # For displaying message boxes
import pandas as pd  # For handling CSV files
import os  # For checking if a file exists
import datetime  # For getting the current date
import calendar  # For getting the number of days in a month
from PIL import Image, ImageTk  # For handling images


# Define the Expense class
class Expense:
    def __init__(self, name, category, amount):  # Initialize an Expense object
        # In Python, "self" is a reference to the current instance of a class. It is used to access variables that
        # belong to the class and to bind the attributes with the given arguments.
        self.name = name  # The name of the expense
        self.category = category  # The category of the expense
        self.amount = amount  # The amount of the expense


# Define the ExpenseTracker class
class ExpenseTracker:
    def __init__(self, root):  # Initialize an ExpenseTracker object
        # In Python, a "root" window is the main window of a graphical user interface (GUI) program. It is the top-level
        # window that contains all other GUI elements, such as buttons, labels, and text boxes.
        # In the Python GUI toolkit "Tkinter", the "Tk()" class is used to create a root window. The root window
        # is then used to add other widgets to the GUI.
        self.root = root  # The root window
        self.root.title("Expense Tracker")  # Set the title of the window

        # Set the path for the expense file
        self.expense_file_path = "expenses.csv"

        # Create the expense file if it doesn't exist
        if not os.path.isfile(self.expense_file_path):
            open(self.expense_file_path, 'a').close()

        # Calculate the initial budget
        self.budget = self.calculate_initial_budget()

        # Load and set the background image
        img = Image.open("poz1.jpg")
        img = img.resize((800, 600), Image.LANCZOS)
        # The second argument to the "resize()" method is the resampling filter to use when resizing the image.
        # The "Image.LANCZOS" filter is a high-quality downsampling filter that is well-suited for photographic images.
        img = ImageTk.PhotoImage(img)
        # The "PhotoImage" constructor takes an image as its argument and returns a new "PhotoImage" object that can be
        # used to display the image in a "Tkinter" window. In this case, the "img" variable is passed as an argument to
        # the "PhotoImage" constructor, so the "PhotoImage" object created will display the same image as the "img" variable.
        self.background_image = img
        background_label = tk.Label(root, image=self.background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        # This line of code uses the "place()" method to position the "background_label" widget in the top-left corner
        # of its parent widget, with a width and height that are proportional to the size of the parent widget.
        # Specifically, the x and y arguments are set to 0, which positions the widget in the top-left corner of its
        # parent widget. The "relwidth" and "relheight" arguments are set to 1, which means that the width and height of
        # the widget will be equal to the width and height of its parent widget, respectively.

        # Create labels, entries, dropdowns, and buttons for the GUI
        self.name_label = tk.Label(root, text="Enter expense name:")
        self.name_entry = tk.Entry(root)
        # This line of code creates a new instance of the "Entry" widget from the "tk" module, which is used to create a
        # single-line text box in a Tkinter GUI. The "name_entry" variable is an instance of the "Entry" class,
        # which represents a text box that can be used to enter or display a single line of text.
        self.amount_label = tk.Label(root, text="Enter expense amount:")
        self.amount_entry = tk.Entry(root)
        self.category_label = tk.Label(root, text="Select a category:")
        self.category_var = tk.StringVar(root)
        self.category_dropdown = tk.OptionMenu(root, self.category_var, "Food", "Home", "Work", "Fun")
        self.submit_button = tk.Button(root, text="Submit Expense", command=self.submit_expense)
        self.budget_label = tk.Label(root, text=f"Current Budget: {self.budget}")
        self.daily_budget_label = tk.Label(root, text=f"Daily Budget: {self.calculate_daily_budget()}")
        self.expense_summary_frame = tk.Frame(root)

        # Pack the GUI elements into the root window
        # In Python, pack() organizes widgets in blocks before placing them in the parent widget.
        # In Python, "pady" is an option that can be used to add padding to a widget in the vertical direction.
        # It specifies the amount of space to be added above and below the widget.
        self.name_label.pack(pady=10)
        self.name_entry.pack(pady=10)
        self.amount_label.pack(pady=10)
        self.amount_entry.pack(pady=10)
        self.category_label.pack(pady=10)
        self.category_dropdown.pack(pady=10)
        self.submit_button.pack(pady=10)
        self.budget_label.pack(pady=10)
        self.daily_budget_label.pack(pady=10)
        self.expense_summary_frame.pack(pady=10)

        # Update the expense summary
        self.update_expense_summary()

    # Calculate the initial budget
    def calculate_initial_budget(self):
        try:
            df = pd.read_csv(self.expense_file_path, names=['name', 'amount', 'category'])  # Read the expense file
            total_expense = df['amount'].sum()  # Calculate the total expense
        except pd.errors.EmptyDataError:  # Handle the case when the CSV file is empty
            total_expense = 0
        return 2000 - total_expense  # Return the initial budget

    # Calculate the daily budget
    def calculate_daily_budget(self):
        now = datetime.datetime.now()  # Get the current date
        days_in_month = calendar.monthrange(now.year, now.month)[1]  # Get the number of days in the current month
        remaining_days = days_in_month - now.day  # Calculate the remaining days in the month
        daily_budget = self.budget / remaining_days if remaining_days > 0 else 0  # Calculate the daily budget
        return round(daily_budget, 2)  # Return the daily budget

    # Update the expense summary
    def update_expense_summary(self):
        for widget in self.expense_summary_frame.winfo_children():
            widget.destroy()  # Remove all widgets from the expense summary frame
        try:
            df = pd.read_csv(self.expense_file_path, names=['name', 'amount', 'category'])  # Read the expense file
            for index, row in df.iterrows():  # Iterate over the rows in the DataFrame
                # Create a label for the expense
                expense_label = tk.Label(self.expense_summary_frame, text=f"{row['name']}: {row['amount']} ({row['category']})")
                # Create a delete button for the expense
                delete_button = tk.Button(self.expense_summary_frame, text="Delete", command=lambda expense_name=row['name']: self.delete_expense(expense_name))
                # In this context, "lambda" is used to define an anonymous function that takes one argument
                # "(expense_name=row['name'])" and returns the result of calling the "delete_expense" method with
                # "expense_name" as its argument.The "delete_expense" method is called on the object "self"
                # Using a lambda function allows you to define the function inline, without having to give it a name.
                # This can be useful when you only need to use the function once and don’t want to clutter your code
                # with unnecessary function definitions.
                expense_label.pack(side="left")  # Pack the label into the expense summary frame
                delete_button.pack(side="left")  # Pack the delete button into the expense summary frame
        except pd.errors.EmptyDataError:  # Handle the case when the CSV file is empty
            pass

    # Submit an expense
    def submit_expense(self):
        expense_name = self.name_entry.get()  # Get the name of the expense from the entry
        expense_amount = float(self.amount_entry.get())  # Get the amount of the expense from the entry
        selected_category = self.category_var.get()  # Get the selected category from the dropdown
        new_expense = Expense(name=expense_name, category=selected_category, amount=expense_amount)  # Create a new Expense object
        self.save_expense_to_file(new_expense, self.expense_file_path)  # Save the expense to the file
        self.update_budget()  # Update the budget
        self.update_expense_summary()  # Update the expense summary
        messagebox.showinfo("Success", "Expense saved successfully!")  # Show a success message

    # Delete an expense
    def delete_expense(self, expense_name):
        # Ask for confirmation to delete the expense
        if messagebox.askyesno("Confirmation", f"Are you sure you want to delete {expense_name}?"):
            self.remove_expense_from_file(expense_name, self.expense_file_path)  # Remove the expense from the file
            self.update_budget()  # Update the budget
            self.update_expense_summary()  # Update the expense summary
            messagebox.showinfo("Success", "Expense deleted successfully!")  # Show a success message

    # Save an expense to the file
    def save_expense_to_file(self, expense: Expense, expense_file_path):
        with open(expense_file_path, "a") as f:  # Open the expense file in append mode
            f.write(f"{expense.name},{expense.amount},{expense.category}\n")  # Write the expense to the file

    # Remove an expense from the file
    def remove_expense_from_file(self, expense_name, expense_file_path):
        df = pd.read_csv(expense_file_path, names=['name', 'amount', 'category'])  # Read the expense file
        df = df[df.name != expense_name]  # Remove the expense from the DataFrame
        df.to_csv(expense_file_path, index=False, header=False)  # Write the DataFrame back to the file
        # The index argument is set to False, which means that the row index labels will not be included in the
        # output file. The header argument is also set to False, which means that the column names will not be
        # included in the output file.

    # Update the budget
    def update_budget(self):
        self.budget = self.calculate_initial_budget()  # Calculate the budget
        self.budget_label.config(text=f"Current Budget: {self.budget}")  # Update the budget label
        self.daily_budget_label.config(text=f"Daily Budget: {self.calculate_daily_budget()}")  # Update the daily budget label


if __name__ == "__main__":
    # Create the root window and start the application
    root = tk.Tk()
    # Set the window size
    root.geometry("800x600")  # Set window size to 800x600
    app = ExpenseTracker(root)
    # This line of code creates an instance of the ExpenseTracker class from the ExpenseTracker module and assigns
    # it to the app variable. The ExpenseTracker constructor takes one argument: the parent widget. In this case,
    # the root widget is being used as the parent widget, so the ExpenseTracker object will be placed inside the
    # root window. Once the ExpenseTracker object has been created, it can be used to display the expense tracker
    # application in the "Tkinter" window by calling its "mainloop()" method.
    root.mainloop()
    # In Python, "mainloop()" is a method that starts the event loop of a graphical user interface (GUI) application.
    # It listens for events such as button clicks or key-presses and blocks any code that comes after it from running
    # until the window is closed.
    # In the Python GUI toolkit "Tkinter", "mainloop()" is used to run the event loop of the application.
    # It is an infinite loop that keeps the window open and waits for user input. The loop runs until the window is
    # closed by the user.
