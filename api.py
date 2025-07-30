from services import PromptService
from models import Prompt
from typing import List, Optional

class PromptManagerAPI:
    """
    API layer for the AI Prompt Manager.
    Provides a simplified interface for the console application to interact
    with the PromptService.
    """
    def __init__(self):
        self.service = PromptService()

    def add_new_prompt(self, text: str, tags: List[str], tool: str) -> Optional[int]:
        """
        API method to add a new prompt.
        Delegates to the PromptService.
        """
        return self.service.add_prompt(text, tags, tool)

    def get_prompt_details(self, prompt_id: int) -> Optional[Prompt]:
        """
        API method to get prompt details by ID.
        Delegates to the PromptService.
        """
        return self.service.get_prompt(prompt_id)

    def update_existing_prompt(self, prompt_id: int, text: str, tags: List[str], tool: str, is_favorite: bool) -> bool:
        """
        API method to update an existing prompt.
        Delegates to the PromptService.
        """
        return self.service.update_prompt(prompt_id, text, tags, tool, is_favorite)

    def delete_existing_prompt(self, prompt_id: int) -> bool:
        """
        API method to delete a prompt.
        Delegates to the PromptService.
        """
        return self.service.delete_prompt(prompt_id)

    def get_all_prompts_api(self) -> List[Prompt]:
        """
        API method to get all prompts.
        Delegates to the PromptService.
        """
        return self.service.list_all_prompts()

    def search_and_filter_prompts_api(self, keyword: Optional[str] = None, is_favorite: Optional[bool] = None) -> List[Prompt]:
        """
        API method to search and filter prompts.
        Delegates to the PromptService.
        """
        return self.service.search_and_filter_prompts(keyword, is_favorite)

    def toggle_favorite_api(self, prompt_id: int) -> Optional[bool]:
        """
        API method to toggle favorite status.
        Delegates to the PromptService.
        """
        return self.service.toggle_favorite_status(prompt_id)
