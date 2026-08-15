---
name: bioc-protocol-runner
description: Search, retrieve, evaluate trust, and execute citable workflows from federated protocol repositories
version: 1.0.0
category: protocols
author: bioconductor
tags: [workflow, protocol, pipeline, citation, provenance]
---

# bioc-protocol-runner

Finds and executes citable, versioned analysis protocols from federated community repositories, ensuring reproducible agent behavior and correct attribution of methods and underlying literature.

## Usage

- "Run the 16S quality control protocol"
- "Search for a metagenomics taxonomy protocol and run it"
- "Can you follow the waldronlab/ai-agent-protocols version of the 16S pipeline?"

## Prerequisites

- Read access to the internet to fetch `registry.yaml` and `PROTOCOLS.yaml` indices from GitHub.

## Process

### 1. Discover Available Protocols

1. Read `registry.yaml` from the `waldronlab/ai-agent-protocols` repository (or whatever repository the user specified, defaulting to `https://raw.githubusercontent.com/waldronlab/ai-agent-protocols/main/registry.yaml`).
2. For each registered entry in that file, fetch its `PROTOCOLS.yaml` index using its `index_url`.
3. Merge all protocol entries from all fetched indices into a single available protocol list.

### 2. Match Protocol to Request

1. Match the user's stated task to the available protocols using `name`, `description`, `category`, and `tags`.
2. If there are multiple matches, rank them by `trust_tier` (descending), and then by `status` (preferring `stable`).

### 3. Present Selection to User

1. Show the top 1-3 matches to the user.
2. For each match, provide the `name`, repository name, `version`, `status`, `trust_tier`, and `description`.
3. Ask the user to confirm which protocol to run.
   - *Warning*: If the chosen protocol has status `draft`, warn the user that it may be unstable.
   - *Error*: If the chosen protocol has status `deprecated`, refuse to run it unless explicitly overridden.

### 4. Resolve Dependencies

1. Once the user selects a protocol, check its `protocols_used` field.
2. Verify that each dependency exists in the merged federation index.
3. Order execution: Dependencies must be executed *before* the main protocol, in the order they are declared.
4. *Constraint*: Currently, only single-level dependencies are supported. If a dependency itself has dependencies, inform the user and abort.

### 5. Fetch Content and Compile Citations

1. For each protocol in the execution chain (dependencies first, then the main protocol):
   - Fetch the markdown content using the `protocol_url` specified in the index.
   - Parse the `## References` section and the `citations` YAML frontmatter field to extract DOIs and PMIDs (Level 2 Citations).
2. **Important**: Before executing any code, emit the full Method Provenance block to the user using the following format, adapted for each protocol in the chain:

   ```markdown
   ## Method Provenance

   ### Protocol Citation (Level 1)
   Following: [Author] "Name of Protocol"
   Repository: [Repository Name], protocol: [Protocol Name] v[Version]
   Repository DOI: [repository_doi if present]
   Protocol DOI: [protocol_doi if present]
   Trust tier: [trust_tier]
   License: [license]

   ### Primary Literature to Cite (Level 2)
   This protocol implements methods from:
   - [List of DOIs and PMIDs from the `citations` field and `## References` section]
   ```

   *Note: If `protocol_doi` is present, cite it. If only `repository_doi` is present, ensure it is clearly displayed alongside the specific protocol name and version so the user knows which part of the repository was used.*

### 6. Execute Protocol

1. Follow the steps in the fetched protocol content in order.
2. Adapt the provided code to the user's specific environment, file paths, parameters, and organisms as necessary.
3. If a step cannot be followed exactly as written, or requires a different package version than specified, note this departure inline.

### 7. Record Departures

1. After execution completes, emit a final "Departures from protocol" section.
2. List any deviations made during execution (e.g., using a different parameter value, skipping a step, or substituting a package). This is a normal part of adapting a protocol; recording it is what matters for provenance.

## Output Format

1. The "Method Provenance" block (Level 1 and Level 2 citations).
2. Code and execution logs from running the steps.
3. The "Departures from protocol" summary.
4. The standard Bioconductor skill execution citation (from `AGENTS.md`).

## Examples

**User**: "Search for a metagenomics taxonomy protocol and run it"

**Skill produces**:
- A short list of matching protocols with version, status, trust tier, and description
- A request for the user to confirm which protocol to run
- A method provenance block before any execution begins
- A departures summary after the protocol finishes

## Notes

- Trust scores and popularity metrics are reserved for a future release, but `trust_tier` from the registry should be displayed if available.
