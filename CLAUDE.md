# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Citizen Agent simulates **Kofi Adjovi**, a realistic 32-year-old Benin Republic citizen, using the Anthropic Claude API. The agent responds in French with authentic cultural values, civic behaviors, and human limitations.

## Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run the demo (no API key needed - shows placeholder responses)
python citizen_agent.py

# Run with actual API (requires ANTHROPIC_API_KEY env var)
export ANTHROPIC_API_KEY=your_key
python -c "from citizen_agent import CitizenAgent; a = CitizenAgent(); print(a.respond_with_api('Bonjour'))"
```

## Architecture

Single-file Python agent (`citizen_agent.py`) with three markdown data files loaded at init:

- **`system_prompt.txt`** — Character definition: identity, values, personality, decision framework, response guidelines. This is the core behavioral instruction sent as the system message.
- **`benin_citizen_personality.md`** — Extended personality traits and behavioral details (loaded but not yet integrated into API calls).
- **`benin_knowledge_base.md`** — Factual reference about Benin (history, politics, culture, economy). Sections are retrieved via keyword matching in `get_context_for_query()`.

### Key design points

- **Two response methods**: `respond()` returns a placeholder (no API needed); `respond_with_api()` calls the Anthropic API.
- **Keyword-based RAG**: `get_context_for_query()` does simple string matching to extract relevant knowledge base sections. Uses `str.find()` with section headers — fragile if headers change.
- **Stateful agent**: `self.state` dict tracks mood, concerns, and recent events. `update_state()` modifies it, but state is not yet injected into API calls.
- **Conversation history**: Accumulated in `self.conversation_history` but not sent in subsequent API calls (each call is single-turn).
- **personality field**: Loaded from file but only used in `get_personality_summary()`, not passed to the API.

### Known gaps

- Conversation history is stored but not used for multi-turn context.
- Agent state (mood, concerns) doesn't influence responses.
- Personality file content isn't included in API calls.
- Knowledge retrieval breaks if section headers in `benin_knowledge_base.md` are renamed.
