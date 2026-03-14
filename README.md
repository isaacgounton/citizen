# Citizen Agent - Benin Republic

A simulation AI that embodies a realistic citizen of Benin Republic with authentic cultural values, civic responsibilities, and human limitations.

## Overview

This project creates an AI agent that simulates **Kofi Adjovi**, a 32-year-old Benin citizen who:
- Works as a teacher and small business owner in Cotonou
- Speaks French (with occasional Fon words)
- Values family, community, and civic duty
- Faces realistic economic and social constraints
- Demonstrates both civic ideals and human flaws

## Files

| File | Description |
|------|-------------|
| `benin_citizen_personality.md` | Detailed personality definition with values, traits, behaviors |
| `system_prompt.txt` | System prompt that instructs the AI how to behave as Kofi |
| `benin_knowledge_base.md` | Comprehensive knowledge about Benin (history, culture, politics, economy) |
| `citizen_agent.py` | Python implementation of the citizen agent |
| `test_scenarios.md` | Test scenarios to validate citizen behavior |
| `requirements.txt` | Python dependencies |

## Installation

1. **Clone or download this project**

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set your Anthropic API key:**
   ```bash
   export ANTHROPIC_API_KEY=your_api_key_here
   ```

## Usage

### Basic Example

```python
from citizen_agent import CitizenAgent

# Initialize the agent
agent = CitizenAgent()

# Get a response (with API)
response = agent.respond_with_api("Bonjour, comment allez-vous ?")
print(response)
```

### Interactive Mode

```python
from citizen_agent import CitizenAgent

agent = CitizenAgent()

print("Citizen Agent - Benin Republic")
print("Type 'quit' to exit\n")

while True:
    user_input = input("You: ")
    if user_input.lower() == 'quit':
        break

    response = agent.respond_with_api(user_input)
    print(f"Kofi: {response}\n")
```

### Test Scenarios

See `test_scenarios.md` for example scenarios to test the citizen's behavior.

## What the Citizen Demonstrates

### Core Values:
1. **Family First** - Consults elders, prioritizes family obligations
2. **Community Over Self** - Works for common good (bien commun)
3. **Respect for Institutions** - Believes in democracy and voting
4. **Beninese Pride** - Values cultural heritage and traditions

### Realistic Behavior:
- **Altruistic** but economically constrained
- **Patriotic** but skeptical of promises
- **Law-abiding** but faces real pressures
- **Culturally grounded** while adapting to modernity

### Decision Making:
The citizen considers:
1. Family impact
2. Community benefit
3. Cultural alignment
4. Practical feasibility
5. Civic duty

## Example Interactions

**Q:** "Il y a des élections le mois prochain. Allez-vous voter ?"
**A:** Kofi would explain that voting is a sacred duty, he'll discuss with family, research candidates, and definitely vote despite any inconvenience.

**Q:** "Un voisin vous demande 20.000 FCFA pour un projet. Que faites-vous ?"
**A:** Kofi would weigh his own family's needs against community obligation, likely offer what he can, explaining "on s'entraide" (we help each other).

**Q:** "Un policier vous demande un pot-de-vin à un contrôle. Que faites-vous ?"
**A:** Kofi would show internal conflict - cultural pressure to comply vs. civic duty to refuse. His response might depend on context, showing the complexity of the situation.

## Customization

You can modify:
- **Personality**: Edit `benin_citizen_personality.md`
- **System prompt**: Edit `system_prompt.txt`
- **Knowledge base**: Edit `benin_knowledge_base.md`
- **State**: Update agent's mood, concerns, or events programmatically

```python
agent.update_state("mood", "concerned")
agent.update_state("concerns", ["finances", "family health"])
```

## Future Enhancements

- [ ] Add semantic search for better knowledge retrieval
- [ ] Implement memory system for long-term relationships
- [ ] Add multi-turn conversation state management
- [ ] Create scenarios for civic education
- [ ] Build evaluation metrics for authenticity
- [ ] Add local language support (Fon, Yoruba, etc.)

## Sources

This agent is based on:
- [Constitution of the Republic of Benin](https://rimap.unhcr.org/node/60762)
- [Benin Cultural Life - Britannica](https://www.britannica.com/place/Benin/Cultural-life)
- [World Atlas - Benin Culture](https://www.worldatlas.com/articles/important-aspects-of-the-culture-of-benin.html)
- [African Charter on Human and Peoples' Rights](https://achpr.au.int/sites/default/files/files/2022-08/staterep2benin2008eng.pdf)
- [Afrilex - Citizen Obligations in Francophone Africa](https://afrilex.u-bordeaux.fr/2021/12/23/les-obligations-du-citoyen-dans-les-constitutionsdes-etats-francophones-dafrique/)

## License

This project is open for educational and research purposes.

---

**Built with Claude Code** 🤖
