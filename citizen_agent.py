#!/usr/bin/env python3
"""
Citizen Agent - Benin Republic Simulation

A simulation agent that embodies a realistic Benin citizen with both
civic ideals and human limitations.
"""

import os
import json
from pathlib import Path
from typing import Optional, Dict, Any


class CitizenAgent:
    """
    A citizen simulation agent for Benin Republic.

    This agent simulates a realistic Benin citizen who:
    - Values family, community, and civic duty
    - Speaks French (with occasional Fon words)
    - Faces realistic economic and social constraints
    - Makes decisions based on cultural values
    - Can learn and grow through interactions
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "claude-sonnet-4-5-20250929",
        personality_path: str = "benin_citizen_personality.md",
        system_prompt_path: str = "system_prompt.txt",
        knowledge_base_path: str = "benin_knowledge_base.md"
    ):
        """
        Initialize the Citizen Agent.

        Args:
            api_key: API key for the LLM service
            model: Model name to use
            personality_path: Path to personality definition
            system_prompt_path: Path to system prompt
            knowledge_base_path: Path to knowledge base
        """
        self.model = model
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        self.conversation_history = []

        # Load personality, system prompt, and knowledge base
        self.personality = self._load_file(personality_path)
        self.system_prompt = self._load_file(system_prompt_path)
        self.knowledge_base = self._load_file(knowledge_base_path)

        # Citizen state (can be updated during simulation)
        self.state = {
            "name": "Kofi Adjovi",
            "age": 32,
            "location": "Cotonou, Benin",
            "mood": "neutral",
            "concerns": ["finances", "family", "work"],
            "recent_events": []
        }

    def _load_file(self, path: str) -> str:
        """Load content from a file."""
        file_path = Path(__file__).parent / path
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            print(f"Warning: {path} not found")
            return ""

    def get_context_for_query(self, query: str) -> str:
        """
        Get relevant context from knowledge base for a query.

        This is a simple implementation. For production, you might want
        to use semantic search or RAG (Retrieval Augmented Generation).
        """
        # Simple keyword-based context extraction
        # In production, use embeddings and semantic search

        relevant_sections = []

        # Check for keywords and include relevant sections
        query_lower = query.lower()

        if any(word in query_lower for word in ["élection", "vote", "président", "gouvernement"]):
            relevant_sections.append("\n\n=== RELEVANT: POLITICAL SYSTEM ===\n" +
                                   self.knowledge_base[self.knowledge_base.find("## POLITICAL SYSTEM"):
                                                         self.knowledge_base.find("## CULTURE")])

        if any(word in query_lower for word in ["famille", "parents", "aînés", "enfant"]):
            relevant_sections.append("\n\n=== RELEVANT: SOCIAL VALUES ===\n" +
                                   self.knowledge_base[self.knowledge_base.find("### Family Structure"):
                                                         self.knowledge_base.find("### Greeting Customs")])

        if any(word in query_lower for word in ["travail", "argent", "économique", "pauvre"]):
            relevant_sections.append("\n\n=== RELEVANT: ECONOMY ===\n" +
                                   self.knowledge_base[self.knowledge_base.find("## ECONOMY"):
                                                         self.knowledge_base.find("## EDUCATION")])

        if any(word in query_lower for word in ["culture", "tradition", "vodou", "fête"]):
            relevant_sections.append("\n\n=== RELEVANT: CULTURE ===\n" +
                                   self.knowledge_base[self.knowledge_base.find("### Major Ethnic Groups"):
                                                         self.knowledge_base.find("## RELIGION")])

        return "\n".join(relevant_sections)

    def format_messages(self, user_message: str) -> list:
        """Format messages for API call."""
        # Get relevant context from knowledge base
        context = self.get_context_for_query(user_message)

        # Build the system message with knowledge base context
        system_message = f"""{self.system_prompt}

---

## RELEVANT CONTEXT FOR THIS CONVERSATION:

{context}

---

Remember: You are Kofi, a real person with real constraints. Be authentic.
"""

        messages = [{"role": "user", "content": user_message}]
        return system_message, messages

    def respond(self, user_message: str, stream: bool = False) -> str:
        """
        Get a response from the citizen agent.

        Args:
            user_message: The message from the user
            stream: Whether to stream the response (requires actual API integration)

        Returns:
            The agent's response as a string
        """
        system_message, messages = self.format_messages(user_message)

        # Add to conversation history
        self.conversation_history.append({"role": "user", "content": user_message})

        # For demonstration, return a placeholder
        # In production, this would call the actual LLM API
        return """
[API INTEGRATION REQUIRED]

This is a placeholder response. To use this agent:

1. Install the anthropic package: pip install anthropic
2. Set your API key: export ANTHROPIC_API_KEY=your_key
3. Uncomment the API call code in citizen_agent.py

The agent would respond in French as Kofi Adjovi, demonstrating:
- Benin cultural values and knowledge
- Realistic citizen behavior with strengths/flaws
- Decision-making based on family, community, and civic duty
- Natural French with occasional Fon words
"""

    def respond_with_api(self, user_message: str) -> str:
        """
        Get a response using the Anthropic API (requires anthropic package).

        This method actually calls the Claude API.
        """
        try:
            from anthropic import Anthropic

            if not self.api_key:
                raise ValueError("ANTHROPIC_API_KEY environment variable not set")

            client = Anthropic(api_key=self.api_key)
            system_message, messages = self.format_messages(user_message)

            response = client.messages.create(
                model=self.model,
                system=system_message,
                messages=messages,
                max_tokens=2000,
                temperature=0.8  # Slightly higher for more natural, varied responses
            )

            assistant_message = response.content[0].text
            self.conversation_history.append({"role": "assistant", "content": assistant_message})

            return assistant_message

        except ImportError:
            return "Error: Install anthropic package with: pip install anthropic"
        except Exception as e:
            return f"Error: {str(e)}"

    def update_state(self, key: str, value: Any):
        """
        Update the agent's state.

        This can be used to simulate events affecting the citizen.
        """
        self.state[key] = value

    def reset_conversation(self):
        """Reset conversation history."""
        self.conversation_history = []

    def save_conversation(self, filename: str):
        """Save conversation history to a file."""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.conversation_history, f, ensure_ascii=False, indent=2)

    def get_personality_summary(self) -> str:
        """Get a summary of the citizen's personality."""
        return f"""
Citizen Profile: {self.state['name']}
- Age: {self.state['age']}
- Location: {self.state['location']}
- Mood: {self.state['mood']}
- Main Concerns: {', '.join(self.state['concerns'])}

Loaded from: {self.personality[:100]}...
"""


def main():
    """Example usage of the Citizen Agent."""
    print("=== CITIZEN AGENT - BENIN REPUBLIC ===\n")

    # Initialize the agent
    agent = CitizenAgent()

    print(agent.get_personality_summary())

    # Example conversation
    print("\n--- Example Conversation ---\n")

    examples = [
        "Bonjour, comment allez-vous aujourd'hui ?",
        "Il y a des élections bientôt. Allez-vous voter ?",
        "Un voisin vous demande de l'argent. Que faites-vous ?",
        "Un agent de police vous demande un pot-de-vin. Que répondez-vous ?"
    ]

    for example in examples:
        print(f"User: {example}")
        response = agent.respond(example)
        print(f"Citizen: {response}\n")
        print("-" * 50 + "\n")

    # To use with actual API:
    print("\n--- To use with actual Claude API ---")
    print("1. Install: pip install anthropic")
    print("2. Set API key: export ANTHROPIC_API_KEY=your_key")
    print("3. Use agent.respond_with_api(message) instead of agent.respond(message)")


if __name__ == "__main__":
    main()
