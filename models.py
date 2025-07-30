from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Prompt:
    """
    Represents an AI prompt with its attributes.

    Attributes:
        id (Optional[int]): Unique identifier for the prompt (None for new prompts).
        text (str): The main text content of the prompt.
        tags (List[str]): A list of tags associated with the prompt.
        tool (str): The domain developer tool associated with the prompt.
        is_favorite (bool): A flag indicating if the prompt is favorited.
    """
    id: Optional[int] = None
    text: str = ""
    tags: List[str] = field(default_factory=list)
    tool: str = ""
    is_favorite: bool = False

    def to_dict(self) -> dict:
        """
        Converts the Prompt object to a dictionary.
        Tags are converted from a list to a comma-separated string for database storage.
        """
        return {
            "id": self.id,
            "text": self.text,
            "tags": ",".join(self.tags), # Store tags as comma-separated string in DB
            "tool": self.tool,
            "is_favorite": self.is_favorite
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Prompt':
        """
        Creates a Prompt object from a dictionary, typically retrieved from the database.
        Tags are converted from a comma-separated string back to a list.
        """
        # Ensure tags are handled correctly, even if empty or None from DB
        tags_list = []
        if data.get('tags'):
            tags_list = [tag.strip() for tag in str(data['tags']).split(',') if tag.strip()]

        return cls(
            id=data.get('id'),
            text=data.get('text', ''),
            tags=tags_list,
            tool=data.get('tool', ''),
            is_favorite=bool(data.get('is_favorite', False)) # Ensure boolean type
        )
