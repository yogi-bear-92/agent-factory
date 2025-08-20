claude
\*\* Create a comprehensive task list in PRPs/checklist.md for PRP $ARGIMENTS

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
