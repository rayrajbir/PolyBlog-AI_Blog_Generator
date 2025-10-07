from typing import TypedDict
from pydantic import BaseModel, Field

# Blog model to hold topic and content
class Blog(BaseModel):
    topic: str = Field(description="The topic of the blog post")
    content: str = Field(description="The content of the blog post")
    
# TypedDict for internal state representation
class BlogStateDict(TypedDict):
    topic: str
    blog: Blog
    current_language: str

# States class to use with StateGraph
class BlogState:
    TITLE_CREATION = "title_creation"
    CONTENT_GENERATION = "content_generation"
