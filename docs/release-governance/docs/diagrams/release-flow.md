# Release evidence flow

Generic process draft; each adopting project defines its own target gates.

```mermaid
flowchart TD
    A[Candidate revision] --> B[Pin dependencies and build inputs]
    B --> C[Build and identify artifact]
    C --> D[Execute required tests]
    D --> E{Required evidence passes?}
    E -- no --> F[Record failure or blocker]
    F --> A
    E -- yes --> G[Owner reviews evidence and recovery plan]
    G --> H{Promotion approved?}
    H -- no --> F
    H -- yes --> I[Promote exact tested artifact and immutable tag]
    I --> J[Separately authorized deployment]
    J --> K[Target verification and monitoring]
```

Changed source, dependencies, configuration, or artifacts require impact
review and appropriate revalidation before promotion.
