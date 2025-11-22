# Agent Research Command

Comprehensive research and analysis using multiple sources and industry-standard research methodologies.

## Usage
/agent-research "your research question or topic"

## Examples
/agent-research "Best practices for database sharding"
/agent-research "Compare React vs Vue vs Angular for enterprise applications"
/agent-research "Latest trends in microservices architecture patterns"

## Features
- **Multi-Source Analysis**: Searches documentation, academic papers, and industry blogs
- **Comparative Analysis**: Side-by-side feature and performance comparisons
- **Expert Opinion Synthesis**: Aggregates insights from industry leaders
- **Implementation Patterns**: Real-world examples and case studies
- **Best Practices**: Proven approaches and common pitfalls

## Research Methodology
1. **Define Scope**: Clear research questions and success criteria
2. **Source Identification**: Authoritative documentation and expert sources
3. **Data Collection**: Systematic gathering of information
4. **Analysis**: Critical evaluation and synthesis
5. **Recommendations**: Actionable insights based on findings

## Example Output
```
🔬 Research Report: Best Practices for Database Sharding

## Executive Summary
Database sharding is essential for scaling beyond single-node capacity.
Key approaches include horizontal range-based, hash-based, and directory-based sharding.

## Key Findings

### 1. Sharding Strategies (Ranked by Maturity)
**Range-Based Sharding** ⭐⭐⭐⭐⭐
- Pros: Simple to understand, range queries efficient
- Cons: Uneven distribution, hot spots possible
- Best for: Time-series data, geographic data

**Hash-Based Sharding** ⭐⭐⭐⭐
- Pros: Even distribution, no hot spots
- Cons: Range queries expensive, rehashing complex
- Best for: Key-value stores, user data

**Directory-Based Sharding** ⭐⭐⭐
- Pros: Flexible mapping, easy rebalancing
- Cons: Additional lookup overhead, directory single point
- Best for: Multi-tenant applications

### 2. Industry Implementation Patterns
**Twitter**: Range-based for timeline data
**Instagram**: Hash-based for user data
**Shopify**: Directory-based for multi-tenant

### 3. Common Pitfalls & Solutions
- **Cross-Shard Joins**: Denormalize or use application joins
- **Hot Spots**: Implement consistent hashing
- **Rebalancing**: Plan for future growth from day one

## Recommendations
1. Start with hash-based sharding for user data
2. Implement application-level joins for complex queries
3. Monitor shard balance and implement auto-rebalancing
4. Plan for 2x growth capacity per shard

## Implementation Timeline: 6-12 months
## Complexity: High
## Required Expertise: Database engineering, Distributed systems
```