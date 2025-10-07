from langgraph.graph import StateGraph, START, END
from src.llms.groqllm import GroqLLM
from src.states.blog_state import BlogStateDict
from src.nodes.blog_node import BlogNode

class GraphBuilder:
    def __init__(self, llm):
        self.llm = llm
        # ✅ Use BlogStateDict (dict-like, mergeable by LangGraph)
        self.graph = StateGraph(BlogStateDict)
        self.blog_node = BlogNode(llm)

    def build_topic_graph(self):
        """Graph for generating a blog title and content from a topic."""
        self.graph.add_node("title_creation", self.blog_node.title_creation)
        self.graph.add_node("content_generation", self.blog_node.content_generation)

        # Define flow
        self.graph.add_edge(START, "title_creation")
        self.graph.add_edge("title_creation", "content_generation")
        self.graph.add_edge("content_generation", END)

        return self.graph

    def build_language_graph(self):
        """Graph for multilingual blog generation and translation."""
        self.blog_node_obj = BlogNode(self.llm)
        print("LLM initialized:", self.llm)

        # Define nodes
        self.graph.add_node("title_creation", self.blog_node.title_creation)
        self.graph.add_node("content_generation", self.blog_node.content_generation)
        self.graph.add_node(
            "hindi_translation",
            lambda state: self.blog_node_obj.translation({**state, "current_language": "hindi"})
        )
        self.graph.add_node(
            "french_translation",
            lambda state: self.blog_node_obj.translation({**state, "current_language": "french"})
        )

        # Define flow
        self.graph.add_edge(START, "title_creation")
        self.graph.add_edge("title_creation", "content_generation")

        # Conditional routing after content generation
        self.graph.add_conditional_edges(
            "content_generation",
            self.blog_node_obj.route_decision,
            {
                "hindi": "hindi_translation",
                "french": "french_translation",
            }
        )

        # End points
        self.graph.add_edge("hindi_translation", END)
        self.graph.add_edge("french_translation", END)

        return self.graph

    def setup_graph(self, usecase: str):
        """Compile the graph for a specific usecase."""
        if usecase == "topic":
            self.build_topic_graph()
        elif usecase == "language":
            self.build_language_graph()
        else:
            raise ValueError(f"Unknown usecase: {usecase}")
        return self.graph.compile()
