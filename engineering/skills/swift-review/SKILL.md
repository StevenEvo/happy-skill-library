---
name: swift-review
description: Review Swift changes against project conventions.
context: fork
agent: Explore
paths: "**/*.swift"
allowed-tools: Read Grep
---

Review the Swift diff for retain cycles, main-actor violations, and force unwraps.
