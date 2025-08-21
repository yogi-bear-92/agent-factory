Agent Operations Quick Reference (For autonomous coding agents)

1. Install & env: uv sync; copy .env.example to .env; run ./scripts/dev-start.sh for services (Redis, Chroma, API).
2. Lint & format: ruff check --fix src tests; ruff format src tests (line length 88; isort via Ruff rule I; ignore E501, B008, C901).
3. Type checking: mypy src --strict (configured: disallow untyped defs/decorators, no implicit optional, warn unused ignores, strict equality).
4. Run all tests: uv run pytest -v; fast fail: pytest -x.
5. Run a single test file: uv run pytest tests/test_models.py -v; single test: uv run pytest tests/test_models.py::test_agent_message_creation -q.
6. Focused pattern: uv run pytest -k "chroma and not redis" --maxfail=1.
7. PRP workflow: uv run PRPs/scripts/prp_runner.py --prp <name> --interactive (headless: --output-format json).
8. Dev server/API health: ./scripts/dev-start.sh then curl -f http://localhost:8000/health (add if missing before relying on it).
9. Imports: standard lib, third-party, internal (src.*) separated by blank lines; let Ruff auto-sort; avoid wildcard imports; use explicit relative only within package.
10. Naming: snake_case functions/vars; PascalCase classes (AgentPRP, ExecutionResult); ALL_CAPS constants; private helpers prefixed _; keep module names short.
11. Types: Prefer explicit annotations everywhere; no Any in signatures; Pydantic models for config & structured messages; use | for unions (py312); return rich result objects (ExecutionResult, AgentResponse) instead of bare tuples.
12. Async: Prefer async/await; never block event loop (use asyncio.to_thread for CPU/file IO); heartbeat loops catch asyncio.CancelledError explicitly.
13. Error handling: Catch specific exceptions; log via structlog/get_logger or logging.getLogger(__name__); include context fields not raw stack unless debugging; never swallow—return ExecutionResult.failure([...]).
14. Logging: Structured (structlog); add contextual keys via log_context(); avoid print(); INFO for lifecycle, DEBUG for fine-grain, ERROR with succinct message.
15. Vector/store & messaging: Use ChromaVectorStore.store_knowledge / query_similar; RedisMessageBus.* for pub/sub; always await store/query.
16. Configuration: All runtime config via pydantic Settings (src/config/settings.py); do not hardcode credentials; add new settings with env_prefix section.
17. Dependency rules: Add libs only in pyproject.toml; keep minimal; prefer stdlib (pathlib, asyncio) first.
18. Git workflow: Small atomic commits after passing lint + mypy + focused tests; write intent-focused messages ("feat(agent): add heartbeat jitter").
19. Test authoring: Use pytest + asyncio_mode=auto; name tests test_*; assert explicit; use fixtures for temp dirs & mocks; isolate side effects.
20. Do not introduce new patterns when existing agent/base abstractions fit; extend BaseAgent; reuse ExecutionResult; keep PRPs information-dense.
