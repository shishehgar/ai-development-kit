# AIDK Studio Architecture

## Layers

### Frontend

React, TypeScript and Vite.

Responsibilities:

- User interface
- Project navigation
- Forms and validation
- Reports and dashboards
- Contextual help
- API communication

The frontend must not execute operating-system commands directly.

### Backend

FastAPI application.

Responsibilities:

- API endpoints
- Request validation
- Task execution
- Progress reporting
- Security controls
- Access to AIDK services

### Domain layer

Existing AIDK Python modules.

Responsibilities:

- Workspace inspection
- Git inspection
- Engineering audit
- Improvement planning
- Safe fixes
- Dependency inspection
- Database operations
- Report generation

### Help system

Structured Markdown and JSON help content.

Each feature must provide:

- Short description
- Detailed explanation
- Usage procedure
- CLI equivalent
- Safety level
- Common errors
- Recovery instructions
