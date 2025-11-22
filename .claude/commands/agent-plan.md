# Agent Plan Command

Strategic planning and task breakdown using industry-standard AI agent frameworks.

## Usage
/agent-plan "your objective or project description"

## Examples
/agent-plan "Build a REST API for user authentication"
/agent-plan "Migrate from SQLite to PostgreSQL"
/agent-plan "Implement automated testing pipeline"

## Features
- **Strategic Planning**: Breaks down complex objectives into manageable phases
- **Task Decomposition**: Creates detailed action items with dependencies
- **Risk Assessment**: Identifies potential blockers and mitigation strategies
- **Resource Planning**: Estimates time, complexity, and required skills
- **Industry Standards**: Uses proven project management methodologies

## Example Output
```
🎯 Strategic Plan: Build a REST API for User Authentication

## Phase 1: Foundation & Design (Week 1)
- [ ] Research authentication standards (JWT, OAuth2, Session-based)
- [ ] Design API endpoints (/auth/login, /auth/register, /auth/refresh)
- [ ] Choose technology stack (Express.js, FastAPI, Spring Boot)
- [ ] Define database schema for users and sessions

## Phase 2: Core Implementation (Week 2-3)
- [ ] Implement user registration endpoint
- [ ] Implement user login endpoint
- [ ] Add password hashing (bcrypt, Argon2)
- [ ] Create JWT token generation/validation

## Phase 3: Security & Validation (Week 4)
- [ ] Add input validation and sanitization
- [ ] Implement rate limiting
- [ ] Add account lockout mechanisms
- [ ] Security audit and penetration testing

## Risk Assessment
- **High**: Security vulnerabilities → Mitigate with security audit
- **Medium**: Performance bottlenecks → Implement caching strategies
- **Low**: Integration issues → Plan API versioning

## Estimated Timeline: 4 weeks
## Complexity: Intermediate
## Required Skills: Backend development, Security, Database design
```