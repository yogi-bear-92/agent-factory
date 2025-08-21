# Validate PRP

## PRP File: $ARGUMENTS

Pre-flight validation of a PRP to ensure all context and dependencies are available before execution.

## Validation Process

This command runs a comprehensive validation script that checks:

1. **PRP Structure** - Ensures all required sections are present (Goal, Why, What, Context, Implementation, Validation)
2. **File References** - Validates referenced files exist or will be created by the PRP
3. **URL Accessibility** - Checks that all referenced URLs are reachable
4. **Python Dependencies** - Verifies critical packages are available (chromadb, langchain, fastapi, etc.)
5. **Command Availability** - Ensures validation commands can be executed (python, uv, git, docker, etc.)

## Usage

```bash
# Validate a specific PRP using the wrapper script
PRPs/scripts/validate PRPs/my-feature.md

# Or run the Python script directly for detailed output
python PRPs/scripts/validate_prp.py PRPs/my-feature.md
```

## Exit Codes

- **0**: PRP is ready for execution
- **1**: PRP needs attention (warnings present)
- **2**: PRP is blocked (critical failures)

## Validation Categories

### ✅ PASS - Ready to proceed
### ⚠️ WARN - Review recommended but not blocking  
### ❌ FAIL - Must be resolved before execution

## Integration with Execute Command

This validation should be run before any PRP execution:

```bash
# Recommended workflow
./PRPs/scripts/validate PRPs/my-feature.md
if [ $? -eq 0 ]; then
    # PRP is ready - proceed with execution
    uv run PRPs/scripts/prp_runner.py --prp my-feature --interactive
else
    echo "Fix validation issues first"
fi
```

## Validation Report

Generates a comprehensive report including:

- **Context Completeness Score** (0-100%)
- **Dependency Readiness** (Ready/Issues/Blocked)
- **Risk Assessment** (Low/Medium/High)
- **Readiness Score** (0-100%)
- **Specific Recommendations** for each issue found

## Auto-Fix Suggestions

The validator provides actionable suggestions for common issues:

- Missing Python packages: `uv add package-name`
- Missing commands: Installation instructions
- File reference issues: Create missing files or update references
- URL accessibility: Check network connectivity or update URLs

This validation ensures PRPs have all necessary context for successful autonomous implementation.
