import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pandastable import Table, TableModel
import pandas as pd
import numpy as np

class DataCleaningApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Data Cleaning App")
        self.geometry("800x600")

        self.df = None

        self.create_menu()
        self.create_widgets()

    def create_menu(self):
        self.menu_bar = tk.Menu(self)
        
        # File Menu
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="Browse", command=self.browse_file)
        self.file_menu.add_command(label="Save", command=self.open_save_file_window)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.quit)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        
        self.config(menu=self.menu_bar)

    def create_widgets(self):
        self.show_button = tk.Button(self, text="Show File", command=self.show_file)
        self.show_button.pack(pady=5)

        self.clean_button = tk.Button(self, text="Replace Missing Values", command=self.clean_data)
        self.clean_button.pack(pady=5)

        self.selective_cleaning_button = tk.Button(self, text="Selective Cleaning", command=self.open_selective_cleaning_window)
        self.selective_cleaning_button.pack(pady=5)

        self.remove_column_button = tk.Button(self, text="Remove Column", command=self.open_remove_column_window)
        self.remove_column_button.pack(pady=5)


        self.create_attribute_button = tk.Button(self, text="Create Attribute", command=self.open_create_attribute_window)
        self.create_attribute_button.pack(pady=5)

        # self.convert_to_numeric_button = tk.Button(self, text="Convert to Numeric", command=self.open_convert_to_numeric_window)
        # self.convert_to_numeric_button.pack(pady=5)

        self.value_percentages_button = tk.Button(self, text="Value Percentages", command=self.open_value_percentages_window)
        self.value_percentages_button.pack(pady=5)

        self.console = tk.Text(self, height=10, wrap=tk.WORD)
        self.console.pack(fill=tk.BOTH, expand=True)

    def write_console(self, message):
        self.console.insert(tk.END, message + "\n")

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            try:
                self.df = pd.read_csv(file_path)
                if 'date' in self.df.columns:
                    self.df['date'] = pd.to_datetime(self.df['date'])  # Parsing date column
                self.write_console("File read successfully.")
            except Exception as e:
                self.write_console(f"Error: {str(e)}")
    def show_file(self):
        if self.df is not None:
            show_data_window = tk.Toplevel()
            show_data_window.title("Show Data Table")

            # Use the Table widget from pandastable to display the DataFrame
            pt = Table(show_data_window, dataframe=self.df)
            pt.show()
            self.write_console("File displayed successfully.")
        else:
            self.write_console("Please select a file first.")


    def clean_data(self):
        if self.df is not None:
            try:
                # Replace empty strings and strings containing only a space with NaN
                self.df.replace(['', ' '], np.nan, inplace=True)
                # Replace NaN values with question mark
                self.df.fillna('?', inplace=True)
                self.write_console("Missing values were replaced with '?' successfully.")
            except Exception as e:
                self.write_console(f"Error: {str(e)}")
        else:
            self.write_console("Please select a file and show its content first.")
    # def clean_data(self):
    #     if self.df is not None:
    #         try:
    #             missing_percentages = self.df.isnull().mean() * 100

    #             for col in self.df.columns:
    #                 missing_percentage = missing_percentages[col]
    #                 if pd.api.types.is_numeric_dtype(self.df[col]) and missing_percentage < 15:
    #                     self.df[col].fillna(self.df[col].mean(), inplace=True)
    #                 if missing_percentage > 60:
    #                     self.df.drop(columns=[col], inplace=True)

    #             self.write_console("Data cleaned successfully.")
    #         except Exception as e:
    #             self.write_console(f"Error: {str(e)}")
    #     else:
    #         self.write_console("Please select a file and show its content first.")
    
    def open_selective_cleaning_window(self):
        if self.df is not None:
            columns = self.df.columns
            selective_cleaning_window = SelectiveCleaningWindow(self, columns)
            selective_cleaning_window.mainloop()
        else:
            self.write_console("Please select a file first.")

    def open_remove_column_window(self):
        if self.df is not None:
            columns = self.df.columns
            remove_column_window = RemoveColumnWindow(self, columns)
        else:
            self.write_console("Please select a file first.")
    
    # def open_correlation_window(self):
    #     if self.df is not None:
    #         columns = self.df.columns
    #         correlation_window = CorrelationWindow(self, columns)
    #     else:
    #         self.write_console("Please select a file first.")
    
    def open_create_attribute_window(self):
        if self.df is not None:
            columns = self.df.columns
            create_attribute_window = CreateAttributeWindow(self, columns)
        else:
            self.write_console("Please select a file first.")
    def open_save_file_window(self):
        save_file_window = SaveFileWindow(self)
        save_file_window.mainloop()

    def open_convert_to_numeric_window(self):
        if self.df is not None:
            columns_with_string_values = [col for col in self.df.columns if self.df[col].dtype == 'object']
            if columns_with_string_values:
                convert_to_numeric_window = ConvertToNumericWindow(self, columns_with_string_values)
                convert_to_numeric_window.mainloop()
            else:
                self.write_console("No columns with string values found.")
        else:
            self.write_console("Please select a file first.")
    
    def open_value_percentages_window(self):
        if self.df is not None:
            columns = list(self.df.columns)  # Convert Index to list of columns
            if columns:
                value_percentages_window = ValuePercentagesWindow(self, columns)
            else:
                self.write_console("No columns found in the dataset.")
        else:
            self.write_console("Please select a file first.")

class SaveFileWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Save File")
        self.geometry("300x150")

        self.parent = parent

        self.save_location_var = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Save location:").pack(pady=5)
        tk.Radiobutton(self, text="Local", variable=self.save_location_var, value="local").pack(pady=5)
        tk.Radiobutton(self, text="Upload to DB", variable=self.save_location_var, value="db").pack(pady=5)

        self.save_button = tk.Button(self, text="Save", command=self.save_file)
        self.save_button.pack(pady=10)

    def save_file(self):
        save_location = self.save_location_var.get()
        if save_location == "local":
            file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
            if file_path:
                try:
                    self.parent.df.to_csv(file_path, index=False)
                    self.parent.write_console("File saved locally successfully.")
                except Exception as e:
                    self.parent.write_console(f"Error: {str(e)}")
        elif save_location == "db":
            # You need to provide MongoDB connection details here
            try:
                client = pymongo.MongoClient("mongodb://localhost:27017/")
                db = client["mydatabase"]
                collection = db["mycollection"]
                records = self.parent.df.to_dict(orient='records')
                collection.insert_many(records)
                self.parent.write_console("File uploaded to MongoDB successfully.")
            except Exception as e:
                self.parent.write_console(f"Error: {str(e)}")  
class SelectiveCleaningWindow(tk.Toplevel):
    def __init__(self, parent, columns):
        super().__init__(parent)
        self.title("Selective Cleaning")
        self.geometry("400x300")

        self.parent = parent
        self.columns = columns

        self.replacement_options = ["Column Mean", "0", "Most Common Value", "Median", "None"]

        self.create_widgets()

    def create_widgets(self):
        self.column_label = tk.Label(self, text="Select Column:")
        self.column_label.pack(pady=5)

        # Process column names to remove extra spaces and quotes
        self.columns = [col.strip().strip("'") for col in self.columns]

        self.column_var = tk.StringVar(self)
        self.column_dropdown = ttk.Combobox(self, textvariable=self.column_var, values=self.columns)
        self.column_dropdown.pack(pady=5)

        self.replacement_label = tk.Label(self, text="Select Replacement Value:")
        self.replacement_label.pack(pady=5)

        self.replacement_var = tk.StringVar(self)
        self.replacement_dropdown = ttk.Combobox(self, textvariable=self.replacement_var, values=self.replacement_options)
        self.replacement_dropdown.pack(pady=5)

        self.condition_label = tk.Label(self, text="Enter Condition (e.g., == 0):")
        self.condition_label.pack(pady=5)

        self.condition_entry = tk.Entry(self)
        self.condition_entry.pack(pady=5)

        self.console = tk.Text(self, height=8, width=50, wrap=tk.WORD)
        self.console.pack(fill=tk.BOTH, expand=True)

        self.clean_button = tk.Button(self, text="Clean Data", command=self.clean_data)
        self.clean_button.pack(pady=10)

    def write_console(self, message):
        self.console.insert(tk.END, message + "\n")

    def clean_data(self):
        selected_column = self.column_var.get()
        condition = self.condition_entry.get()
        replacement_option = self.replacement_var.get()

        if selected_column and condition and replacement_option:
            try:
                condition = f"({selected_column}{condition})"
                if replacement_option == "Column Mean":
                    replacement_value = self.parent.df[selected_column].mean()
                elif replacement_option == "0":
                    replacement_value = 0
                elif replacement_option == "Most Common Value":
                    replacement_value = self.parent.df[selected_column].value_counts().idxmax()
                elif replacement_option == "Median":
                    replacement_value = self.parent.df[selected_column].median()
                elif replacement_option == "None":
                    replacement_value = None

                self.parent.df.loc[self.parent.df.eval(condition), selected_column] = replacement_value
                self.write_console(f"Data cleaned successfully for {selected_column} based on condition: {condition}.")
            except Exception as e:
                self.write_console(f"Error: {str(e)}")
        else:
            self.write_console("Please select a column, replacement value, and enter a condition.")
class RemoveColumnWindow(tk.Toplevel):
    def __init__(self, parent, columns):
        super().__init__(parent)
        self.title("Remove Columns")
        self.geometry("300x400")

        self.parent = parent
        self.columns = columns

        self.selected_columns = []

        self.create_widgets()

    def create_widgets(self):
        self.column_label = tk.Label(self, text="Select Columns to Remove:")
        self.column_label.pack(pady=10)

        self.column_vars = []
        for column in self.columns:
            var = tk.BooleanVar()
            var.set(False)
            self.column_vars.append(var)
            checkbox = tk.Checkbutton(self, text=column, variable=var)
            checkbox.pack(anchor=tk.W, padx=10)

        self.remove_button = tk.Button(self, text="Remove", command=self.remove_columns)
        self.remove_button.pack(pady=10)

    def remove_columns(self):
        self.selected_columns = [self.columns[i] for i, var in enumerate(self.column_vars) if var.get()]
        if self.selected_columns:
            self.parent.df.drop(columns=self.selected_columns, inplace=True)
            self.parent.show_file()
            self.destroy()
        else:
            messagebox.showinfo("No Selection", "Please select columns to remove.")

class CreateAttributeWindow(tk.Toplevel):
    def __init__(self, parent, columns):
        super().__init__(parent)
        self.title("Create Attribute")
        self.geometry("400x400")

        self.parent = parent
        self.columns = [col.strip().strip("'") for col in columns]  # Adjust column names

        self.combination_methods = ["Concat", "Sum", "Subtract", "Divide", "Multiply"]

        self.new_column_name_var = tk.StringVar(self)
        self.column1_var = tk.StringVar(self)
        self.column2_var = tk.StringVar(self)
        self.combination_method_var = tk.StringVar(self)

        self.create_widgets()

    def create_widgets(self):
        self.new_column_label = tk.Label(self, text="New Column Name:")
        self.new_column_label.pack(pady=5)

        self.new_column_entry = tk.Entry(self, textvariable=self.new_column_name_var)
        self.new_column_entry.pack(pady=5)

        self.column1_label = tk.Label(self, text="Select First Column:")
        self.column1_label.pack(pady=5)

        self.column1_dropdown = ttk.Combobox(self, textvariable=self.column1_var, values=self.columns)
        self.column1_dropdown.pack(pady=5)

        self.column2_label = tk.Label(self, text="Select Second Column:")
        self.column2_label.pack(pady=5)

        self.column2_dropdown = ttk.Combobox(self, textvariable=self.column2_var, values=self.columns)
        self.column2_dropdown.pack(pady=5)

        self.combination_method_label = tk.Label(self, text="Select Combination Method:")
        self.combination_method_label.pack(pady=5)

        self.combination_method_dropdown = ttk.Combobox(self, textvariable=self.combination_method_var, values=self.combination_methods)
        self.combination_method_dropdown.pack(pady=5)

        self.create_button = tk.Button(self, text="Create", command=self.create_column)
        self.create_button.pack(pady=10)


    def create_column(self):
        new_column_name = self.new_column_name_var.get()
        column1 = self.column1_var.get()
        column2 = self.column2_var.get()
        combination_method = self.combination_method_var.get()

        if new_column_name and column1 and column2 and combination_method:
            try:
                if combination_method == "Concat":
                    self.parent.df[new_column_name] = self.parent.df[column1].astype(str) + self.parent.df[column2].astype(str)
                elif combination_method == "Sum":
                    self.parent.df[new_column_name] = self.parent.df[column1] + self.parent.df[column2]
                elif combination_method == "Subtract":
                    self.parent.df[new_column_name] = self.parent.df[column1] - self.parent.df[column2]
                elif combination_method == "Divide":
                    self.parent.df[new_column_name] = self.parent.df[column1] / self.parent.df[column2]
                elif combination_method == "Multiply":
                    self.parent.df[new_column_name] = self.parent.df[column1] * self.parent.df[column2]

                self.parent.write_console(f"New column '{new_column_name}' created successfully.")
                self.columns = self.parent.df.columns.tolist()  # Update column names
                self.update_dropdowns()
            except Exception as e:
                self.parent.write_console(f"Error: {str(e)}")
        else:
            self.parent.write_console("Please fill all fields.")
    def update_dropdowns(self):
        self.columns = [col.strip().strip("'") for col in self.columns]
        self.column1_dropdown['values'] = self.columns
        self.column2_dropdown['values'] = self.columns
class ConvertToNumericWindow(tk.Toplevel):
    def __init__(self, parent, columns):
        super().__init__(parent)
        self.title("Convert to Numeric")
        self.geometry("300x400")

        self.parent = parent
        self.columns = columns

        self.selected_column = tk.StringVar()
        self.selected_column.trace("w", self.update_unique_values)

        self.unique_values = {}
        self.numeric_scores = {}

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Select Column:").pack(pady=5)
        self.column_dropdown = ttk.Combobox(self, textvariable=self.selected_column, values=self.columns)
        self.column_dropdown.pack(pady=5)

        self.console_frame = tk.Frame(self)
        self.console_frame.pack(fill=tk.BOTH, expand=True)

        self.confirm_button = tk.Button(self, text="Confirm", command=self.convert_to_numeric)
        self.confirm_button.pack(pady=10)

    def update_unique_values(self, *args):
        self.console_frame.destroy()

        self.console_frame = tk.Frame(self)
        self.console_frame.pack(fill=tk.BOTH, expand=True)

        column = self.selected_column.get()
        if column:
            unique_values = self.parent.df[column].unique()
            self.unique_values = {value: tk.Entry(self.console_frame) for value in unique_values}

            for i, (value, entry) in enumerate(self.unique_values.items()):
                tk.Label(self.console_frame, text=value).grid(row=i, column=0, padx=5, pady=2)
                entry.grid(row=i, column=1, padx=5, pady=2)

class ValuePercentagesWindow(tk.Toplevel):
    def __init__(self, parent, columns):
        super().__init__(parent)
        self.title("Value Percentages")
        self.geometry("300x400")

        self.parent = parent
        self.columns = columns

        self.selected_column = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Select Column:").pack(pady=5)
        self.column_dropdown = ttk.Combobox(self, textvariable=self.selected_column, values=self.columns)
        self.column_dropdown.pack(pady=5)

        self.console = tk.Text(self, height=10, wrap=tk.WORD)
        self.console.pack(fill=tk.BOTH, expand=True)

        self.show_percentages_button = tk.Button(self, text="Show Percentages", command=self.show_percentages)
        self.show_percentages_button.pack(pady=10)

    def show_percentages(self):
        column = self.selected_column.get()
        if column:
            unique_values = self.parent.df[column].value_counts(normalize=True)

            self.console.delete(1.0, tk.END)
            for value, percentage in unique_values.items():
                self.console.insert(tk.END, f"{value}: {percentage*100:.2f}%\n")
        else:
            messagebox.showinfo("Error", "Please select a column.")



if __name__ == "__main__":
    app = DataCleaningApp()
    app.mainloop()
