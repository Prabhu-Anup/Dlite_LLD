from database import PromptDB
from models import Prompt
from typing import List, Optional

class PromptService:
    """
    Provides business logic for managing AI prompts.
    Interacts with the PromptDB for data persistence.
    """
    def __init__(self):
        self.db = PromptDB()

    def add_prompt(self, text: str, tags: List[str], tool: str) -> Optional[int]:
        """
        Adds a new prompt to the system.
        Args:
            text (str): The prompt's text.
            tags (List[str]): List of tags.
            tool (str): Associated tool.
        Returns:
            Optional[int]: The ID of the new prompt if successful, None otherwise.
        """
        prompt = Prompt(text=text, tags=tags, tool=tool)
        return self.db.insert_prompt(prompt)

    def get_prompt(self, prompt_id: int) -> Optional[Prompt]:
        """
        Retrieves a single prompt by its ID.
        Args:
            prompt_id (int): The ID of the prompt to retrieve.
        Returns:
            Optional[Prompt]: The Prompt object if found, None otherwise.
        """
        return self.db.get_prompt_by_id(prompt_id)

    def update_prompt(self, prompt_id: int, text: str, tags: List[str], tool: str, is_favorite: bool) -> bool:
        """
        Updates an existing prompt's details.
        Args:
            prompt_id (int): The ID of the prompt to update.
            text (str): New text for the prompt.
            tags (List[str]): New list of tags.
            tool (str): New associated tool.
            is_favorite (bool): New favorite status.
        Returns:
            bool: True if the update was successful, False otherwise.
        """
        prompt = self.db.get_prompt_by_id(prompt_id)
        if prompt:
            prompt.text = text
            prompt.tags = tags
            prompt.tool = tool
            prompt.is_favorite = is_favorite
            return self.db.update_prompt(prompt)
        return False

    def delete_prompt(self, prompt_id: int) -> bool:
        """
        Deletes a prompt from the system by its ID.
        Args:
            prompt_id (int): The ID of the prompt to delete.
        Returns:
            bool: True if the deletion was successful, False otherwise.
        """
        return self.db.delete_prompt(prompt_id)

    def list_all_prompts(self) -> List[Prompt]:
        """
        Retrieves all prompts currently in the system.
        Returns:
            List[Prompt]: A list of all Prompt objects.
        """
        return self.db.get_all_prompts()

    def search_and_filter_prompts(self, keyword: Optional[str] = None, is_favorite: Optional[bool] = None) -> List[Prompt]:
        """
        Searches and filters prompts based on a keyword and/or favorite status.
        Args:
            keyword (Optional[str]): A keyword to search for in text, tags, or tool fields.
            is_favorite (Optional[bool]): True to filter for favorites, False for non-favorites, None for all.
        Returns:
            List[Prompt]: A list of prompts matching the criteria.
        """
        prompts = []
        if keyword:
            prompts = self.db.search_prompts(keyword)
        else:
            prompts = self.db.get_all_prompts()

        # Apply in-memory filtering for is_favorite if specified
        if is_favorite is not None:
            prompts = [p for p in prompts if p.is_favorite == is_favorite]

        return prompts

    def toggle_favorite_status(self, prompt_id: int) -> Optional[bool]:
        """
        Toggles the favorite status of a specific prompt.
        Args:
            prompt_id (int): The ID of the prompt to toggle.
        Returns:
            Optional[bool]: The new favorite status (True/False) if successful, None if prompt not found.
        """
        prompt = self.db.get_prompt_by_id(prompt_id)
        if prompt:
            prompt.is_favorite = not prompt.is_favorite # Toggle the status
            if self.db.update_prompt(prompt):
                return prompt.is_favorite
        return None
