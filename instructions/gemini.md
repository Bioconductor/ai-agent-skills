# Google Gemini Setup

Open Gemini Code Assist, and enter into the chat box:

```
I want the waldronlab skills from https://github.com/waldronlab/ai-agent-skills

You must also read and adhere to the agent behavior and safe execution standards defined in AGENTS.md.
```

This should download all skills and store them locally at ~/.gemini/ai-agent-skills to be available for future conversations. You should also be able to select a subset of skills to load for a specific conversation by referencing their names or paths, and install future updates from the repository by similar request.

To test persistence, start a new conversation and ask Gemini to recall the skills you shared. For example:

```
What waldronlab skills do I have?
```

**Note**: Google AI Pro for students (https://gemini.google/students/) provides additional quota and access to more recent models. 