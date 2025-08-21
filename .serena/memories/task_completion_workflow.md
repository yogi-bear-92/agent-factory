# Task Completion Workflow

## When a Task is Completed

### 1. Validation Gates (Must Run All Levels)

#### Level 1: Syntax & Style
```bash
# Python code validation
ruff check --fix src/
mypy src/
ruff format src/

# Expected: Zero errors before proceeding
```

#### Level 2: Unit Tests
```bash
# Run unit tests
uv run pytest tests/ -v

# Run with coverage (if available)
uv run pytest tests/ --cov=src --cov-report=term-missing

# Expected: All tests pass
```

#### Level 3: Integration Testing
```bash
# Test PRP execution
uv run PRPs/scripts/prp_runner.py --prp test-feature --output-format json

# Test Claude commands
claude /review-staged-unstaged

# Expected: Integration tests pass
```

#### Level 4: System Validation
```bash
# For multi-agent systems
docker-compose up -d
curl http://localhost:8000/health

# For PRP systems
claude /prp-base-execute PRPs/test-prp.md

# Expected: System functions correctly
```

### 2. Code Review Process

```bash
# Review changes using PRP methodology
claude /review-staged-unstaged

# Check for:
# - Following PRP structure and conventions
# - Proper validation gates included
# - All context documented
# - Anti-patterns avoided
```

### 3. Documentation Updates

#### Required Documentation
- Update relevant PRP templates if patterns change
- Add new commands to `.claude/commands/` if created
- Update `CLAUDE.md` if project conventions change
- Add examples to `claude_md_files/` for new frameworks

#### Documentation Checklist
- [ ] PRP includes all required context
- [ ] Implementation blueprint is complete
- [ ] Validation commands are executable
- [ ] Examples are provided for complex patterns

### 4. Git Operations

```bash
# Smart commit with meaningful message
claude /smart-commit "feature: implement agent coordination system"

# Or manual commit following conventions
git add .
git commit -m "feat: add multi-agent coordination with Redis pub/sub

- Implement BaseAgent class with message handling
- Add RedisMessageBus for agent communication  
- Create task coordination workflows
- Include validation gates for all components"
```

### 5. Final Validation Checklist

#### Technical Validation
- [ ] All 4 validation levels completed successfully
- [ ] No linting errors: `ruff check src/`
- [ ] No type errors: `mypy src/`
- [ ] All tests pass: `uv run pytest tests/ -v`

#### PRP Validation  
- [ ] PRP structure follows template requirements
- [ ] All context sections are comprehensive
- [ ] Implementation blueprint is detailed
- [ ] Validation gates are executable
- [ ] Success criteria are measurable

#### Integration Validation
- [ ] Compatible with existing agent-factory framework
- [ ] MCP servers (serena, archon, browsermcp) integration works
- [ ] Claude Code commands function correctly
- [ ] No breaking changes to existing workflows

### 6. Deployment (If Applicable)

```bash
# For multi-agent systems
docker-compose build
docker-compose up -d

# Verify deployment
curl http://localhost:8000/health
curl http://localhost:8000/agents/status

# For PRP updates
# No deployment needed - templates are ready for use
```

### 7. Learning and Improvement

#### Success Pattern Recording
- Document what worked well in PRP context sections
- Update templates with new successful patterns
- Add to `PRPs/ai_docs/` for future AI context

#### Failure Analysis
- Document what didn't work and why
- Update anti-patterns sections
- Improve validation gates to catch similar issues

## Progressive Success Approach

1. **Start Simple**: Implement basic functionality first
2. **Validate Early**: Run validation gates at each step
3. **Enhance Iteratively**: Add complexity only after validation passes
4. **Document Everything**: Capture context and patterns for future use

This workflow ensures one-pass implementation success through comprehensive validation and continuous learning.