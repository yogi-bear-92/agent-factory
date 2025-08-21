# Warp Drive Prompts - Agent Factory Commands

This document contains all 32+ commands from the agent-factory project, formatted for easy creation in Warp Drive.

## How to Use This Guide

1. Open Warp Drive (notebooks feature)
2. Create a new notebook for each category
3. Copy and paste the command content from each section below
4. Use the command names as notebook titles

---

## 🚀 PRP Commands (Core Development)

### 1. prp-base-create

**Name**: `prp-base-create`  
**Description**: Create comprehensive PRPs with research  
**Command**:
```
# Create BASE PRP

## Feature: {{feature_name}}

## PRP Creation Mission

Create a comprehensive PRP that enables **one-pass implementation success** through systematic research and context curation.

**Critical Understanding**: The executing AI agent only receives:

- Start by reading and understanding the prp concepts PRPs/README.md
- The PRP content you create
- Its training data knowledge
- Access to codebase files (but needs guidance on which ones)

**Therefore**: Your research and context curation directly determines implementation success. Incomplete context = implementation failure.

## Research Process

> During the research process, create clear tasks and spawn as many agents and subagents as needed using the batch tools. The deeper research we do here the better the PRP will be. we optimize for chance of success and not for speed.

1. **Codebase Analysis in depth**
   - Create clear todos and spawn subagents to search the codebase for similar features/patterns Think hard and plan your approach
   - Identify all the necessary files to reference in the PRP
   - Note all existing conventions to follow
   - Check existing test patterns for validation approach
   - Use the batch tools to spawn subagents to search the codebase for similar features/patterns

2. **External Research at scale**
   - Create clear todos and spawn with instructions subagents to do deep research for similar features/patterns online and include urls to documentation and examples
   - Library documentation (include specific URLs)
   - For critical pieces of documentation add a .md file to PRPs/ai_docs and reference it in the PRP with clear reasoning and instructions
   - Implementation examples (GitHub/StackOverflow/blogs)
   - Best practices and common pitfalls found during research
   - Use the batch tools to spawn subagents to search for similar features/patterns online and include urls to documentation and examples

3. **User Clarification**
   - Ask for clarification if you need it

## PRP Generation Process

### Step 1: Choose Template

Use `PRPs/templates/prp_base.md` as your template structure - it contains all necessary sections and formatting.

### Step 2: Context Completeness Validation

Before writing, apply the **"No Prior Knowledge" test** from the template:
_"If someone knew nothing about this codebase, would they have everything needed to implement this successfully?"_

### Step 3: Research Integration

Transform your research findings into the template sections:

**Goal Section**: Use research to define specific, measurable Feature Goal and concrete Deliverable
**Context Section**: Populate YAML structure with your research findings - specific URLs, file patterns, gotchas
**Implementation Tasks**: Create dependency-ordered tasks using information-dense keywords from codebase analysis
**Validation Gates**: Use project-specific validation commands that you've verified work in this codebase

### Step 4: Information Density Standards

Ensure every reference is **specific and actionable**:

- URLs include section anchors, not just domain names
- File references include specific patterns to follow, not generic mentions
- Task specifications include exact naming conventions and placement
- Validation commands are project-specific and executable

### Step 5: ULTRATHINK Before Writing

After research completion, create comprehensive PRP writing plan using TodoWrite tool:

- Plan how to structure each template section with your research findings
- Identify gaps that need additional research
- Create systematic approach to filling template with actionable context

## Output

Save as: `PRPs/{feature-name}.md`

## PRP Quality Gates

### Context Completeness Check

- [ ] Passes "No Prior Knowledge" test from template
- [ ] All YAML references are specific and accessible
- [ ] Implementation tasks include exact naming and placement guidance
- [ ] Validation commands are project-specific and verified working

### Template Structure Compliance

- [ ] All required template sections completed
- [ ] Goal section has specific Feature Goal, Deliverable, Success Definition
- [ ] Implementation Tasks follow dependency ordering
- [ ] Final Validation Checklist is comprehensive

### Information Density Standards

- [ ] No generic references - all are specific and actionable
- [ ] File patterns point at specific examples to follow
- [ ] URLs include section anchors for exact guidance
- [ ] Task specifications use information-dense keywords from codebase

## Success Metrics

**Confidence Score**: Rate 1-10 for one-pass implementation success likelihood

**Validation**: The completed PRP should enable an AI agent unfamiliar with the codebase to implement the feature successfully using only the PRP content and codebase access.
```

---

### 2. prp-base-execute

**Name**: `prp-base-execute`  
**Description**: Execute PRPs against codebase  
**Command**:
```
# Execute BASE PRP

## PRP File: {{prp_file}}

## Mission: One-Pass Implementation Success

PRPs enable working code on the first attempt through:

- **Context Completeness**: Everything needed, nothing guessed
- **Progressive Validation**: 4-level gates catch errors early
- **Pattern Consistency**: Follow existing codebase approaches
- Read PRPs/README.md to understand PRP concepts

**Your Goal**: Transform the PRP into working code that passes all validation gates.

## Execution Process

1. **Load PRP**
   - Read the specified PRP file completely
   - Absorb all context, patterns, requirements and gather codebase intelligence
   - Use the provided documentation references and file patterns, consume the right documentation before the appropriate todo/task
   - Trust the PRP's context and guidance - it's designed for one-pass success
   - If needed do additional codebase exploration and research as needed

2. **ULTRATHINK & Plan**
   - Create comprehensive implementation plan following the PRP's task order
   - Break down into clear todos using TodoWrite tool
   - Use subagents for parallel work when beneficial (always create prp inspired prompts for subagents when used)
   - Follow the patterns referenced in the PRP
   - Use specific file paths, class names, and method signatures from PRP context
   - Never guess - always verify the codebase patterns and examples referenced in the PRP yourself

3. **Execute Implementation**
   - Follow the PRP's Implementation Tasks sequence, add more detail as needed, especially when using subagents
   - Use the patterns and examples referenced in the PRP
   - Create files in locations specified by the desired codebase tree
   - Apply naming conventions from the task specifications and CLAUDE.md

4. **Progressive Validation**

   **Execute the level validation system from the PRP:**
   - **Level 1**: Run syntax & style validation commands from PRP
   - **Level 2**: Execute unit test validation from PRP
   - **Level 3**: Run integration testing commands from PRP
   - **Level 4**: Execute specified validation from PRP

   **Each level must pass before proceeding to the next.**

5. **Completion Verification**
   - Work through the Final Validation Checklist in the PRP
   - Verify all Success Criteria from the "What" section are met
   - Confirm all Anti-Patterns were avoided
   - Implementation is ready and working

**Failure Protocol**: When validation fails, use the patterns and gotchas from the PRP to fix issues, then re-run validation until passing.
```

---

### 3. prime-core

**Name**: `prime-core`  
**Description**: Prime Claude with project context  
**Command**:
```
> Command for priming Claude Code with core knowledge about your project

# Prime Context for Claude Code

Use the command `tree` to get an understanding of the project structure.

Start with reading the CLAUDE.md file if it exists to get an understanding of the project.

Read the README.md file to get an understanding of the project.

Read key files in the src/ directory

> List any additional files that are important to understand the project.

Explain back to me:
- Project structure
- Project purpose and goals
- Key files and their purposes
- Any important dependencies
- Any important configuration files
```

---

### 4. review-staged-unstaged

**Name**: `review-staged-unstaged`  
**Description**: Review git changes using PRP methodology  
**Command**:
```
List and review any files in the staging area, both staged and unstaged.
Ensure you look at both new files and modified files.

Check the diff of each file to see what has changed.

Previous review report: {{previous_review}}

May or may not be added, ignore the previous review if not specified.

## Review Focus Areas

1. **Code Quality**
   - Type hints on all functions and classes
   - Pydantic v2 models for data validation
   - No print() statements (use logging)
   - Proper error handling
   - Following PEP 8
   - Docstrings following google style python docstrings

2. **Pydantic v2 Patterns**
   - Using ConfigDict not class Config
   - field_validator not @validator
   - model_dump() not dict()
   - Proper use of Annotated types

3. **Security**
   - Input validation on all endpoints
   - No SQL injection vulnerabilities
   - Passwords properly hashed
   - No hardcoded secrets

4. **Structure**
   - Unit tests are co-located with the code they test in tests/ folders
   - Each feature is self-contained with its own models, service, and tools
   - Shared components are only things used by multiple features
   - Future improvements (like multiple AI providers) would go in src/shared/ai_providers/ when implemented
   - Integration tests remain at the root level in tests/integration/

5. **Linting**
   - ruff check --fix
   - mypy

6. **Testing**
   - New code has tests
   - Edge cases covered
   - Mocking external dependencies

7. **Performance**
   - No N+1 queries
   - Efficient algorithms
   - Proper async usage

8. **Documentation**
   - Clear README with setup instructions
   - CLAUDE.md is up to date with any new important utils, dependencies etc for future cluade code instances

## Review Output

Create a concise review report with:

```markdown
# Code Review #[number]

## Summary
[2-3 sentence overview]

## Issues Found

### 🔴 Critical (Must Fix)
- [Issue with file:line and suggested fix]

### 🟡 Important (Should Fix)
- [Issue with file:line and suggested fix]

### 🟢 Minor (Consider)
- [Improvement suggestions]

## Good Practices
- [What was done well]

## Test Coverage
Current: X% | Required: 80%
Missing tests: [list]
Save report to PRPs/code_reviews/review[#].md (check existing files first)
```
```

---

## 🔧 Development Commands

### 5. debug

**Name**: `debug`  
**Description**: Debug issues with RCA analysis  
**Command**:
```
# Debug Issue

Systematically debug and diagnose the reported problem.

## Problem Description

{{problem_description}}

## Debugging Process

1. **Reproduce the Issue**
   - Get exact steps to reproduce
   - Verify you can see the same problem
   - Note any error messages or logs
   - Document the expected vs actual behavior

2. **Gather Information**

   ```bash
   # Check recent changes
   git log --oneline -10

   # Look for error patterns in logs
   # Search for related error messages
   ```

3. **Isolate the Problem**
   - **Binary Search**: Comment out code sections to narrow down
   - **Git Bisect**: Find when the bug was introduced
   - **Logging**: Add strategic log statements
   - **Debugger**: Set breakpoints if applicable

4. **Common Debugging Strategies**

   ### For Runtime Errors
   - Read the full stack trace
   - Identify the exact line causing the error
   - Check variable values at that point
   - Verify assumptions about data types

   ### For Logic Errors
   - Add print/log statements to trace execution
   - Verify each step produces expected results
   - Check boundary conditions
   - Test with minimal reproducible example

   ### For Performance Issues
   - Add timing measurements
   - Check for N+1 queries
   - Look for inefficient algorithms
   - Profile if necessary

   ### For Integration Issues
   - Verify external service is accessible
   - Check authentication/credentials
   - Validate request/response formats
   - Test with curl/Postman first

5. **Root Cause Analysis**
   - Why did this happen?
   - Why wasn't it caught earlier?
   - Are there similar issues elsewhere?
   - How can we prevent this class of bugs?

6. **Implement Fix**
   - Fix the root cause, not just symptoms
   - Add defensive programming if needed
   - Consider edge cases
   - Keep fix minimal and focused, follow KISS

7. **Verify Resolution**
   - Confirm original issue is fixed
   - Check for regression
   - Test related functionality
   - Add test to prevent recurrence

8. **Document Findings**

   ```markdown
   ## Debug Summary

   ### Issue

   [What was broken]

   ### Root Cause

   [Why it was broken]

   ### Fix

   [What was changed]

   ### Prevention

   [How to avoid similar issues]
   ```

## Debug Checklist

- [ ] Issue reproduced locally
- [ ] Root cause identified
- [ ] Fix implemented
- [ ] Tests added/updated
- [ ] No regressions introduced
- [ ] Documentation updated if needed

Remember: The goal is not just to fix the bug, but to understand why it happened and prevent similar issues in the future.
```

---

### 6. create-pr

**Name**: `create-pr`  
**Description**: Create well-structured pull requests  
**Command**:
```
# Create Pull Request

Create a well-structured pull request with proper description and context.

## PR Title (if provided)
{{pr_title}}

## Process

1. **Prepare Branch**
   ```bash
   # Check current branch
   git branch --show-current
   
   # Ensure we're not on main
   # If on main, create a feature branch
   ```

2. **Review Changes**
   ```bash
   # See what will be included
   git status
   git diff main...HEAD
   ```

3. **Create Commits**
   - Stage relevant files
   - Create logical, atomic commits if not already done
   - Write clear commit messages following conventional commits, do not include any reference to cluade, written by clade etc:
     - `feat:` for new features
     - `fix:` for bug fixes
     - `docs:` for documentation
     - `test:` for tests
     - `refactor:` for refactoring

4. **Push to Remote**
   ```bash
   git push -u origin HEAD
   ```

5. **Create PR**
   ```bash
   gh pr create --title "{{pr_title}}" --body "$(cat <<'EOF'
   ## Summary
   [Brief description of what this PR does]
   
   ## Changes
   - [List key changes]
   - [Be specific]
   
   ## Type of Change
   - [ ] Bug fix
   - [ ] New feature
   - [ ] Breaking change
   - [ ] Documentation update
   
   ## Testing
   - [ ] Tests pass locally
   - [ ] Added new tests
   - [ ] Manual testing completed
   
   ## Checklist
   - [ ] Code follows project style
   - [ ] Self-reviewed
   - [ ] Updated documentation
   - [ ] No console.logs or debug code
   
   ## Screenshots (if applicable)
   [Add screenshots for UI changes]
   
   ## Additional Context
   [Any extra information reviewers should know]
   EOF
   )"
   ```

6. **Post-Creation**
   - Add labels if needed: `gh pr edit --add-label "feature,needs-review"`
   - Request reviewers if known
   - Link to related issues

Remember to:
- Keep PRs focused and small
- Provide context for reviewers
- Test thoroughly before creating PR
```

---

### 7. smart-commit

**Name**: `smart-commit`  
**Description**: Analyze changes and create intelligent commits  
**Command**:
```
---
name: commit
description: Analyze changes and create a smart git commit
arguments: "Additional instructions for the commit"
---

additional instructions = {{additional_instructions}}

type = "feat", "fix", "docs", "style", "refactor", "perf", "test", "chore"

# Smart Git Commit

Please help me create a git commit by:

1. First, check the current git status and analyze what changed:

```bash
git status
git diff --staged
```

2. If no files are staged, show me the changes and help me decide what to stage:

```bash
git diff
git status -s
```

3. Based on the changes, suggest:

- The appropriate commit type (feat/fix/docs/style/refactor/perf/test/chore)
- A concise, descriptive commit message following conventional commits
- If the changes are complex, suggest breaking into multiple commits

4. The commit format should be:

$type: description for simple commits
For complex changes, include a body explaining what and why

5. After showing me the suggested commit message, ask if I want to:

- Use it as-is
- Modify it
- Add more details to the body
- Stage different files

6. Once approved, create the commit and show me the result.

7. Finally, ask if I want to push or create a PR.
```

---

### 8. onboarding

**Name**: `onboarding`  
**Description**: Comprehensive onboarding for new developers  
**Command**:
```
Please perform a comprehensive onboarding analysis for a new developer joining this project. Execute the following steps:

## 1. Project Overview
First, analyze the repository structure and provide:
- Project name, purpose, and main functionality
- Tech stack (languages, frameworks, databases, tools)
- Architecture pattern (MVC, microservices, etc.)
- Key dependencies and their purposes

## 2. Repository Structure
Map out the codebase organization:
- List all top-level directories with their purposes
- Identify where different types of code live (models, controllers, utils, tests)
- Highlight any non-standard or unique organizational patterns
- Note any monorepo structures or submodules

## 3. Getting Started
Create step-by-step setup instructions:
- Prerequisites (required software, versions)
- Environment setup commands
- How to install dependencies
- Configuration files that need to be created/modified
- How to run the project locally
- How to run tests
- How to build for production

## 4. Key Components
Identify and explain the most important files/modules:
- Entry points (main.js, index.py, app.tsx, etc.)
- Core business logic locations
- Database models/schemas
- API endpoints or routes
- Configuration management
- Authentication/authorization implementation

## 5. Development Workflow
Document the development process:
- Git branch naming conventions
- How to create a new feature
- Testing requirements
- Code style/linting rules
- PR process and review guidelines
- CI/CD pipeline overview

## 6. Architecture Decisions
Identify important patterns and decisions:
- Design patterns used and why
- State management approach
- Error handling strategy
- Logging and monitoring setup
- Security measures
- Performance optimizations

## 7. Common Tasks
Provide examples for frequent development tasks:
- How to add a new API endpoint
- How to create a new database model
- How to add a new test
- How to debug common issues
- How to update dependencies

## 8. Potential Gotchas
List things that might trip up new developers:
- Non-obvious configurations
- Required environment variables
- External service dependencies
- Known issues or workarounds
- Performance bottlenecks
- Areas of technical debt

## 9. Documentation and Resources
- Locate existing documentation (README, wikis, docs/)
- API documentation
- Database schemas
- Deployment guides
- Team conventions or style guides

## 10. Next Steps
Create an onboarding checklist for the new developer:
1. Set up development environment
2. Run the project successfully
3. Make a small test change
4. Run the test suite
5. Understand the main user flow
6. Identify area to start contributing

## Output Format
Please create:
1. A comprehensive ONBOARDING.md file at the root of the repository with all above information
2. A QUICKSTART.md with just the essential setup steps
3. suggest updates to the README.md if it's missing critical information (dont uopdate the readme directly)

Focus on clarity and actionability. Assume the developer is experienced but completely new to this codebase.
```

---

## 💡 TypeScript Commands

### 9. prp-ts-create

**Name**: `prp-ts-create`  
**Description**: Create TypeScript-specific PRPs  
**Command**:
```
# Create TypeScript PRP

## Feature: {{feature_name}}

## PRP Creation Mission

Create a comprehensive TypeScript PRP that enables **one-pass implementation success** through systematic research and context curation.

**Critical Understanding**: The executing AI agent only receives:

- Start by reading and understanding the prp concepts PRPs/README.md
- The PRP content you create
- Its training data knowledge
- Access to codebase files (but needs guidance on which ones)

**Therefore**: Your research and context curation directly determines implementation success. Incomplete context = implementation failure.

## Research Process

> During the research process, create clear tasks and spawn as many agents and subagents as needed using the batch tools. The deeper research we do here the better the PRP will be. we optimize for chance of success and not for speed.

1. **TypeScript/React Codebase Analysis in depth**
   - Create clear todos and spawn subagents to search the codebase for similar features/patterns Think hard and plan your approach
   - Identify all the necessary TypeScript files to reference in the PRP
   - Note all existing TypeScript/React conventions to follow
   - Check existing component patterns, hook patterns, and API route patterns
   - Analyze TypeScript interface definitions and type usage patterns
   - Check existing test patterns for React components and TypeScript code validation approach
   - Use the batch tools to spawn subagents to search the codebase for similar features/patterns

2. **TypeScript/React External Research at scale**
   - Create clear todos and spawn with instructions subagents to do deep research for similar features/patterns online and include urls to documentation and examples
   - TypeScript documentation (include specific URLs with version compatibility)
   - React/Next.js documentation (include specific URLs for App Router, Server Components, etc.)
   - For critical pieces of documentation add a .md file to PRPs/ai_docs and reference it in the PRP with clear reasoning and instructions
   - Implementation examples (GitHub/StackOverflow/blogs) specific to TypeScript/React/Next.js
   - Best practices and common pitfalls found during research (TypeScript compilation issues, React hydration, Next.js gotchas)
   - Use the batch tools to spawn subagents to search for similar features/patterns online and include urls to documentation and examples

3. **User Clarification**
   - Ask for clarification if you need it

## PRP Generation Process

### Step 1: Choose Template

Use `PRPs/templates/prp_base_typescript.md` as your template structure - it contains all necessary sections and formatting specific to TypeScript/React development.

### Step 2: Context Completeness Validation

Before writing, apply the **"No Prior Knowledge" test** from the template:
_"If someone knew nothing about this TypeScript/React codebase, would they have everything needed to implement this successfully?"_

### Step 3: Research Integration

Transform your research findings into the template sections:

**Goal Section**: Use research to define specific, measurable Feature Goal and concrete Deliverable (component, API route, integration, etc.)
**Context Section**: Populate YAML structure with your research findings - specific TypeScript/React URLs, file patterns, gotchas
**Implementation Tasks**: Create dependency-ordered tasks using information-dense keywords from TypeScript/React codebase analysis
**Validation Gates**: Use TypeScript/React-specific validation commands that you've verified work in this codebase

### Step 4: TypeScript/React Information Density Standards

Ensure every reference is **specific and actionable** for TypeScript development:

- URLs include section anchors, not just domain names (React docs, TypeScript handbook, Next.js docs)
- File references include specific TypeScript patterns to follow (interfaces, component props, hook patterns)
- Task specifications include exact TypeScript naming conventions and placement (PascalCase components, camelCase props, etc.)
- Validation commands are TypeScript/React-specific and executable (tsc, eslint with TypeScript rules, React Testing Library)

### Step 5: ULTRATHINK Before Writing

After research completion, create comprehensive PRP writing plan using TodoWrite tool:

- Plan how to structure each template section with your TypeScript/React research findings
- Identify gaps that need additional TypeScript/React research
- Create systematic approach to filling template with actionable TypeScript context
- Consider TypeScript compilation dependencies and React component hierarchies

## Output

Save as: `PRPs/{feature-name}.md`

## TypeScript PRP Quality Gates

### Context Completeness Check

- [ ] Passes "No Prior Knowledge" test from TypeScript template
- [ ] All YAML references are specific and accessible (TypeScript/React docs, component examples)
- [ ] Implementation tasks include exact TypeScript naming and placement guidance
- [ ] Validation commands are TypeScript/React-specific and verified working
- [ ] TypeScript interface definitions and component prop types are specified

### Template Structure Compliance

- [ ] All required TypeScript template sections completed
- [ ] Goal section has specific Feature Goal, Deliverable, Success Definition
- [ ] Implementation Tasks follow TypeScript dependency ordering (types → components → pages → tests)
- [ ] Final Validation Checklist includes TypeScript/React-specific validation

### TypeScript/React Information Density Standards

- [ ] No generic references - all are specific to TypeScript/React patterns
- [ ] File patterns include specific TypeScript examples to follow (interfaces, components, hooks)
- [ ] URLs include section anchors for exact TypeScript/React guidance
- [ ] Task specifications use information-dense keywords from TypeScript/React codebase
- [ ] Component patterns specify Server vs Client component usage
- [ ] Type definitions are comprehensive and follow existing patterns

## Success Metrics

**Confidence Score**: Rate 1-10 for one-pass TypeScript implementation success likelihood

**Quality Standard**: Minimum 8/10 required before PRP approval

**Validation**: The completed PRP should enable an AI agent unfamiliar with the TypeScript/React codebase to implement the feature successfully using only the PRP content and codebase access, with full type safety and React best practices.
```

---

### 10. prp-ts-execute

**Name**: `prp-ts-execute`  
**Description**: Execute TypeScript PRPs  
**Command**:
```
# Execute TypeScript PRP

## PRP File: {{prp_file}}

## Mission: One-Pass TypeScript Implementation Success

PRPs enable working TypeScript/React code on the first attempt through:

- **Context Completeness**: Everything needed, nothing guessed
- **Progressive Validation**: 4-level gates catch errors early
- **Pattern Consistency**: Follow existing TypeScript/React codebase approaches
- **Type Safety**: Leverage TypeScript's compile-time error detection
- Read PRPs/README.md to understand PRP concepts

**Your Goal**: Transform the PRP into working TypeScript code that passes all validation gates and maintains type safety.

## Execution Process

1. **Load PRP**
   - Read the specified TypeScript PRP file completely
   - Absorb all context, patterns, requirements and gather codebase intelligence
   - Use the provided documentation references and file patterns, consume the right documentation before the appropriate todo/task
   - Trust the PRP's context and guidance - it's designed for one-pass success
   - If needed do additional codebase exploration and research as needed
   - Pay special attention to TypeScript interfaces, component patterns, and Next.js App Router structure

2. **ULTRATHINK & Plan**
   - Create comprehensive implementation plan following the PRP's task order
   - Break down into clear todos using TodoWrite tool
   - Use subagents for parallel work when beneficial (always create prp inspired prompts for subagents when used)
   - Follow the TypeScript/React patterns referenced in the PRP
   - Use specific file paths, interface names, component names, and type definitions from PRP context
   - Never guess - always verify the codebase patterns and examples referenced in the PRP yourself
   - Consider TypeScript compilation dependencies (types before components, components before pages)

3. **Execute Implementation**
   - Follow the PRP's Implementation Tasks sequence, add more detail as needed, especially when using subagents
   - Use the TypeScript/React patterns and examples referenced in the PRP
   - Create files in locations specified by the desired codebase tree
   - Apply TypeScript naming conventions from the task specifications and CLAUDE.md
   - Ensure proper TypeScript typing throughout (interfaces, props, return types)
   - Follow Next.js App Router patterns for file-based routing

4. **Progressive Validation**

   **Execute the 4-level validation system from the TypeScript PRP:**
   - **Level 1**: Run TypeScript syntax & style validation commands from PRP (ESLint, tsc, Prettier)
   - **Level 2**: Execute component and hook unit test validation from PRP
   - **Level 3**: Run Next.js integration testing commands from PRP (dev server, API routes, production build)
   - **Level 4**: Execute TypeScript/React-specific validation from PRP (E2E, performance, accessibility)

   **Each level must pass before proceeding to the next.**

5. **Completion Verification**
   - Work through the Final Validation Checklist in the PRP
   - Verify all Success Criteria from the "What" section are met
   - Confirm all Anti-Patterns were avoided (especially TypeScript/React-specific ones)
   - Verify TypeScript compilation is successful with no errors
   - Ensure proper Server/Client component separation if using Next.js
   - Implementation is ready and working with full type safety

**Failure Protocol**: When validation fails, use the TypeScript/React patterns and gotchas from the PRP to fix issues, then re-run validation until passing. Pay special attention to:
- TypeScript compilation errors and type mismatches
- React hydration issues between server and client
- Next.js App Router specific requirements
- Component prop interface violations
```

---

## 🔍 Git Operations Commands

### 11. conflict-resolver-general

**Name**: `conflict-resolver-general`  
**Description**: Intelligent merge conflict resolution  
**Command**:
```
You are an expert at resolving Git merge conflicts intelligently. Your task is to resolve all merge conflicts in the current repository.

## Step-by-step process:

1. First, check the current git status to understand the situation
2. Identify all files with merge conflicts
3. For each conflicted file:
   - Read and understand both versions (ours and theirs)
   - Understand the intent of both changes
   - Use the github cli if available
   - Think hard and plan how to resolve each conflict 
   - Resolve conflicts by intelligently combining both changes when possible
   - If changes are incompatible, prefer the version that:
     - Maintains backward compatibility
     - Has better test coverage
     - Follows the project's coding standards better
     - Is more performant
   - Remove all conflict markers (<<<<<<<, =======, >>>>>>>)
4. After resolving each file, verify the syntax is correct
5. Run any relevant tests to ensure nothing is broken
6. Stage the resolved files
7. Provide a summary of all resolutions made

## Important guidelines:

- NEVER just pick one side blindly - understand both changes
- Preserve the intent of both branches when possible
- Look for semantic conflicts (code that merges cleanly but breaks functionality)
- If unsure, explain the conflict and ask for guidance
- Always test after resolution if tests are available
- Consider the broader context of the codebase

## Commands you should use:

- `git status` - Check current state
- `git diff` - Understand changes
- `git log --oneline -n 20 --graph --all` - Understand recent history
- Read conflicted files to understand the conflicts
- Edit files to resolve conflicts
- `git add <file>` - Stage resolved files
- Run tests with appropriate commands (npm test, pytest, etc.)
- Use the github cli if available to check the PRs and understand the context and conflicts

Begin by checking the current git status.
```

---

### 12. smart-resolver

**Name**: `smart-resolver`  
**Description**: Deep codebase-aware conflict resolution  
**Command**:
```
Perform an intelligent merge conflict resolution with deep understanding of our codebase.

## Pre-resolution analysis:

1. Understand what each branch was trying to achieve:
git log --oneline origin/main..HEAD
git log --oneline HEAD..origin/main

2. Check if there are any related issues or PRs:
git log --grep="fix" --grep="feat" --oneline -20
- use the github cli as needed

3. Identify the type of conflicts (feature vs feature, fix vs refactor, etc.)

4. Think hard about your findings and plan accordingly

## Resolution strategy:

### For different file types:

**Source code conflicts (.js, .ts, .py, etc.)**:
- Understand the business logic of both changes
- Merge both features if they're complementary
- If conflicting, check which has better test coverage
- Look for related files that might need updates

**Test file conflicts**:
- Usually merge both sets of tests
- Ensure no duplicate test names
- Update test descriptions if needed

**Configuration files**:
- package.json: Merge dependencies, scripts
- .env.example: Include all new variables
- CI/CD configs: Merge all jobs unless duplicate

**Documentation conflicts**:
- Merge both documentation updates
- Ensure consistency in terminology
- Update table of contents if needed

**Lock files (package-lock.json, poetry.lock)**:
- Delete and regenerate after resolving package.json/pyproject.toml

## Post-resolution verification:

1. Run linters to check code style
2. Run type checkers if applicable  
3. Run test suite
4. Check for semantic conflicts (code that merges but breaks functionality)
5. Verify no debugging code was left in

## Final steps:

1. Create a detailed summary of all resolutions
2. If any resolutions are uncertain, mark them with TODO comments
3. Suggest additional testing that might be needed
4. Stage all resolved files

Begin by analyzing the current conflict situation with git status and understanding both branches.
```

---

## 🎯 Advanced PRP Commands

### 13. prp-planning-create

**Name**: `prp-planning-create`  
**Description**: Create planning documents with diagrams  
**Command**:
```
# Create PLANNING PRP (Advanced)

Transform rough ideas into comprehensive PRDs with rich visual documentation.

## Idea: {{idea_description}}

## Discovery Process

1. **Concept Expansion**
   - Break down the core idea
   - Define success criteria
   - Map to business goals if provided

2. **Market & Technical Research**
   - Do deep web search for the following:
     - Market analysis
     - Competitor analysis
     - Technical feasibility study
     - Best practice examples
     - Integration possibilities

3. **User Research & Clarification**
     - Ask user for the following if not provided:
     - Target user personas?
     - Key pain points?
     - Success metrics?
     - Constraints/requirements?

## PRD Generation

Using /PRPs/templates/prp_planning_base.md:

### Visual Documentation Plan
```yaml
diagrams_needed:
  user_flows:
    - Happy path journey
    - Error scenarios
    - Edge cases
  
  architecture:
    - System components
    - Data flow
    - Integration points
  
  sequences:
    - API interactions
    - Event flows
    - State changes
  
  data_models:
    - Entity relationships
    - Schema design
    - State machines
```

### Research Integration
- **Market Analysis**: Include findings in PRD
- **Technical Options**: Compare approaches
- **Risk Assessment**: With mitigation strategies
- **Success Metrics**: Specific, measurable

### User Story Development
```markdown
## Epic: [High-level feature]

### Story 1: [User need]
**As a** [user type]
**I want** [capability]
**So that** [benefit]

**Acceptance Criteria:**
- [ ] Specific behavior
- [ ] Edge case handling
- [ ] Performance requirement

**Technical Notes:**
- Implementation approach
- API implications
- Data requirements
```

### Implementation Strategy
- Phases with dependencies (no dates)
- Priority ordering
- MVP vs enhanced features
- Technical prerequisites

## User Interaction Points

1. **Idea Validation**
   - Confirm understanding
   - Clarify ambiguities
   - Set boundaries

2. **Research Review**
   - Share findings
   - Validate assumptions
   - Adjust direction

3. **PRD Draft Review**
   - Architecture approval
   - Risk acknowledgment
   - Success metric agreement

## Diagram Guidelines
- Use Mermaid for all diagrams
- Include legends where needed
- Show error paths
- Annotate complex flows

## Output Structure
```markdown
1. Executive Summary
2. Problem & Solution
3. User Stories (with diagrams)
4. Technical Architecture (with diagrams)
5. API Specifications
6. Data Models
7. Implementation Phases
8. Risks & Mitigations
9. Success Metrics
10. Appendices
```

Save as: `PRPs/{feature-name}-prd.md`

## Quality Checklist
- [ ] Problem clearly articulated
- [ ] Solution addresses problem
- [ ] All user flows diagrammed
- [ ] Wireframes included if needed
- [ ] Architecture visualized
- [ ] APIs fully specified with examples
- [ ] Data models included
- [ ] Dependencies identified
- [ ] Risks identified and mitigated
- [ ] Success metrics measurable
- [ ] Implementation phases logical
- [ ] Ready for implementation PRP

Remember: Great PRDs prevent implementation confusion.
```

---

### 14. api-contract-define

**Name**: `api-contract-define`  
**Description**: Define API contracts between frontend/backend  
**Command**:
```
# Define API Contract Between Backend and Frontend

Feature: {{feature_name}}

## Task: Create detailed API contract specification for backend/frontend coordination

1. **Define RESTful endpoints**:

   ```yaml
   Base URL: /api/v1/{feature}

   Endpoints:
   - GET /api/v1/{features}
     Query params: page, size, sort, filter
     Response: Page<{Feature}Response>

   - GET /api/v1/{features}/{id}
     Path param: id (Long)
     Response: {Feature}Response

   - POST /api/v1/{features}
     Body: {Feature}Request
     Response: {Feature}Response (201 Created)

   - PUT /api/v1/{features}/{id}
     Path param: id (Long)
     Body: {Feature}Request
     Response: {Feature}Response

   - DELETE /api/v1/{features}/{id}
     Path param: id (Long)
     Response: 204 No Content
   ```

2. **Define request/response DTOs**:

   ```typescript
   // Request DTO (for POST/PUT)
   interface {Feature}Request {
     name: string;        // min: 2, max: 100
     description?: string; // max: 1000
     // Add domain-specific fields
   }

   // Response DTO (for GET)
   interface {Feature}Response {
     id: number;
     name: string;
     description?: string;
     createdAt: string;   // ISO 8601
     updatedAt: string;   // ISO 8601
     // Add computed fields
   }

   // Page response wrapper
   interface Page<T> {
     content: T[];
     totalElements: number;
     totalPages: number;
     size: number;
     number: number;
   }
   ```

3. **Define error responses**:

   ```json
   {
     "timestamp": "2024-01-20T10:30:00Z",
     "status": 400,
     "error": "Bad Request",
     "message": "Validation failed",
     "path": "/api/v1/{features}",
     "errors": [
       {
         "field": "name",
         "message": "Name is required"
       }
     ]
   }
   ```

4. **Define validation rules**:
   - Backend: Bean Validation annotations
   - Frontend: Matching Zod schemas

   ```
   name: required, 2-100 chars
   description: optional, max 1000 chars
   email: valid email format
   date: ISO 8601 format
   ```

5. **Define status codes**:
   - 200: OK (GET, PUT)
   - 201: Created (POST)
   - 204: No Content (DELETE)
   - 400: Bad Request (validation)
   - 404: Not Found
   - 409: Conflict (duplicate)
   - 500: Internal Server Error

6. **Integration requirements**:
   - CORS: Allow frontend origin
   - Content-Type: application/json
   - Authentication: Bearer token (if needed)
   - Pagination: Spring Pageable format
   - Sorting: field,direction (e.g., "name,asc")

7. **Backend implementation notes**:

   ```java
   // Entity fields match response DTO
   // Use MapStruct for DTO mapping
   // Repository method naming conventions
   // Service layer validation
   ```

8. **Frontend implementation notes**:
   ```typescript
   // Zod schemas match validation rules
   // API client with base configuration
   // TanStack Query hooks
   // Error handling utilities
   ```

Save this contract as: `PRPs/contracts/{feature}-api-contract.md`

Share this file between backend and frontend teams for alignment.
```

---

## 🚀 Rapid Development Commands

### 15. parallel-prp-creation

**Name**: `parallel-prp-creation`  
**Description**: Create multiple PRP variations in parallel  
**Command**: 
```
---
name: parallel-prp-creation
description: Create multiple PRP variations in parallel for comparative analysis and implementation strategy validation
arguments:
  - name: prp_name
    description: The base name for the PRP (e.g., "user-authentication")
  - name: implementation_details
    description: Core feature requirements and context
  - name: number_of_parallel_prps
    description: Number of parallel PRP variations to create (recommended 2-5)
---

# Parallel PRP Creation - Multiple Implementation Strategies

Generate {{number_of_parallel_prps}} parallel PRP variations for comparative analysis and implementation approach validation. This command leverages multiple AI agents working simultaneously to create different implementation strategies for the same feature, enabling selection of the optimal approach.

## Overview

This workflow creates **{{number_of_parallel_prps}}** independent PRP variations:

- Each agent researches the same feature from different architectural perspectives
- Each agent creates a complete PRP with distinct implementation approaches
- All agents work concurrently for maximum efficiency
- Results enable comparative analysis and strategy selection

## Execution Parameters

PRP_NAME: {{prp_name}}
IMPLEMENTATION_DETAILS: {{implementation_details}}
NUMBER_OF_PARALLEL_PRPs: {{number_of_parallel_prps}}

## Parallel Agent Coordination

**CRITICAL**: Execute all agents simultaneously using multiple Task tool calls in a single response. Do not wait for one agent to complete before starting the next.

## Agent Assignment Strategy

Each agent approaches the same feature with different focus areas:

### Agent Specialization Matrix

```yaml
Agent 1: Performance-Optimized Approach
  Focus: Scalability, caching, optimization
  Architecture: High-performance patterns
  Validation: Load testing, performance metrics

Agent 2: Security-First Approach
  Focus: Security, validation, authentication
  Architecture: Defense-in-depth patterns
  Validation: Security testing, penetration testing

Agent 3: Maintainability-Focused Approach
  Focus: Clean code, modularity, testing
  Architecture: SOLID principles, design patterns
  Validation: Unit testing, code quality

Agent 4: Rapid-Development Approach
  Focus: Quick implementation, minimal complexity
  Architecture: Simplified patterns, frameworks
  Validation: Integration testing, functionality

Agent 5: Enterprise-Grade Approach
  Focus: Robustness, monitoring, observability
  Architecture: Enterprise patterns, microservices
  Validation: End-to-end testing, monitoring
```

## Parallel Execution Commands

Execute these agents concurrently:

```
Use the Task tool to run these {{number_of_parallel_prps}} agents in PARALLEL for feature: {{prp_name}}

Implementation Details: {{implementation_details}}
```

### Expected Outputs

Upon completion, you will have:

```
PRPs/
├── {{prp_name}}-1.md    # Performance-optimized approach
├── {{prp_name}}-2.md    # Security-first approach
├── {{prp_name}}-3.md    # Maintainability-focused approach
├── {{prp_name}}-4.md    # Rapid-development approach
├── {{prp_name}}-5.md    # Enterprise-grade approach

Root Directory/
├── RESULTS_{{prp_name}}-1.md    # Performance approach analysis
├── RESULTS_{{prp_name}}-2.md    # Security approach analysis
├── RESULTS_{{prp_name}}-3.md    # Maintainability approach analysis
├── RESULTS_{{prp_name}}-4.md    # Rapid development approach analysis
├── RESULTS_{{prp_name}}-5.md    # Enterprise approach analysis
```

This parallel approach maximizes the probability of identifying the optimal implementation strategy by exploring multiple architectural approaches simultaneously, enabling data-driven selection of the best approach for your specific requirements.
```

---

## Summary

I've provided you with **15 core commands** formatted for Warp Drive creation. These represent the most essential commands from your agent-factory project:

### **Core PRP Workflow** (5 commands):
1. `prp-base-create` - Create comprehensive PRPs
2. `prp-base-execute` - Execute PRPs 
3. `prime-core` - Prime with project context
4. `review-staged-unstaged` - Review changes
5. `parallel-prp-creation` - Create multiple PRP variations

### **Development Tools** (4 commands):
6. `debug` - Debug with RCA analysis
7. `create-pr` - Create structured PRs
8. `smart-commit` - Intelligent commits
9. `onboarding` - Developer onboarding

### **TypeScript Support** (2 commands):
10. `prp-ts-create` - TypeScript PRPs
11. `prp-ts-execute` - Execute TypeScript PRPs

### **Git Operations** (2 commands):
12. `conflict-resolver-general` - Resolve conflicts
13. `smart-resolver` - Smart conflict resolution

### **Advanced Features** (2 commands):
14. `prp-planning-create` - Planning with diagrams
15. `api-contract-define` - API contracts

## Next Steps

1. **Copy each command above into Warp Drive** as separate notebooks
2. **Test with core workflow**: Start with `prime-core`, then `prp-base-create`, then `prp-base-execute`
3. **Add remaining commands** from the original files as needed

---

## 📋 Additional PRP Commands

### 16. prp-spec-create

**Name**: `prp-spec-create`  
**Description**: Generate specification-driven PRPs  
**Command**:
```
# Create SPEC PRP (Advanced)

Generate a comprehensive specification-driven PRP with clear transformation goals.

## Specification: {{specification_description}}

## Analysis Process

1. **Current State Assessment**
   - Map existing implementation
   - Identify pain points
   - Document technical debt
   - Note integration points

2. **Desired State Research**
   - Best practices for target state
   - Implementation examples
   - Migration strategies
   - Risk assessment
   - Dependency mapping

3. **User Clarification**
   - Confirm transformation goals
   - Priority of objectives
   - Acceptable trade-offs

## PRP Generation

Using /PRPs/templates/prp_spec.md:

### State Documentation

```yaml
current_state:
  files: [list affected files]
  behavior: [how it works now]
  issues: [specific problems]

desired_state:
  files: [expected structure]
  behavior: [target functionality]
  benefits: [improvements gained]
```

### Hierarchical Objectives

1. **High-Level**: Overall transformation goal
2. **Mid-Level**: Major milestones
3. **Low-Level**: Specific tasks with validation

### Task Specification with information dense keywords

#### Information dense keywords:

- MIRROR: Mirror the state of existing code to be mirrored to another use case
- COPY: Copy the state of existing code to be copied to another use case
- ADD: Add new code to the codebase
- MODIFY: Modify existing code
- DELETE: Delete existing code
- RENAME: Rename existing code
- MOVE: Move existing code
- REPLACE: Replace existing code
- CREATE: Create new code

#### Example:

```yaml
task_name:
  action: MODIFY/CREATE
  file: path/to/file
  changes: |
    - Specific modifications
    - Implementation details
    - With clear markers
  validation:
    - command: "test command"
    - expect: "success criteria"
```

### Implementation Strategy

- Identify dependencies
- Order tasks by priority and implementation order and dependencies logic
- Include rollback plans
- Progressive enhancement

## User Interaction Points

1. **Objective Validation**
   - Review hierarchical breakdown
   - Confirm priorities
   - Identify missing pieces

2. **Risk Review**
   - Document identified risks
   - Find mitigations
   - Set go/no-go criteria

## Context Requirements

- Current implementation details
- Target architecture examples
- Migration best practices
- Testing strategies

## Output

Save as: `SPEC_PRP/PRPs/{spec-name}.md`

## Quality Checklist

- [ ] Current state fully documented
- [ ] Desired state clearly defined
- [ ] All objectives measurable
- [ ] Tasks ordered by dependency
- [ ] Each task has validation that AI can run
- [ ] Risks identified with mitigations
- [ ] Rollback strategy included
- [ ] Integration points noted

Remember: Focus on the transformation journey, not just the destination.
```

---

### 17. prp-spec-execute

**Name**: `prp-spec-execute`  
**Description**: Execute specification PRPs  
**Command**:
```
# Execute SPEC PRP

Implement a specification using an existing SPEC PRP.

## PRP File: {{prp_file}}

## Execution Process

1. **Understand Spec**
   - Current state analysis
   - Desired state goals
   - Task dependencies

2. **ULTRATHINK**
   - Think hard before you execute the plan. Create a comprehensive plan addressing all requirements.
   - Break down complex tasks into smaller, manageable steps using your todos tools.
   - Use the TodoWrite tool to create and track your implementation plan.
   - Identify implementation patterns from existing code to follow.

3. **Execute Tasks**
   - Follow task order
   - Run validation after each
   - Fix failures before proceeding

4. **Verify Transformation**
   - Confirm desired state achieved
   - Run all validation gates
   - Test integration

Progress through each objective systematically.
```

---

### 18. prp-task-create

**Name**: `prp-task-create`  
**Description**: Generate task-focused PRPs  
**Command**:
```
# Create TASK PRP (Advanced)

Generate a comprehensive task list for focused changes with validation.

## Task: {{task_description}}

## Analysis Process

1. **Scope Definition**
   - Identify all affected files
   - Map dependencies
   - Check for side effects
   - Note test coverage

2. **Pattern Research**
   - Find similar changes in history
   - Identify conventions to follow
   - Check for helper functions
   - Review test patterns

3. **User Clarification**
   - Confirm change scope
   - Verify acceptance criteria
   - Check deployment considerations
   - Identify blockers

## PRP Generation

**READ**
Using TASK_PRP/PRPs/prp_task.md format:

### Context Section

```yaml
context:
  docs:
    - url: [API documentation]
      focus: [specific methods]

  patterns:
    - file: existing/example.py
      copy: [pattern to follow]

  gotchas:
    - issue: "Library requires X"
      fix: "Always do Y first"
```

### Task Structure

```
ACTION path/to/file:
  - OPERATION: [specific change]
  - VALIDATE: [test command]
  - IF_FAIL: [debug strategy]
  - ROLLBACK: [undo approach]
```

### Task Sequencing

1. **Setup Tasks**: Prerequisites
2. **Core Changes**: Main modifications
3. **Integration**: Connect components
4. **Validation**: Comprehensive tests
5. **Cleanup**: Remove temp code

### Validation Strategy

- Unit test after each change
- Integration test after groups
- Performance check if relevant
- Security scan for sensitive areas

## User Interaction Points

1. **Task Review**
   - Confirm task breakdown
   - Validate sequencing
   - Check completeness

2. **Risk Assessment**
   - Review potential impacts
   - Confirm rollback approach
   - Set success criteria

## Critical Elements

- Include debug patterns
- Add performance checks
- Note security concerns
- Document assumptions

## Output

Save as: `TASK_PRP/PRPs/{task-name}.md`

## Quality Checklist

- [ ] All changes identified
- [ ] Dependencies mapped
- [ ] Each task has validation
- [ ] Rollback steps included
- [ ] Debug strategies provided
- [ ] Performance impact noted
- [ ] Security checked
- [ ] No missing edge cases

Remember: Small, focused changes with immediate validation.
```

---

### 19. prp-task-execute

**Name**: `prp-task-execute`  
**Description**: Execute task PRPs  
**Command**:
```
# Execute TASK PRP

Run through a task list from an existing TASK PRP.

## PRP File: {{prp_file}}

## Execution Process

1. **Load Tasks**
   - Read task list
   - Understand context

2. **Execute Each Task**
   - Perform ACTION
   - Run VALIDATE
   - Fix IF_FAIL issues

3. **Complete Checklist**
   - Verify all tasks done
   - Run final validation
   - Check no regressions

Work through tasks sequentially, validating each.
```

---

### 20. task-list-init

**Name**: `task-list-init`  
**Description**: Create task lists for PRP execution  
**Command**:
```
claude
\*\* Create a comprehensive task list in PRPs/checklist.md for PRP {{prp_name}}

Ingest the infomration then dig deep into our existing codebase and PRP, When done ->

ULTRATHINK about the PRP task and create the plan based adhering to claude.md and extract and refine detailed tasks following this principle:

### list of tasks to be completed to fullfill the PRP in the order they should be completed using infomration dense keywords

- Infomration dense keyword examples:
  ADD, CREATE, MODIFY, MIRROR, FIND, EXECUTE, KEEP, PRESERVE etc

Mark done tasks with: STATUS [DONE], if not done leave empty

```yaml
Task 1:
STATUS [ ]
MODIFY src/existing_module.py:
  - FIND pattern: "class OldImplementation"
  - INJECT after line containing "def __init__"
  - PRESERVE existing method signatures

STATUS [ ]
CREATE src/new_feature.py:
  - MIRROR pattern from: src/similar_feature.py
  - MODIFY class name and core logic
  - KEEP error handling pattern identical

...(...)

Task N:
...

```

Each task should have unit test coverage, make tests pass on each task
```

---

## 🚀 Advanced Rapid Development Commands

### 21. create-base-prp-parallel

**Name**: `create-base-prp-parallel`  
**Description**: Create BASE PRP with parallel research  
**Command**:
```
# Create BASE PRP with Parallel Research

## Feature: {{feature_name}}

Generate a comprehensive PRP using parallel research agents for maximum context gathering efficiency and depth. This command leverages multiple AI agents working simultaneously to research different aspects of the feature, ensuring comprehensive context is passed to enable self-validation and iterative refinement.

## Parallel Research Phase

**IMPORTANT**: Execute the following 4 research agents simultaneously using multiple Agent tool calls in a single response to maximize research efficiency.

### Research Agent Coordination

Launch these agents concurrently - do not wait for one to complete before starting the next:

#### Agent 1: Codebase Pattern Analysis
```
Task: Codebase Context Research
Prompt: Analyze the codebase for patterns relevant to "{{feature_name}}". Research and identify:
- Similar features/patterns already implemented in the codebase
- Files that contain relevant examples or patterns to reference
- Existing conventions, architectural patterns, and code styles to follow
- Test patterns and validation approaches used in similar features
- Integration points and dependencies to consider
- File structure and organization patterns to mirror

Focus on codebase exploration only - do not write code. Use Glob, Grep, and Read tools extensively. Return a comprehensive analysis of existing patterns with specific file paths and code examples to reference in the PRP.
```

#### Agent 2: External Technical Research
```
Task: External Technical Research
Prompt: Research external technical resources for "{{feature_name}}". Investigate:
- Library documentation and API references (include specific URLs)
- Implementation examples from GitHub, StackOverflow, and technical blogs
- Best practices and architectural patterns for similar features
- Common pitfalls, gotchas, and solutions
- Performance considerations and optimization techniques
- Security considerations and vulnerability patterns

Focus purely on research - do not write code. Use web search extensively. Return comprehensive technical research with specific URLs, code examples, and implementation guidance.
```

#### Agent 3: Testing & Validation Strategy
```
Task: Testing Strategy Research
Prompt: Research testing and validation approaches for "{{feature_name}}". Analyze:
- Test patterns used in the current codebase
- Unit testing strategies and frameworks
- Integration testing approaches
- Validation gates and quality checks
- Error handling and edge case patterns
- Performance testing considerations

Research only - no test implementation. Use codebase analysis and web search. Return detailed testing strategy with specific patterns to follow and validation commands to include in the PRP.
```

#### Agent 4: Documentation & Context Research
```
Task: Documentation Context Research
Prompt: Research documentation and context resources for "{{feature_name}}". Gather:
- Check PRPs/ai_docs/ for relevant documentation files
- Configuration examples and setup patterns
- Environment and dependency requirements
- Known issues and workarounds documented
- Related feature documentation and examples
- User guides and implementation notes

Research focus only. Use Read tool to examine ai_docs directory. Return documentation context with specific file references and configuration examples to include in the PRP.
```

## Research Synthesis & PRP Generation

Once all agents complete their research, synthesize the findings and generate a comprehensive PRP using the base template structure:

### PRP Template Integration

Using PRPs/templates/prp_base.md as the foundation, integrate the research findings:

#### Critical Context Integration
From the research agents, include:
- **Codebase Patterns**: Specific file paths and code examples from Agent 1
- **Technical Documentation**: URLs and specific sections from Agent 2
- **Testing Strategies**: Validation approaches and patterns from Agent 3
- **Project Documentation**: Relevant ai_docs and configuration from Agent 4

#### Implementation Blueprint Enhancement
- Start with pseudocode informed by existing patterns
- Reference real files and patterns discovered in research
- Include error handling strategies from similar implementations
- List tasks in order of completion based on codebase analysis

#### Context-Rich Validation Gates
```bash
# Syntax/Style (from codebase analysis)
uv run ruff check . --fix
uv run mypy .

# Unit Tests (following existing patterns)
uv run pytest tests/ -v

# Integration Tests (if applicable)
[specific commands found in codebase]
```

## Output

Save as: `PRPs/{feature-name}-parallel.md`

## Success Metrics

Score the PRP on a scale of 1-10 for:
- **Context Richness**: How much relevant context is included
- **Implementation Clarity**: How clear the implementation path is
- **Validation Completeness**: How comprehensive the testing strategy is
- **One-Pass Success Probability**: Confidence level for successful implementation

Target: 8+ on all metrics through parallel research depth

Remember: The goal is one-pass implementation success through comprehensive parallel research and context gathering.
```

---

### 22. create-planning-parallel

**Name**: `create-planning-parallel`  
**Description**: Create planning documents with parallel research  
**Command**:
```
# Create PLANNING PRP (Parallel Research)

Transform rough ideas into comprehensive PRDs using parallel research agents for maximum efficiency and depth.

## Idea: {{idea_description}}

## Phase 1: Parallel Research Discovery

**IMPORTANT**: Execute the following 4 research agents simultaneously using multiple Agent tool calls in a single response to maximize research efficiency.

### Research Agent Coordination

Launch these agents concurrently - do not wait for one to complete before starting the next:

#### Agent 1: Market Intelligence
```
Task: Market Research Analysis
Prompt: Research the market landscape for "{{idea_description}}". Conduct deep analysis of:
- Competitor landscape and positioning
- Market size, growth trends, and opportunities
- Pricing models and revenue strategies
- Existing solutions and their limitations
- Market gaps and unmet needs
- Target audience and user segments

Focus purely on research - do not write any code. Use web search extensively. Return a comprehensive market analysis report with specific data points and insights.
```

#### Agent 2: Technical Feasibility
```
Task: Technical Architecture Research
Prompt: Analyze technical feasibility for "{{idea_description}}". Research and evaluate:
- Recommended technology stacks and frameworks
- System architecture patterns and best practices
- Integration possibilities with existing systems
- Scalability and performance considerations
- Technical challenges and solutions
- Development effort estimation

Focus on research only - no code implementation. Use web search for current best practices. Return technical recommendations with pros/cons analysis.
```

#### Agent 3: User Experience Research
```
Task: UX Pattern Analysis
Prompt: Research user experience patterns for "{{idea_description}}". Investigate:
- User journey mapping and flow examples
- Pain points in existing solutions
- UX best practices and design patterns
- Accessibility standards and requirements
- User interface trends and innovations
- Usability testing insights from similar products

Research only - no design creation. Use web search for UX case studies. Return UX analysis with actionable recommendations.
```

#### Agent 4: Best Practices & Compliance
```
Task: Industry Standards Research
Prompt: Research industry best practices for "{{idea_description}}". Cover:
- Security standards and compliance requirements
- Data privacy and protection regulations
- Performance benchmarks and KPIs
- Quality assurance methodologies
- Risk management practices
- Legal and regulatory considerations

Research focus only. Use web search for compliance guides. Return comprehensive best practices guide with specific standards.
```

## Phase 2: Research Synthesis & Analysis

Once all agents complete their research, synthesize the findings into:

### Market Opportunity Assessment
- Market size and growth potential
- Competitive landscape overview
- Target user segments and personas
- Value proposition differentiation

### Technical Architecture Framework
- Recommended technology stack
- System design approach
- Integration strategy
- Scalability plan

### User Experience Blueprint
- User journey mapping
- Key interaction patterns
- Accessibility requirements
- Design system recommendations

### Implementation Readiness
- Security and compliance checklist
- Risk assessment and mitigation
- Success metrics and KPIs
- Quality gates and validation

## Output

Save the completed PRD as: `PRPs/{sanitized-feature-name}-prd.md`

### Quality Checklist
Before marking complete, verify:
- [ ] All 4 research areas covered comprehensively
- [ ] User validation questions answered
- [ ] Technical architecture clearly defined
- [ ] User flows diagrammed with Mermaid
- [ ] Implementation phases outlined
- [ ] Success metrics defined
- [ ] Security requirements documented
- [ ] Ready for implementation PRP creation

Remember: This command leverages parallel research agents to create comprehensive PRDs 4x faster than sequential research.
```

---

### 23. hackathon-prp-parallel

**Name**: `hackathon-prp-parallel`  
**Description**: Hackathon-style parallel PRP creation  
**Command**:
```
# Hackathon PRP Parallel Workflow - Maximum Speed Edition

Execute a massive parallel workflow that leverages multiple AI agents working simultaneously to deliver a complete solution in record time.

## Overview

This workflow deploys 20+ parallel agents:
- 5 agents for spec generation (different perspectives)
- 5 agents for prompt plan creation
- 5 agents for backend implementation
- 5 agents for frontend implementation
- 2 agents for integration and demo prep

All agents work concurrently and report results for synthesis.

## Step 1: Parallel Spec Generation (5 minutes)

Deploy 5 parallel agents to analyze the challenge from different angles:

```
Use the Task tool to run these 5 research agents in PARALLEL for challenge: {{challenge}}

Task 1 - Technical Architecture Agent:
"Analyze {{challenge}} and create technical architecture spec:
- System design and components
- Technology choices and justification
- API design patterns
- Database schema design
- Performance considerations
- Security architecture
Save to: PRPs/specs/{{challenge|slugify}}-tech-spec.md"

Task 2 - User Experience Agent:
"Analyze {{challenge}} from UX perspective:
- User journeys and flows
- UI component requirements
- Interaction patterns
- Accessibility requirements
- Error handling UX
- Loading and feedback states
Save to: PRPs/specs/{{challenge|slugify}}-ux-spec.md"

Task 3 - Business Logic Agent:
"Define business rules and logic for {{challenge}}:
- Core business rules
- Validation requirements
- Edge cases and exceptions
- Data integrity rules
- Business process flows
- Integration requirements
Save to: PRPs/specs/{{challenge|slugify}}-business-spec.md"

Task 4 - Testing Strategy Agent:
"Create comprehensive testing strategy:
- Test scenarios and cases
- Performance test requirements
- Security test cases
- Integration test approach
- Demo test scenarios
- Coverage targets
Save to: PRPs/specs/{{challenge|slugify}}-test-spec.md"

Task 5 - Demo Impact Agent:
"Analyze for maximum demo impact:
- Key features to highlight
- Wow factors to implement
- Metrics to showcase
- Story narrative
- Backup plans
- Time allocations
Save to: PRPs/specs/{{challenge|slugify}}-demo-spec.md"

Synthesize all specs into: PRPs/specs/{{challenge|slugify}}-unified-spec.md
```

## Execution Monitoring

Create a real-time dashboard showing:

```
## Parallel Execution Status

### Spec Generation (Tasks 1-5)
- [ ] Technical Architecture: [status]
- [ ] User Experience: [status]
- [ ] Business Logic: [status]
- [ ] Testing Strategy: [status]
- [ ] Demo Impact: [status]

### Backend Implementation (Tasks 11-15)
- [ ] Entities: [status]
- [ ] Services: [status]
- [ ] REST API: [status]
- [ ] Security: [status]
- [ ] Integration: [status]

### Frontend Implementation (Tasks 16-20)
- [ ] Components: [status]
- [ ] State Management: [status]
- [ ] Forms: [status]
- [ ] UI Polish: [status]
- [ ] Integration: [status]

### Final Phase (Tasks 21-25)
- [ ] Full Stack Integration: [status]
- [ ] Demo Preparation: [status]
- [ ] Backend QA: [status]
- [ ] Frontend QA: [status]
- [ ] Integration QA: [status]

### Metrics
- Total Agents: 25
- Parallel Execution Groups: 5
- Estimated Time: 40 minutes
- Lines of Code Generated: [count]
- Test Coverage: [percentage]
- Response Time: [ms]
```

## Success Metrics

Showcase the power of parallel execution:
- 25 AI agents working simultaneously
- 40-minute complete implementation
- 80%+ test coverage
- Sub-100ms response times
- Full documentation generated
- Production-ready code

This parallel approach demonstrates the true power of AI-assisted development!
```

---

### 24. hackathon-research

**Name**: `hackathon-research`  
**Description**: Rapid hackathon research with 15 agents  
**Command**:
```
# Hackathon Multi-Option Research

Rapidly evaluate multiple solution approaches for hackathon challenges using massive parallel research (15 concurrent agents).

## Problem/Challenge: {{problem_statement}}

## Phase 1: Problem Analysis & Option Generation

### Problem Breakdown
Analyze the challenge statement for:
- Core requirements and constraints
- Success criteria and evaluation metrics
- Available time and resources
- Technical constraints and preferences
- Target users and use cases

### Solution Approach Generation

Generate 3 distinct solution approaches:

#### Option A: Speed-First Approach
- **Philosophy**: "Ship fast, iterate later"
- **Strategy**: Leverage existing tools, proven patterns, minimal custom code
- **Target**: Working prototype in minimal time
- **Trade-offs**: May sacrifice innovation for speed

#### Option B: Innovation-First Approach  
- **Philosophy**: "Breakthrough solution with novel approach"
- **Strategy**: Cutting-edge tech, unique architecture, creative problem-solving
- **Target**: High-impact, differentiated solution
- **Trade-offs**: Higher risk, potentially longer development time

#### Option C: Balanced Approach
- **Philosophy**: "Solid foundation with strategic innovation"
- **Strategy**: Proven base with selective modern enhancements
- **Target**: Reliable solution with competitive advantages
- **Trade-offs**: Moderate risk, moderate innovation

## Phase 2: Massive Parallel Research (15 Agents)

**CRITICAL**: Execute all 15 research agents simultaneously using multiple Agent tool calls in a single response for maximum efficiency.

### Research Matrix: 5 Agents × 3 Options

#### Speed-First Research Agents (5 agents)
- **Agent A1**: Technical Feasibility (Speed-First)
- **Agent A2**: Speed-to-Market Analysis
- **Agent A3**: Market Research (Speed-First)
- **Agent A4**: Design Research (Speed-First)
- **Agent A5**: User Research (Speed-First)

#### Innovation-First Research Agents (5 agents)
- **Agent B1**: Technical Feasibility (Innovation-First)
- **Agent B2**: Innovation Development Timeline
- **Agent B3**: Market Research (Innovation-First)
- **Agent B4**: Design Research (Innovation-First)
- **Agent B5**: User Research (Innovation-First)

#### Balanced Research Agents (5 agents)
- **Agent C1**: Technical Feasibility (Balanced)
- **Agent C2**: Balanced Development Strategy
- **Agent C3**: Market Research (Balanced)
- **Agent C4**: Design Research (Balanced)
- **Agent C5**: User Research (Balanced)

## Phase 3: File Validation & Synthesis

### Create Final Recommendations File

After all option synthesis files are complete, create the comprehensive final analysis:

Create file: `PRPs/research/final-recommendations-analysis.md`
```markdown
# Hackathon Research Final Recommendations

## Executive Summary
**Winner**: [Winning option name]
**Key Rationale**: [2-3 sentence summary of why this option won]
**Implementation Confidence**: [High/Medium/Low]

## Option Comparison Matrix
| Criteria | Speed-First | Innovation-First | Balanced | Weight |
|----------|------------|------------------|----------|--------|
| Development Speed | [score] | [score] | [score] | 35% |
| Technical Feasibility | [score] | [score] | [score] | 25% |
| Innovation/Impact | [score] | [score] | [score] | 20% |
| Market Positioning | [score] | [score] | [score] | 15% |
| User Fit | [score] | [score] | [score] | 5% |
| **Total Score** | **[X.X]** | **[X.X]** | **[X.X]** | 100% |

## Winner Selection & Rationale

### Primary Recommendation: [Winning Option]
**Score**: [X.X/10]
**Confidence Level**: [High/Medium/Low]

**Why This Option Won**:
1. [Primary reason based on scoring]
2. [Secondary reason based on team/context fit]
3. [Tertiary reason based on risk/opportunity]
```

### Scoring Framework (Hackathon Optimized)

#### Weighted Scoring Criteria
```yaml
Development Speed: 35%      # Critical for hackathon timeline
Technical Feasibility: 25%  # Must be achievable
Innovation/Impact: 20%      # Competitive advantage
Market Positioning: 15%     # Strategic advantage and differentiation
User Fit: 5%               # User need alignment and adoption potential
```

### Execution Success Criteria
- [ ] **19 Total Files Created**: 15 individual agent research + 3 synthesis + 1 final recommendations
- [ ] **Quantitative Decision**: Winner selected based on weighted scoring, not intuition
- [ ] **Implementation Ready**: Detailed roadmap with hour-by-hour timeline and specific tasks
- [ ] **Risk Aware**: Contingency plans and decision checkpoints defined
- [ ] **Team Aligned**: Clear roles, responsibilities, and coordination strategy

Remember: This enhanced system provides granular visibility into each research component while maintaining comprehensive analysis and actionable recommendations.
```

---

### 25. prp-analyze-run

**Name**: `prp-analyze-run`  
**Description**: Analyze PRP execution results  
**Command**:
```
# Analyze PRP Results

## PRP File: {{prp_file}}

Post-execution analysis of a PRP implementation to capture lessons learned, success metrics, and template improvements.

## Analysis Process

1. **Execution Metrics Collection**
   - Measure actual vs estimated token usage
   - Track implementation time and iterations
   - Document test failures and fixes
   - Analyze code quality metrics

2. **Success Pattern Analysis**
   - Identify what worked well
   - Extract reusable patterns
   - Document effective context elements
   - Capture successful validation strategies

3. **Failure Pattern Learning**
   - Document encountered issues
   - Analyze root causes
   - Create prevention strategies
   - Update known gotchas database

4. **Template Improvement Recommendations**
   - Identify context gaps
   - Suggest validation enhancements
   - Recommend documentation updates
   - Propose new anti-patterns

5. **Knowledge Base Updates**
   - Add new failure patterns to database
   - Update success metrics
   - Enhance similar feature detection
   - Improve confidence scoring

## Metrics Collection

```bash
# Collect implementation metrics
echo "Collecting execution metrics..."

# Get git statistics
COMMITS_DURING_IMPL=$(git rev-list --count HEAD --since="2 hours ago")
FILES_CHANGED=$(git diff --name-only HEAD~$COMMITS_DURING_IMPL HEAD | wc -l)
LINES_ADDED=$(git diff --shortstat HEAD~$COMMITS_DURING_IMPL HEAD | grep -o '[0-9]* insertion' | grep -o '[0-9]*' || echo 0)

# Get test results
TEST_RESULTS=$(pytest tests/ --tb=no -q 2>&1 | tail -n 1)
TEST_COUNT=$(echo "$TEST_RESULTS" | grep -o '[0-9]* passed' | grep -o '[0-9]*' || echo 0)

echo "📊 Implementation Metrics:"
echo "- Commits: $COMMITS_DURING_IMPL"
echo "- Files changed: $FILES_CHANGED"
echo "- Lines added: $LINES_ADDED"
echo "- Tests passing: $TEST_COUNT"
```

## Analysis Report Generation

```yaml
📊 PRP Analysis Report
======================

🎯 Implementation Summary:
- PRP File: {{prp_file}}
- Execution Date: [timestamp]
- Overall Success: [SUCCESS/PARTIAL/FAILED]

📈 Metrics:
- Implementation time: [X] minutes
- Tests: [X] passed, [X] failed
- Code quality: [X] issues

🎯 Context Effectiveness:
- Documentation URLs: [X]% referenced
- File references: [X]% used
- Examples: [X]% followed

💡 Recommendations for Future PRPs:
- [High] [Specific improvement suggestion]
- [Medium] [Process enhancement]
- [Low] [Minor optimization]

📚 Knowledge Base Updates:
- New failure patterns: [X]
- Updated success metrics: [X]
- Template improvements: [X]
```

## Continuous Improvement Loop

This analysis system creates a continuous improvement loop:

1. **Execute PRP** → Implement feature
2. **Analyze Results** → Extract patterns and metrics
3. **Update Knowledge Base** → Store learnings
4. **Improve Templates** → Apply learnings to future PRPs
5. **Better Context** → Higher success rates

The system learns from each implementation, making future PRPs more effective and reducing failure rates over time.
```

---

### 26. prp-validate

**Name**: `prp-validate`  
**Description**: Validate PRP before execution  
**Command**:
```
# Validate PRP

## PRP File: {{prp_file}}

Pre-flight validation of a PRP to ensure all context and dependencies are available before execution.

## Validation Process

1. **Parse PRP**
   - Read the specified PRP file
   - Extract all file references, URLs, and dependencies
   - Parse validation checklist items

2. **Context Validation**
   - Check all referenced files exist
   - Validate all URLs are accessible
   - Verify environment dependencies are available
   - Check for required API keys/credentials

3. **Codebase Analysis**
   - Scan for similar patterns mentioned in PRP
   - Validate existing examples are current
   - Check for architectural consistency

4. **Dependency Check**
   - Verify all required libraries are installed
   - Check version compatibility
   - Validate external service connectivity

5. **Risk Assessment**
   - Analyze failure patterns mentioned in PRP
   - Assess complexity and confidence score
   - Identify potential bottlenecks

## Validation Gates

### File References
```bash
# Check all referenced files exist
echo "Validating file references..."
for file in $(grep -o 'file: [^[:space:]]*' "{{prp_file}}" | cut -d' ' -f2); do
    if [ ! -f "$file" ]; then
        echo "❌ Missing file: $file"
        exit 1
    else
        echo "✅ Found: $file"
    fi
done
```

### URL Accessibility
```bash
# Check all referenced URLs are accessible
echo "Validating URL references..."
for url in $(grep -o 'url: [^[:space:]]*' "{{prp_file}}" | cut -d' ' -f2); do
    if curl -s --head "$url" > /dev/null; then
        echo "✅ Accessible: $url"
    else
        echo "⚠️  Cannot access: $url"
    fi
done
```

## Validation Report

```
🔍 PRP Validation Report
========================
📁 Context Validation: [PASS/FAIL]
- Files referenced: X/X found
- URLs accessible: X/X responding
- Examples current: [YES/NO]

🔧 Dependencies: [READY/ISSUES/BLOCKED]
- Python modules: X/X available
- External services: X/X accessible
- API keys: X/X configured

⚠️  Risk Assessment: [LOW/MEDIUM/HIGH]
- Complexity score: X/10
- Failure patterns: X identified
- Mitigation strategies: X documented

📊 Readiness Score: XX/100
🎯 Recommended Actions:
[ ] Install missing dependencies
[ ] Configure missing API keys
[ ] Update stale examples
[ ] Review risk mitigation strategies

Status: [READY_TO_EXECUTE/NEEDS_ATTENTION/BLOCKED]
```

## Integration with Execute Command

The validate command should be automatically called by execute-prp before starting implementation:

```bash
# In execute-prp.md, add this as step 0:
echo "Running pre-execution validation..."
validate-prp "{{prp_file}}"
if [ $? -ne 0 ]; then
    echo "❌ Validation failed. Please fix issues before execution."
    exit 1
fi
```
```

---

### 27. user-story-rapid

**Name**: `user-story-rapid`  
**Description**: Rapid user story analysis and implementation  
**Command**:
```
# Analyze User Story and Create Implementation Plan

User Story: {{user_story}}

## Task: Create detailed implementation plan for separate backend and frontend projects based on the tech stack detailed in the user story

1. **Parse user story**:
   - Extract: As a [user], I want [feature], so that [benefit]
   - List explicit and implicit acceptance criteria
   - Identify non-functional requirements (performance, security, UX)
   - Define success metrics

2. **Plan API contract first** (backend/frontend agreement):
   ```yaml
   Endpoints:
     - GET /api/v1/{resources} - List with pagination
     - GET /api/v1/{resources}/{id} - Get single resource
     - POST /api/v1/{resources} - Create new
     - PUT /api/v1/{resources}/{id} - Update existing
     - DELETE /api/v1/{resources}/{id} - Delete
   
   DTOs:
     Request: {field validations}
     Response: {field types}
     Error: {standard error format}
   ```

3. **Backend implementation plan** (Java project):
   ```
   Package structure:
   com.company.feature/
   ├── controller/
   ├── service/
   ├── repository/
   ├── entity/
   ├── dto/
   ├── exception/
   └── mapper/
   ```
   
   Implementation order:
   1. Entity with JPA annotations
   2. Repository interface
   3. DTOs with validation
   4. Mapper interface
   5. Service with business logic
   6. Controller with OpenAPI
   7. Exception handling
   8. Integration tests

4. **Frontend implementation plan** (React project):
   ```
   src/features/{feature}/
   ├── api/          # API client functions
   ├── components/   # UI components
   ├── hooks/        # Custom hooks
   ├── schemas/      # Zod validation
   ├── types/        # TypeScript types
   ├── __tests__/    # Component tests
   └── index.ts      # Public exports
   ```
   
   Implementation order:
   1. Zod schemas matching backend DTOs
   2. TypeScript types
   3. API client functions
   4. Custom hooks with TanStack Query
   5. UI components
   6. Forms with validation
   7. Error handling
   8. Component tests

5. **Integration plan**:
   - CORS configuration on backend
   - Environment variables for API URL
   - Error response handling
   - Loading states
   - Optimistic updates where applicable

6. **Validation commands**:
   ```bash
   # Backend (in Java project)
   ./gradlew clean build test
   
   # Frontend (in React project)
   npm run type-check && npm run lint && npm run test:coverage
   
   # Integration (manual or e2e)
   - Start backend: ./gradlew bootRun
   - Start frontend: npm run dev
   - Test full user flow
   ```

7. **Risk mitigation**:
   - Start with API contract agreement
   - Use API mocking in frontend if backend delayed
   - Implement health check endpoint
   - Add request/response logging
   - Plan for error scenarios

Save this plan as: `PRPs/implementations/{feature}-plan.md`
```

---

## 🔄 Additional Development Commands

### 28. new-dev-branch

**Name**: `new-dev-branch`  
**Description**: Create new development branch  
**Command**:
```
Lets start working on a new branch from develop

## Instructions

1. Move to develop and ensure you pull latest
2. Create a new branch from develop for {{branch_name}}
3. get ready to start working on the new branch
```

---

### 29. refactor-simple

**Name**: `refactor-simple`  
**Description**: Quick refactoring check for code quality  
**Command**:
```
Quick refactoring check for Python code focusing on:
- Vertical slice boundaries
- Function complexity
- Type safety with Pydantic v2
- Single responsibility

Scan for:
1. Functions > 20 lines that need decomposition
2. long files that need decomposition
3. Missing Pydantic models for I/O
4. Cross-feature imports violating vertical slices
5. Classes with multiple responsibilities
6. Missing type hints

Desired architecture:
- Vertical slice boundaries
- Single responsibility
- Type safety with Pydantic v2 

For each issue found, provide:
- Location
- Why it's a problem
- Specific fix with code example
- Specific place where the fix should be implemented
- Priority (high/medium/low)

Focus on actionable items that can be fixed in <1 hour each.

save a refactor_plan.md in the PRPs/ai_docs folder, ensure you dont overwrite any existing files
```

---

### 30. review-general

**Name**: `review-general`  
**Description**: Comprehensive code review  
**Command**:
```
# Code Review

Please perform a comprehensive code review of the current changes or specified files.

## Review Scope
{{review_scope}}

## Review Process

1. **Understand Changes**
   - If reviewing staged changes: `git diff --staged`
   - If reviewing specific files: Read the specified files
   - If reviewing a PR: `gh pr view {{review_scope}} --json files,additions,deletions`
   - If reviewing a local directory: `git diff {{review_scope}}`
   - If reviewing the entire codebase: `git diff origin/main`

## Review Focus Areas

1. **Code Quality**
   - Type hints on all functions and classes
   - Pydantic v2 models for data validation
   - No print() statements (use logging)
   - Proper error handling
   - Following PEP 8
   - Docstrings following google style python docstrings

2. **Security**
   - Input validation on all endpoints
   - No SQL injection vulnerabilities
   - Passwords properly hashed
   - No hardcoded secrets

3. **Structure**
   - Unit tests are co-located with the code they test in tests/ folders
   - Each feature is self-contained with its own models, service, and tools
   - Shared components are only things used by multiple features

4. **Testing**
   - New code has tests
   - Edge cases covered
   - Mocking external dependencies

5. **Performance**
   - No N+1 queries
   - Efficient algorithms
   - Proper async usage

6. **Documentation**
   - Clear README with setup instructions
   - CLAUDE.md is up to date with any new important utils, dependencies etc for future cluade code instances

## Review Output

Create a concise review report with:

```markdown
# Code Review #[number]

## Summary
[2-3 sentence overview]

## Issues Found

### 🔴 Critical (Must Fix)
- [Issue with file:line and suggested fix]

### 🟡 Important (Should Fix)
- [Issue with file:line and suggested fix]

### 🟢 Minor (Consider)
- [Improvement suggestions]

## Good Practices
- [What was done well]

## Test Coverage
Current: X% | Required: 80%
Missing tests: [list]
Save report to PRPs/code_reviews/review[#].md (check existing files first)
```
```

---

### 31. conflict-resolver-specific

**Name**: `conflict-resolver-specific`  
**Description**: Targeted conflict resolution with strategies  
**Command**:
```
You are an expert at resolving Git merge conflicts. {{resolution_strategy}}

## Resolution strategy based on arguments:

- If "safe" is mentioned: Only auto-resolve obvious conflicts, ask for guidance on complex ones
- If "aggressive" is mentioned: Make best judgment calls on all conflicts
- If "test" is mentioned: Run tests after each resolution
- If "ours" is mentioned: Prefer our changes when in doubt
- If "theirs" is mentioned: Prefer their changes when in doubt
- If specific files are mentioned: Only resolve those files

## Process:

1. Check git status and identify conflicts
2. use the github cli to check the PRs and understand the context
3. Think hard about your findings and plan accordingly
4. Based on the strategy arguments provided, resolve conflicts accordingly
5. For each resolution, document what decision was made and why
6. If "test" was specified, run tests after each file resolution
7. Provide detailed summary of all resolutions

## Special handling:

- package-lock.json / yarn.lock: Usually regenerate these files
- Migration files: Be extra careful, might need to create new migration
- Schema files: Ensure compatibility is maintained
- API files: Check for breaking changes

Start by running git status to see all conflicts.
```

---

### 32. TS-review-general

**Name**: `TS-review-general`  
**Description**: Comprehensive TypeScript/Astro codebase review  
**Command**:
```
# General TypeScript/Astro Codebase Review

Perform a comprehensive review of the entire TypeScript/Astro codebase focusing on architecture, patterns, and best practices.

Review scope: {{review_scope}}

If no specific scope provided, review the entire codebase.

## Review Focus Areas

### 1. **Architecture & Structure**
   - Islands Architecture implementation
   - Component organization (static vs interactive)
   - Content collections structure
   - API routes organization
   - Proper separation of concerns

### 2. **TypeScript Quality**
   - Strict mode compliance across all files
   - Type safety and explicit typing
   - Interface definitions and exports
   - Proper use of Astro's built-in types
   - Generic usage and constraints

### 3. **Astro-Specific Patterns**
   - Hydration directives usage patterns
   - Static-first approach implementation
   - Server islands configuration
   - Content management patterns
   - Framework integration consistency

### 4. **Performance & Optimization**
   - Bundle analysis and optimization
   - Image optimization implementation
   - Code splitting and lazy loading
   - Unnecessary JavaScript elimination
   - Hydration strategy effectiveness

### 5. **Security & Validation**
   - Environment variable management
   - Content Security Policy implementation
   - Input validation patterns
   - API security measures
   - Zod schema consistency

## Review Output

Create a comprehensive review report:

```markdown
# TypeScript/Astro Codebase Review #[number]

## Executive Summary
[High-level overview of codebase health, architecture quality, and key findings]

## Critical Findings

### 🔴 Architecture Issues (Must Fix)
- [Structural problems requiring immediate attention]

### 🟡 Pattern Inconsistencies (Should Fix)
- [Inconsistent implementations]

### 🟢 Optimization Opportunities (Consider)
- [Performance improvements]

## Quality Assessment

### TypeScript Quality: [Grade A-F]
- Type safety compliance
- Interface definitions
- Strict mode adherence

### Astro Patterns: [Grade A-F]
- Hydration strategy implementation
- Static-first approach
- Content management

### Performance Score: [Grade A-F]
- Bundle optimization
- Image optimization
- Hydration efficiency

## Compliance Checklist
- [ ] `astro check` passes project-wide
- [ ] `pnpm run lint` zero warnings
- [ ] `pnpm run build` succeeds
- [ ] `pnpm test` 80%+ coverage
- [ ] All components under size limits
- [ ] No `any` types in codebase
```

Save report to PRPs/code_reviews/general_review_[YYYY-MM-DD].md
```

---

### 33. TS-review-staged-unstaged

**Name**: `TS-review-staged-unstaged`  
**Description**: Review TypeScript changes in staging area  
**Command**:
```
List and review any files in the staging area, both staged and unstaged.
Ensure you look at both new files and modified files.

Check the diff of each file to see what has changed.

Previous review report: {{previous_review}}

May or may not be added, ignore the previous review if not specified.

## Review Focus Areas

1. **TypeScript Code Quality**
   - Strict TypeScript usage with explicit types
   - No `any` types - use `unknown` if type is truly unknown
   - Proper type imports with `import type { }` syntax
   - Component props interfaces defined
   - Astro's built-in types used (HTMLAttributes, ComponentProps)
   - Following TypeScript strict mode compliance

2. **Astro-Specific Patterns**
   - Proper hydration directives usage (client:load, client:visible, client:idle)
   - Static-first approach with selective hydration
   - Astro components for static content, framework components only for interactivity
   - Proper use of Astro.props and component interfaces
   - Content collections with Zod schemas
   - Server islands implementation where appropriate

3. **Performance & Bundle Optimization**
   - No unnecessary client-side JavaScript
   - Appropriate hydration strategy choices
   - Image optimization with Astro's Image component
   - Bundle size considerations
   - No over-hydration of static content

4. **Security & Validation**
   - Input validation with Zod schemas
   - Environment variables properly typed with astro:env
   - Content Security Policy implementation
   - No hardcoded secrets in client-side code
   - API route validation with proper error handling

5. **Code Structure & Architecture**
   - Components under 200 lines (500 line hard limit)
   - Functions under 50 lines with single responsibility
   - Proper separation of concerns
   - Feature-based organization
   - Islands architecture principles followed

## Review Output

Create a concise review report with:

```markdown
# TypeScript/Astro Code Review #[number]

## Summary
[2-3 sentence overview focusing on Astro-specific patterns and TypeScript quality]

## Issues Found

### 🔴 Critical (Must Fix)
- [Issue with file:line and suggested fix - focus on type safety, hydration, security]

### 🟡 Important (Should Fix)
- [Issue with file:line and suggested fix - focus on performance, patterns]

### 🟢 Minor (Consider)
- [Improvement suggestions for optimization, maintainability]

## Good Practices
- [What was done well - highlight proper Astro patterns, TypeScript usage]

## Astro-Specific Findings
- [Hydration strategy assessment]
- [Bundle size impact]
- [Content collection usage]
- [Performance optimizations]

## TypeScript Quality
- [Type safety assessment]
- [Strict mode compliance]
- [Interface definitions]

## Test Coverage
Current: X% | Required: 80%
Missing tests: [list with focus on component and API tests]

## Build Validation
- [ ] `astro check` passes
- [ ] `pnpm run lint` passes
- [ ] `pnpm run build` succeeds
- [ ] `pnpm test` passes with 80%+ coverage
```

Save report to PRPs/code_reviews/review[#].md (check existing files first)
```

---

## 🎉 Complete Collection Summary

You now have **33 comprehensive commands** ready for Warp Drive:

### **Core PRP Workflow** (5 commands):
1. `prp-base-create` - Create comprehensive PRPs
2. `prp-base-execute` - Execute PRPs 
3. `prime-core` - Prime with project context
4. `review-staged-unstaged` - Review changes
5. `parallel-prp-creation` - Create multiple PRP variations

### **Development Tools** (8 commands):
6. `debug` - Debug with RCA analysis
7. `create-pr` - Create structured PRs
8. `smart-commit` - Intelligent commits
9. `onboarding` - Developer onboarding
10. `new-dev-branch` - Create development branch
11. `refactor-simple` - Quick refactoring check
12. `review-general` - Comprehensive code review
13. `conflict-resolver-specific` - Targeted conflict resolution

### **TypeScript Support** (4 commands):
14. `prp-ts-create` - TypeScript PRPs
15. `prp-ts-execute` - Execute TypeScript PRPs
16. `TS-review-general` - Comprehensive TypeScript/Astro review
17. `TS-review-staged-unstaged` - Review TypeScript changes

### **Git Operations** (2 commands):
18. `conflict-resolver-general` - Resolve conflicts
19. `smart-resolver` - Smart conflict resolution

### **Advanced PRP Commands** (6 commands):
20. `prp-planning-create` - Planning with diagrams
21. `api-contract-define` - API contracts
22. `prp-spec-create` - Specification-driven PRPs
23. `prp-spec-execute` - Execute specification PRPs
24. `prp-task-create` - Task-focused PRPs
25. `prp-task-execute` - Execute task PRPs
26. `task-list-init` - Create task lists

### **Rapid Development** (8 commands):
27. `create-base-prp-parallel` - Parallel PRP creation
28. `create-planning-parallel` - Parallel planning
29. `hackathon-prp-parallel` - Hackathon parallel workflow
30. `hackathon-research` - Rapid research with 15 agents
31. `prp-analyze-run` - Analyze PRP results
32. `prp-validate` - Validate PRP before execution
33. `user-story-rapid` - Rapid user story implementation

## Next Steps

1. **Copy each command** from this file into Warp Drive as separate notebooks/prompts
2. **Start with core workflow**: `prime-core` → `prp-base-create` → `prp-base-execute`
3. **Test the system** with a real feature implementation
4. **Expand usage** to advanced commands as needed

**The complete agent-factory methodology is now available in Warp Drive!** 🚀
