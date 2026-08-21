# 0002. Federated Protocol Repositories

- **Status:** Accepted
- **Date:** 2026-08-08
- **Deciders:** Levi (User), AI Agent

## Context and Problem Statement

We want to enable AI agents to execute complete, reproducible workflows composed of citable protocols. While `bioconductor/ai-agent-skills` houses "skills" (which orchestrate agent behavior), these skills are not the right venue for hosting domain-specific, scientifically-validated methods. We need a way to decouple *how* an agent runs a protocol from *where* that protocol's content lives, allowing domain experts to publish and maintain protocols independently without contributing directly to this central repository. Furthermore, these protocols must be strictly citable, preserving provenance, author attribution, and connections to peer-reviewed literature.

## Decision

We will implement a **Federated Protocol Repository** architecture.

1. **Separation of Concerns**: The `bioconductor/ai-agent-skills` repository will host a single generic runner skill (`bioc-protocol-runner`). It will not host protocol content.
2. **Federation via Indexing**: Domain experts will publish protocols in their own GitHub repositories (e.g., `waldronlab/ai-agent-protocols`). These repositories will generate a machine-readable index (`PROTOCOLS.yaml`).
3. **Discovery**: The `bioc-protocol-runner` skill will be responsible for querying these indexes, fetching `registry.yaml` from registered repositories, and matching user requests to available protocols.
4. **Citation Mandate & Methods Drafting**: The runner skill is strictly mandated to:
   - Emit a standard **Method Provenance** block before executing any protocol. This block composes citations at two levels:
     - **Level 1**: The protocol itself (Author, Protocol Name, Version, Date, and Protocol/Repository/Publication DOI).
     - **Level 2**: Primary literature referenced by the protocol (DOIs/PMIDs). For atomic protocols, this is derived from the machine-readable `citation` frontmatter field. For composite protocols, this is the aggregation of Level 2 citations from all constituent atomic protocols.
   - Generate a publication-ready **Draft Methods Section** after execution that embeds inline tool/method DOIs, details parameter departures, and includes a dedicated subsection citing the executed protocol artifact.

## Alternatives Considered

- **Hosting protocols as skills**: We considered writing each protocol as a standalone skill in this repository (e.g., a `run-16s-qc` skill). Rejected because it conflates execution logic with scientific content, makes the central repository a bottleneck for domain experts, and dilutes the purpose of an "agent skill".
- **Dynamic API fetching vs. CI Indexing**: We considered having the runner skill dynamically use the GitHub API to search registered repositories. We opted instead to have repositories generate static `PROTOCOLS.yaml` indices that the runner can quickly fetch, ensuring stability and removing runtime API limits.

## Consequences

- **Decentralization**: Labs and working groups can maintain their own protocols with their own review processes and DOIs.
- **Agent Consistency**: Regardless of which protocol is run, the agent will always enforce strict citation output.
- **Complex Dependency Management**: We will need rules for how protocols in one repository depend on protocols in another (Phase 1 limits this to single-level execution dependencies).
