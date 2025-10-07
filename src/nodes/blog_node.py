from src.states.blog_state import BlogStateDict
from langchain_core.messages import SystemMessage, HumanMessage
from src.states.blog_state import Blog
class BlogNode:
    def __init__(self, llm):
        self.llm = llm

    def title_creation(self, state: BlogStateDict) -> dict:
        topic = state.get("topic", "")
        if not topic:
            return {"blog": {"title": "Untitled Blog"}}

        system_message = f"""
            You are a blog content writer. Use Markdown formatting.
            Generate a catchy and engaging blog title based on the topic: "{topic}".
            The title should be creative and SEO-friendly.
        """
        response = self.llm.invoke(system_message)
        return {"blog": {"title": response.content}}

    def content_generation(self, state: BlogStateDict) -> dict:
        blog = state.get("blog", {})
        title = blog.get("title", "")
        if not title:
            return {"blog": {"title": "Untitled Blog", "content": "No content generated."}}

        system_message = f"""
            You are a blog content writer. Use Markdown formatting.
            Generate a detailed and engaging blog post based on the title: "{title}".
            The content should be well-structured, informative, and captivating for readers.
        """
        response = self.llm.invoke(system_message)
        return {"blog": {"title": title, "content": response.content}}

    def translation(self, state: BlogStateDict):
        translation_prompt="""
        Translate the following blog content into {current_language}.
        - Ensure the translation maintains the original meaning and tone.
        - Adapt to cultural references and idoms to be appropriate for {current_language}.
        
        ORIGINAL BLOG CONTENT:
        {blog_content}
        """
        blog_content = state["blog"]["content"]
        messages = [
            HumanMessage(content=translation_prompt.format(
                current_language=state["current_language"],
                blog_content=blog_content
            ))
        ]
        translated_content = self.llm.with_structured_output(Blog).invoke(messages)
        
    def route(self, state: BlogStateDict):
        return {"current_language": state['current_language']}
    
    def route_decision(self, state: BlogStateDict):
        if state.get("current_language") == "hindi":
            return "hindi"
        elif state.get("current_language") == "french":
            return "french"
        else:
            return state['current_language']