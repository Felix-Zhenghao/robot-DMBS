import tkinter as tk
from tkinter import ttk, messagebox

# Subtasks in the GUI refers to specific queries that users will select. 
SUBTASKS = {
    "Basic Tasks": ["Stack", "Stack Three"],
    "Contact-Rich Tasks": ["Square", "Threading", "Coffee", "Three Piece Assembly", "Hammer Cleanup", "Mug Cleanup"],
    "Long-Horizon Tasks": ["Kitchen", "Nut Assembly", "Pick Place", "Coffee Preparation"],
    "Mobile Manipulation Tasks": ["Mobile Kitchen"],
    "Factory Tasks": ["Nut-and-Bolt Assembly", "Gear Assembly", "Frame Assembly"]
}

def show_task_category_page():
    """
    Display the initial page for selecting a task category.

    This page includes a welcome message, instructions, and a dropdown menu
    to select a task category. A "Next" button is included to proceed.
    """
    for widget in root.winfo_children():
        widget.destroy()

    task_category_frame = ttk.Frame(root)
    task_category_frame.pack(expand=True)

    ttk.Label(
        task_category_frame,
        text="Welcome to the Robot Demonstration Database!",
        font=("Helvetica", 18, "bold")
    ).pack(pady=10)
    ttk.Label(
        task_category_frame,
        text="This application allows you to interact with the robot demonstration database.\nSelect a Task Category to start.",
        font=("Helvetica", 12)
    ).pack(pady=10)

    ttk.Label(task_category_frame, text="Select Task Category:", font=("Helvetica", 12, "bold")).pack(pady=10)
    global category_combo
    category_combo = ttk.Combobox(task_category_frame, values=list(SUBTASKS.keys()), font=("Helvetica", 10))
    category_combo.pack(pady=10)
    category_combo.current(0)

    next_button = ttk.Button(task_category_frame, text="Next", command=select_task_category)
    next_button.pack(pady=20)

def show_query_page(selected_task_category):
    """
    Display the query selection page for the selected task category.

    This page allows the user to choose a specific subtask (query) and includes
    a "Create Simulated Environment" button to proceed. A "Back" button is 
    also provided to return to the task category selection page.
    """
    for widget in root.winfo_children():
        widget.destroy()

    query_frame = ttk.Frame(root)
    query_frame.pack(expand=True)

    back_button = ttk.Button(root, text="Back", command=show_task_category_page)
    back_button.place(x=10, y=10)

    ttk.Label(query_frame, text=f"Select Query for {selected_task_category}:", font=("Helvetica", 12, "bold")).pack(pady=10)
    global query_combo
    query_combo = ttk.Combobox(query_frame, values=SUBTASKS[selected_task_category], font=("Helvetica", 10))
    query_combo.pack(pady=10)
    query_combo.current(0)

    create_button = ttk.Button(query_frame, text="Create Simulated Environment", command=create_simulation_environment)
    create_button.pack(pady=20)

    global current_task_category
    current_task_category = selected_task_category


def create_simulation_environment():
    #################################################################################################################################
    # after this method being excuted, our program should call the external function in "tutorial 2()" to presnt the snapshot of
    # the simulated environment. 
    """
    Handle the creation of a simulated environment for the selected query.

    Displays a success message upon creation and transitions to the teleoperation page.
    """
    selected_query = query_combo.get()
    if not selected_query:
        messagebox.showwarning("Selection Error", "Please select a Subtask.")
        return
    messagebox.showinfo("Success", f"Simulated Environment Created for '{selected_query}'!")
    show_final_page(selected_query)

def show_final_page(selected_query):
    """
    Display the teleoperation page for the selected query.

    This page includes a button to start teleoperation and a "Back" button
    to return to the query selection page.
    """
    for widget in root.winfo_children():
        widget.destroy()

    back_button = ttk.Button(root, text="Back", command=lambda: show_query_page(current_task_category))
    back_button.place(x=10, y=10)

    final_frame = ttk.Frame(root)
    final_frame.pack(expand=True)

    begin_button = ttk.Button(
        final_frame,
        text=f"Begin Teleoperation for '{selected_query}'",
        ###################################################################################################################################
        # after this text being printed out, the program calls another function in tutorial 2...
        command=lambda: show_generate_simulation_page(selected_query)
    )
    begin_button.pack(pady=20)

def show_generate_simulation_page(selected_query):
    """
    Display the page to generate new operations or save data.

    Includes buttons to generate human operations, save data to the database,
    or create robot-simulated operations.
    """
    for widget in root.winfo_children():
        widget.destroy()

    back_button = ttk.Button(root, text="Back", command=lambda: show_final_page(selected_query))
    back_button.place(x=10, y=10)

    generate_frame = ttk.Frame(root)
    generate_frame.pack(expand=True)

    create_robot_button = ttk.Button(
        generate_frame,
        text="Create Robot-Simulated Operation",
        ###############################################################################################
        # after this text being printed out, calls the function to show the robot operating itself. 
        command=lambda: show_return_and_save_page(selected_query)
    )
    create_robot_button.pack(pady=10)

    generate_human_button = ttk.Button(
        generate_frame,
        text="Generate New Human Operation",
        ###############################################################################################
        # after this text being printed out, calls the function to start a new teleoperation
        command=lambda: messagebox.showinfo("Human Operation", "Human Operation Generated!")
    )
    generate_human_button.pack(pady=10)

    save_button = ttk.Button(
        generate_frame,
        text="Save Current Human Demonstration Data to RobotDB",
        command=save_human_demonstration_data
    )
    save_button.pack(pady=10)

def save_human_demonstration_data():
    """
    Save human demonstration data to the RobotDB database.

    Currently a stub function that displays a success message.
    """
    messagebox.showinfo("Save Data", "Human Demonstration Data successfully saved to RobotDB!")

def show_return_and_save_page(selected_query):
    """
    Display the final page with options to return to the first step
    or save data to the database.
    """
    for widget in root.winfo_children():
        widget.destroy()

    back_button = ttk.Button(root, text="Back", command=lambda: show_generate_simulation_page(selected_query))
    back_button.place(x=10, y=10)

    final_options_frame = ttk.Frame(root)
    final_options_frame.pack(expand=True)

    return_button = ttk.Button(
        final_options_frame,
        text="Return to First Step",
        command=show_task_category_page
    )
    return_button.pack(side=tk.LEFT, padx=10)

    save_button = ttk.Button(
        final_options_frame,
        text="Save Succeed Data to RobotDB",
        command=lambda: messagebox.showinfo("Save Data", "Data successfully saved to RobotDB!")
    )
    save_button.pack(side=tk.LEFT, padx=10)

def select_task_category():
    """
    Validate the task category selection and proceed to the query page.

    Displays a warning if no category is selected.
    """
    selected_task_category = category_combo.get()
    if not selected_task_category:
        messagebox.showwarning("Selection Error", "Please select a Task Category.")
        return
    show_query_page(selected_task_category)

# GUI Setup
root = tk.Tk()
root.title("Robot Demonstration Database Queries")
root.geometry("800x500")
root.configure(bg="#f0f0f0")

# Start with the Task Category selection page
show_task_category_page()

# Run the GUI
root.mainloop()
