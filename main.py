from api import PromptManagerAPI
from config import Messages
import os
import sys

class ConsoleApp:
    """
    The main console-driven application for the AI Prompt Manager.
    Provides a user interface to interact with the PromptManagerAPI.
    """
    def __init__(self):
        self.api = PromptManagerAPI()

    def clear_screen(self):
        """
        Clears the console screen for better readability.
        Works on both Windows ('cls') and Unix-like systems ('clear').
        """
        os.system('cls' if os.name == 'nt' else 'clear')

    def display_prompt(self, prompt):
        """
        Helper method to display the details of a single prompt in a formatted way.
        """
        fav_status = "Yes" if prompt.is_favorite else "No"
        print(f"ID: {prompt.id}")
        print(f"Text: {prompt.text}")
        print(f"Tags: {', '.join(prompt.tags)}")
        print(f"Tool: {prompt.tool}")
        print(f"Favorite: {fav_status}")
        print("-" * 30) # Separator for readability

    def add_prompt(self):
        """
        Handles the 'Add New Prompt' functionality.
        Prompts the user for prompt details and calls the API to save it.
        """
        self.clear_screen()
        print("\n--- Add New Prompt ---")
        text = input("Enter prompt text: ")
        tags_input = input("Enter tags (comma-separated, e.g., 'marketing, social media'): ")
        # Split tags input by comma and strip whitespace, filter out empty strings
        tags = [tag.strip() for tag in tags_input.split(',') if tag.strip()]
        tool = input("Enter associated tool (e.g., 'Gemini API', 'DALL-E'): ")

        prompt_id = self.api.add_new_prompt(text, tags, tool)
        if prompt_id:
            print(Messages.PROMPT_ADDED.format(prompt_id))
        else:
            print("Failed to add prompt.")
        input("\nPress Enter to continue...")

    def view_all_prompts(self):
        """
        Handles the 'View All Prompts' functionality.
        Retrieves all prompts and displays them.
        """
        self.clear_screen()
        print("\n--- All Prompts ---")
        prompts = self.api.get_all_prompts_api()
        if not prompts:
            print(Messages.NO_PROMPTS)
        else:
            for prompt in prompts:
                self.display_prompt(prompt)
        input("\nPress Enter to continue...")

    def search_prompts(self):
        """
        Handles the 'Search Prompts' functionality.
        Allows searching by keyword and optional filtering by favorite status.
        """
        self.clear_screen()
        print("\n--- Search Prompts ---")
        keyword = input(Messages.SEARCH_PROMPT)
        
        # Option to filter by favorite status
        filter_fav_input = input("Filter by favorite status? (yes/no/all): ").lower().strip()
        is_favorite_filter = None
        if filter_fav_input == 'yes':
            is_favorite_filter = True
        elif filter_fav_input == 'no':
            is_favorite_filter = False

        prompts = self.api.search_and_filter_prompts_api(keyword=keyword, is_favorite=is_favorite_filter)

        if not prompts:
            print("No prompts found matching your criteria.")
        else:
            print("\n--- Search Results ---")
            for prompt in prompts:
                self.display_prompt(prompt)
        input("\nPress Enter to continue...")

    def edit_prompt(self):
        """
        Handles the 'Edit Prompt' functionality.
        Allows the user to modify an existing prompt's details.
        """
        self.clear_screen()
        print("\n--- Edit Prompt ---")
        try:
            prompt_id = int(input("Enter ID of prompt to edit: "))
        except ValueError:
            print("Invalid ID. Please enter a number.")
            input("\nPress Enter to continue...")
            return

        prompt = self.api.get_prompt_details(prompt_id)
        if not prompt:
            print(Messages.PROMPT_NOT_FOUND.format(prompt_id))
            input("\nPress Enter to continue...")
            return

        print("\n--- Current Prompt Details ---")
        self.display_prompt(prompt)

        print("\nEnter new values (leave blank to keep current value):")
        new_text = input(f"New text (current: '{prompt.text}'): ")
        new_tags_input = input(f"New tags (current: '{', '.join(prompt.tags)}'): ")
        new_tool = input(f"New tool (current: '{prompt.tool}'): ")
        new_favorite_input = input(f"New favorite status (current: {'yes' if prompt.is_favorite else 'no'}) (yes/no): ").lower().strip()

        # Use new input if provided, otherwise keep current value
        text = new_text if new_text else prompt.text
        tags = ([tag.strip() for tag in new_tags_input.split(',') if tag.strip()]
                if new_tags_input else prompt.tags)
        tool = new_tool if new_tool else prompt.tool
        
        # Determine new favorite status
        is_favorite = prompt.is_favorite # Default to current
        if new_favorite_input == 'yes':
            is_favorite = True
        elif new_favorite_input == 'no':
            is_favorite = False

        if self.api.update_existing_prompt(prompt_id, text, tags, tool, is_favorite):
            print(Messages.PROMPT_UPDATED.format(prompt_id))
        else:
            print("Failed to update prompt.")
        input("\nPress Enter to continue...")

    def toggle_favorite_status(self):
        """
        Handles toggling the favorite status of a prompt.
        """
        self.clear_screen()
        print("\n--- Toggle Favorite Status ---")
        try:
            prompt_id = int(input("Enter ID of prompt to toggle favorite status: "))
        except ValueError:
            print("Invalid ID. Please enter a number.")
            input("\nPress Enter to continue...")
            return

        new_status = self.api.toggle_favorite_api(prompt_id)
        if new_status is not None:
            status_text = "favorited" if new_status else "unfavorited"
            print(Messages.FAVORITE_TOGGLED.format(prompt_id, status_text))
        else:
            print(Messages.PROMPT_NOT_FOUND.format(prompt_id))
        input("\nPress Enter to continue...")

    def delete_prompt(self):
        """
        Handles deleting a prompt.
        """
        self.clear_screen()
        print("\n--- Delete Prompt ---")
        try:
            prompt_id = int(input("Enter ID of prompt to delete: "))
        except ValueError:
            print("Invalid ID. Please enter a number.")
            input("\nPress Enter to continue...")
            return

        if self.api.delete_existing_prompt(prompt_id):
            print(Messages.PROMPT_DELETED.format(prompt_id))
        else:
            print(Messages.PROMPT_NOT_FOUND.format(prompt_id))
        input("\nPress Enter to continue...")

    def run(self):
        """
        The main loop of the console application.
        Displays the menu and handles user choices.
        """
        self.clear_screen()
        print(Messages.WELCOME)
        while True:
            self.clear_screen()
            print(Messages.MENU)
            choice = input().strip()

            if choice == '1':
                self.add_prompt()
            elif choice == '2':
                self.view_all_prompts()
            elif choice == '3':
                self.search_prompts()
            elif choice == '4':
                self.edit_prompt()
            elif choice == '5':
                self.toggle_favorite_status()
            elif choice == '6':
                self.delete_prompt()
            elif choice == '7':
                print(Messages.EXIT)
                # Ensure database connection is closed gracefully
                if self.api.service.db.connection:
                    self.api.service.db.close()
                sys.exit(0) # Exit the application
            else:
                print(Messages.INVALID_CHOICE)
                input("\nPress Enter to continue...")

if __name__ == "__main__":
    app = ConsoleApp()
    app.run()
