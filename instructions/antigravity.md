---
layout: default
title: Google Antigravity
parent: Installation
---
# Google Antigravity Setup

Open Google Antigravity (AGY), and enter into the chat box:

```
I want the bioconductor skills from https://github.com/bioconductor/ai-agent-skills

You must also read and adhere to the agent behavior and safe execution standards defined in AGENTS.md.
```

This should download all skills and store them locally at ~/.agents/ai-agent-skills to be available for future conversations. You should also be able to select a subset of skills to load for a specific conversation by referencing their names or paths, and install future updates from the repository by similar request.

To test persistence, start a new conversation and ask the agent to recall the skills you shared. For example:

```
What bioconductor skills do I have?
```