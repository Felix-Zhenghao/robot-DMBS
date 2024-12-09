import mysql.connector
from tkinter import messagebox

# Database Configuration
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "password",  
    "database": "RobotDB"    
}

def connect_to_db():

    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
        return None


def execute_query(query, params=None):

    connection = connect_to_db()
    if not connection:
        return None
    try:
        cursor = connection.cursor(dictionary=True)  # Use dictionary cursor for named columns
        cursor.execute(query, params)
        results = cursor.fetchall()
        connection.commit()
        cursor.close()
        connection.close()
        return results
    except mysql.connector.Error as err:
        messagebox.showerror("Query Error", f"Error: {err}")
        return None


def fetch_task_categories():
    """
    Example function to fetch task categories from the database.

    Returns:
        list: A list of task categories.
    """
    query = "SELECT DISTINCT taskName FROM Tasks;"
    results = execute_query(query)
    if results:
        return [row["taskName"] for row in results]
    return []

def save_demo_success_data():
    """
    Example function to save a success demonstration entry.

    Returns:
        bool: True if successful, False otherwise.
    """
    query = """
        INSERT INTO Demonstrations (createTimestamp, success, label)
        VALUES (NOW(), TRUE, 'source_demo');
    """
    if execute_query(query):
        messagebox.showinfo("Success", "Data successfully saved to RobotDB!")
        return True
    return False

# Example Usage of the Functions
if __name__ == "__main__":
    categories = fetch_task_categories()
    if categories:
        print("Fetched Task Categories:", categories)
    else:
        print("No Task Categories found or query failed.")

    save_demo_success_data()
