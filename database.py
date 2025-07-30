import mysql.connector
from mysql.connector import Error
from config import Config
from models import Prompt
from typing import List, Optional, Dict, Any

class PromptDB:
    """
    Manages database operations for the Prompt Manager application.
    Acts as the Data Access Object (DAO) layer.
    """
    def __init__(self):
        self.connection = None
        self.connect()
        self.create_table() # Ensure the prompts table exists on initialization

    def connect(self):
        """
        Establishes a connection to the MySQL database using credentials from Config.
        Handles connection errors.
        """
        try:
            self.connection = mysql.connector.connect(
                host=Config.DB_HOST,
                user=Config.DB_USER,
                password=Config.DB_PASSWORD,
                database=Config.DB_NAME
            )
            if self.connection.is_connected():
                print("Successfully connected to MySQL database.")
        except Error as e:
            print(f"Error connecting to MySQL database: {e}")
            self.connection = None # Set connection to None if connection fails

    def close(self):
        """
        Closes the database connection if it's open.
        """
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("MySQL connection closed.")

    def create_table(self):
        """
        Creates the 'prompts' table in the database if it does not already exist.
        This ensures the schema is ready when the application starts.
        """
        if not self.connection:
            print("Cannot create table: No database connection.")
            return

        cursor = self.connection.cursor()
        try:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS prompts (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    text TEXT NOT NULL,
                    tags VARCHAR(255) DEFAULT '',
                    tool VARCHAR(255) DEFAULT '',
                    is_favorite BOOLEAN DEFAULT FALSE
                )
            """)
            self.connection.commit()
            print("Table 'prompts' checked/created successfully.")
        except Error as e:
            print(f"Error creating table: {e}")
        finally:
            cursor.close()

    def insert_prompt(self, prompt: Prompt) -> Optional[int]:
        """
        Inserts a new prompt record into the 'prompts' table.
        Returns the ID of the newly inserted prompt or None on failure.
        """
        if not self.connection:
            print("Cannot insert prompt: No database connection.")
            return None

        sql = "INSERT INTO prompts (text, tags, tool, is_favorite) VALUES (%s, %s, %s, %s)"
        # Convert tags list to a comma-separated string for storage
        values = (prompt.text, ",".join(prompt.tags), prompt.tool, prompt.is_favorite)
        cursor = self.connection.cursor()
        try:
            cursor.execute(sql, values)
            self.connection.commit()
            return cursor.lastrowid # Returns the ID of the last inserted row
        except Error as e:
            print(f"Error inserting prompt: {e}")
            self.connection.rollback() # Rollback changes on error
            return None
        finally:
            cursor.close()

    def get_prompt_by_id(self, prompt_id: int) -> Optional[Prompt]:
        """
        Retrieves a single prompt record by its ID.
        Returns a Prompt object or None if not found.
        """
        if not self.connection:
            print("Cannot retrieve prompt: No database connection.")
            return None

        sql = "SELECT id, text, tags, tool, is_favorite FROM prompts WHERE id = %s"
        # Use dictionary=True to fetch rows as dictionaries, making it easier to convert to Prompt object
        cursor = self.connection.cursor(dictionary=True)
        try:
            cursor.execute(sql, (prompt_id,))
            record = cursor.fetchone()
            if record:
                return Prompt.from_dict(record)
            return None
        except Error as e:
            print(f"Error retrieving prompt: {e}")
            return None
        finally:
            cursor.close()

    def update_prompt(self, prompt: Prompt) -> bool:
        """
        Updates an existing prompt record in the 'prompts' table.
        Returns True if the update was successful, False otherwise.
        Requires the prompt object to have a valid ID.
        """
        if not self.connection:
            print("Cannot update prompt: No database connection.")
            return False
        if prompt.id is None:
            print("Cannot update prompt: Prompt ID is missing.")
            return False

        sql = "UPDATE prompts SET text = %s, tags = %s, tool = %s, is_favorite = %s WHERE id = %s"
        values = (prompt.text, ",".join(prompt.tags), prompt.tool, prompt.is_favorite, prompt.id)
        cursor = self.connection.cursor()
        try:
            cursor.execute(sql, values)
            self.connection.commit()
            return cursor.rowcount > 0 # Returns True if at least one row was affected
        except Error as e:
            print(f"Error updating prompt: {e}")
            self.connection.rollback()
            return False
        finally:
            cursor.close()

    def delete_prompt(self, prompt_id: int) -> bool:
        """
        Deletes a prompt record from the 'prompts' table by its ID.
        Returns True if the deletion was successful, False otherwise.
        """
        if not self.connection:
            print("Cannot delete prompt: No database connection.")
            return False

        sql = "DELETE FROM prompts WHERE id = %s"
        cursor = self.connection.cursor()
        try:
            cursor.execute(sql, (prompt_id,))
            self.connection.commit()
            return cursor.rowcount > 0 # Returns True if a row was deleted
        except Error as e:
            print(f"Error deleting prompt: {e}")
            self.connection.rollback()
            return False
        finally:
            cursor.close()

    def get_all_prompts(self) -> List[Prompt]:
        """
        Retrieves all prompt records from the 'prompts' table.
        Returns a list of Prompt objects.
        """
        if not self.connection:
            print("Cannot retrieve all prompts: No database connection.")
            return []

        sql = "SELECT id, text, tags, tool, is_favorite FROM prompts"
        cursor = self.connection.cursor(dictionary=True)
        try:
            cursor.execute(sql)
            records = cursor.fetchall()
            return [Prompt.from_dict(record) for record in records]
        except Error as e:
            print(f"Error retrieving all prompts: {e}")
            return []
        finally:
            cursor.close()

    def search_prompts(self, keyword: str) -> List[Prompt]:
        """
        Searches for prompts where the keyword appears in the 'text', 'tags', or 'tool' fields.
        Uses SQL LIKE for partial matching.
        Returns a list of matching Prompt objects.
        """
        if not self.connection:
            print("Cannot search prompts: No database connection.")
            return []

        sql = """
            SELECT id, text, tags, tool, is_favorite
            FROM prompts
            WHERE text LIKE %s OR tags LIKE %s OR tool LIKE %s
        """
        search_term = f"%{keyword}%" # Add wildcards for partial matching
        cursor = self.connection.cursor(dictionary=True)
        try:
            cursor.execute(sql, (search_term, search_term, search_term))
            records = cursor.fetchall()
            return [Prompt.from_dict(record) for record in records]
        except Error as e:
            print(f"Error searching prompts: {e}")
            return []
        finally:
            cursor.close()
