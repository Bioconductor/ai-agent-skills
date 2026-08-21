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

- Network access to fetch `registry.yaml` and `PROTOCOLS.yaml` indices over HTTPS from the protocol registry and protocol repositories (e.g., from a git hosting service such as GitHub).

## Process

### 1. Discover Available Protocols

1. Read `registry.yaml` from the `waldronlab/ai-agent-protocols` repository (or whatever repository the user specified, defaulting to `https://raw.githubusercontent.com/waldronlab/ai-agent-protocols/main/registry.yaml`).
2. For each registered entry in that file, fetch its `PROTOCOLS.yaml` index using its `index_url`. Note that registered repositories serve `PROTOCOLS.yaml` entries with the fields this skill relies on (e.g., `name`, `description`, `version`, `status`, `trust_tier`, `type` (`atomic` | `composite`), `citation`, `publication_doi`, `protocol_doi`, `repository_doi`, `license`, `protocol_url`, `upstream_repositories`, `database_urls`, `protocols_used`).
3. Merge all protocol entries from all fetched indices into a single available protocol list.

### 2. Match Protocol to Request

1. Match the user's stated task to the available protocols using `name`, `description`, `category`, and `tags`.
2. If there are multiple matches, rank them by `trust_tier` (descending), and then by `status` (preferring `stable`).

### 3. Present Selection to User

1. Show the top 1-3 matches to the user.
2. For each match, provide the `name`, repository name, `version`, `status`, `trust_tier`, and `description`.
3. Ask the user to confirm which protocol to run.
   - *Warning*: If the chosen protocol has status `draft`, warn the user that it may be unstable.
   - *Warning*: If the chosen protocol has status `superseded`, warn the user and suggest checking for a newer version or successor protocol.
   - *Error*: If the chosen protocol has status `deprecated`, refuse to run it unless explicitly overridden.

### 4. Resolve Dependencies

1. Once the user selects a protocol, check its `protocols_used` field. The entries follow this object structure:
   ```yaml
   protocols_used:
     - name: humann4-sgb-aggregation
       repository: waldronlab/ai-agent-protocols
       version: 1.0.0
   ```
2. Verify that each dependency exists in the merged federation index.
3. Order execution: Dependencies must be executed *before* the main protocol, in the order they are declared.
4. *Constraint*: Composite protocols define single-level execution dependencies across constituent atomic protocols. If a dependency itself has dependencies, inform the user and abort.

### 5. Fetch Content and Compile Citations

1. For each protocol in the execution chain (dependencies first, then the main protocol):
   - Fetch the markdown content using the `protocol_url` specified in the index.
   - Parse the singular `citation` YAML frontmatter field to extract the DOI or PMID (Level 2 Citation).
   - When executing a composite protocol (`type: composite`), aggregate the singular `citation` DOI/PMID from each constituent atomic protocol listed in `protocols_used`.
2. **Important**: Before executing any code, emit the full Method Provenance block to the user using the following format, adapted for each protocol in the chain:

   ```markdown
   ## Method Provenance

   ### Protocol Citation (Level 1)
   Following: [Author] "[Protocol Title/Name]"
   Repository: [Repository Name], protocol: [Protocol Name] v[Version]
   Repository DOI: [repository_doi if present]
   Protocol DOI: [protocol_doi if present]
   Publication DOI: [publication_doi if present]
   Trust tier: [trust_tier]
   License: [license]

   ### Primary Literature to Cite (Level 2)
   This protocol implements methods from:
   - [Primary method citation (DOI/PMID) from `citation` field]
   - [For composite protocols: aggregated DOIs/PMIDs from all constituent atomic protocols]
   ```

   *Note: If `protocol_doi` is present, cite it. If only `repository_doi` is present, ensure it is clearly displayed alongside the specific protocol name and version so the user knows which part of the repository was used.*

### 6. Execute Protocol

1. Follow the steps in the fetched protocol content in order.
2. **Resource Discovery**: Agents can discover and download pre-computed reference data and upstream tools using the `database_urls` and `upstream_repositories` YAML fields provided in the index.
3. Adapt the provided code to the user's specific environment, file paths, parameters, and organisms as necessary.
4. If a step cannot be followed exactly as written, or requires a different package version than specified, note this departure inline.

### 7. Record Departures

1. After execution completes, emit a final "Departures from protocol" section.
2. List any deviations made during execution (e.g., using a different parameter value, skipping a step, or substituting a package). This is a normal part of adapting a protocol; recording it is what matters for provenance.

### 8. Generate Draft Methods Section

1. **Narrative Synthesis:** Synthesize a publication-ready narrative Methods section describing the exact analysis steps performed.
   - If the protocol contains a `## Methods Template` section, use its text as the baseline phrasing structure and fill in actual runtime parameters and sample identifiers. Otherwise, construct clear academic prose.
2. **Inline Method & Tool Attribution (Level 2):** Embed underlying methodology and software citations directly into the narrative prose at the relevant steps using their DOIs/PMIDs (e.g., *"...using MetaPhlAn 4.2 (DOI: 10.1038/s41587-023-01688-w)"*).
3. **Departures & Parameters:** Seamlessly incorporate any runtime parameter adaptations or deviations recorded in Step 7 into the text.
4. **AI Agent Protocols Attribution Subsection (Level 1):** Include a dedicated separate paragraph/subsection naming and citing the executed protocol artifact, repository, version, and protocol/repository DOI:
   > *"Computational analysis was automated using the AI Agent Protocol `[Protocol Name]` (v`[Version]`, DOI: `[protocol_doi or repository_doi]`) executed via Bioconductor's `bioc-protocol-runner`."*
5. **No Style-Specific Bibliography Formatting:** Do not generate formatted bibliographies in arbitrary styles (APA, MLA, BibTeX, etc.); propagate exact DOIs and PMIDs so users can seamlessly import them into their reference manager of choice.

## Output Format

1. The "Method Provenance" block (Level 1 and Level 2 citations emitted pre-execution).
2. Code and execution logs from running the steps.
3. The "Departures from protocol" summary.
4. The **"Draft Methods Section"** (publication-ready prose with inline DOI citations, runtime parameters, and dedicated AI Agent Protocol attribution subsection).
5. The standard Bioconductor skill execution citation (from `AGENTS.md`).

## Examples

**User**: "Search for a metagenomics taxonomy protocol and run it"

**Skill produces**:
- A short list of matching protocols with version, status, trust tier, and description
- A request for the user to confirm which protocol to run
- A method provenance block before any execution begins
- The executed steps and logs
- A departures summary after the protocol finishes
- A drafted narrative Methods section with inline citations for the user's manuscript

## Notes

- Trust scores and popularity metrics are reserved for a future release, but `trust_tier` from the registry should be displayed if available.

