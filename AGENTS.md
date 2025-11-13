# Project summary and developer preferences

Project: com-kevincojean-llama-server-to-openai-adapter

Root files:
- main.py — FastAPI app with POST /infill (currently returns 501 Not Implemented)
- pyproject.toml — project metadata (Python >=3.12)
- README.md
- tests/test_infill.py — pytest that asserts /infill returns 501

What the code does now
- Exposes a FastAPI app with a single endpoint POST /infill.
- Request model InfillRequest accepts: input_prefix, input_suffix, input_extra (list of {filename,text}), prompt, and allows extra fields (to accept /completion options).
- Endpoint controller body intentionally unimplemented and returns HTTP 501.
- Tests use fastapi.testclient.TestClient and pytest to assert behavior.

Development & run instructions
- Run tests: pytest -q
- Run server for manual testing: uvicorn main:app

Coding preferences and conventions observed
- Use FastAPI for HTTP API surface.
- Use pydantic v2 patterns: prefer model_config = ConfigDict(...) over class Config to avoid deprecation warnings.
- Pydantic models should allow extra fields for flexibility (extra="allow").
- Use HTTPException(status_code=501) for unimplemented endpoints.
- Keep controller functions minimal when service layer is not yet implemented; raise 501 to indicate TODO.
- Tests live under tests/ and use TestClient; if import issues arise during tests, add project root to sys.path or convert the project to a package.
- Prefer concise, explicit tests that assert status codes and response bodies.
- Prefer tests to instantiate real dependencies (avoid monkeypatch/mocking); use lightweight real implementations for services so tests exercise integration points while remaining fast.

Notes for future work
- Implement the infill service (streaming response) and update tests accordingly.
- Consider turning the project into a package (e.g., src/ or package dir) to avoid manipulating sys.path in tests.
- Add type hints and small unit tests for service functions once implemented.

If you want this file expanded or adjusted (different format, more details, or a checklist), tell me what to include.
