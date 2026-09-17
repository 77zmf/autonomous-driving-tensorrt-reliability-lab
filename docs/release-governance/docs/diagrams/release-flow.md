# Autoware Release Flow

```mermaid
flowchart TD
    A[feature / fix] --> B[test/* branch]
    B --> C[point repos to test branches]
    C --> D[test commit]
    D --> E{test pass?}
    E -- no --> C
    E -- yes --> F[lock dependency commits]
    F --> G[merge to main]
    G --> H[tag beta]
    H --> I[tag release]
