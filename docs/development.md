# Development Notes

Use this page as a working checklist when extending the project.

## Recommended near-term improvements

- Add argument count guards for all CLI branches.
- Consolidate duplicate print word parser branch.
- Introduce tests for file parsing and memory serialization.
- Normalize path handling in Python tools.

## Documentation workflow

- Edit pages under docs/.
- Update navigation in mkdocs.yml when adding new pages.
- Preview docs with mkdocs serve.
- Build static docs with mkdocs build.

## Suggested release checklist

- Build C++ solution in Visual Studio.
- Smoke-test CLI load/start/save flow.
- Run mkdocs serve and verify key pages.
- Run mkdocs build and confirm no warnings.
- Commit docs and code updates together when behavior changes.

## Suggested doc expansion areas

- Learning algorithm details in Planner.cpp.
- Formal memory file schema examples.
- Contribution guide and coding standards.

!!! tip "Keep docs close to code"
    When adding a new command, update CLI Reference and Data Files in the same change.
