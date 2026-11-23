# Benchart AI Integrated Platform — v3 Upgrade

## Delivered in this source package
1. Preserved original Benchart Kotlin Multiplatform / Compose project.
2. Python FastAPI analytics companion retained and expanded.
3. 3D dashboard using Three.js: interactive benchmark surface and illustrative beam mesh.
4. FEA nodal-result post-processing endpoint with stress/displacement summaries and optional factor of safety.
5. Optional PyTorch availability detection endpoint.
6. Kotlin/JS API adapter example and integration instructions.
7. OpenAPI docs at `/docs`, dashboard at `/dashboard/`.

## Current integration state
The Python service and dashboard are runnable together. The Kotlin adapter is supplied as an example, but it is not yet connected to the original HomePageUi. This avoids pretending a full Kotlin UI integration has been compiled and tested.

## Next engineering milestones
- Add actual Compose navigation tabs and API configuration UI.
- Add Three.js mesh upload (VTK/OBJ/STL) and element connectivity rendering.
- Add validated solver adapters (CalculiX / Code_Aster / OpenFOAM result import).
- Add material database, load cases, boundary-condition metadata and unit validation.
- Add PyTorch model training pipelines with datasets, checkpointing and GPU selection.
- Add OpenCV upload pipeline and inference/model evaluation.
- Add authentication, CORS allowlist, job queue, persistence and deployment packaging.

## v4 module expansion
- Added module registry and 10 selectable Three.js 3D concept scenes.
- Added robotics two-link forward kinematics and Pandas dataset profiling endpoints.
- Expanded browser dashboard with module-specific tools and clear capability boundaries.
- Next engineering milestones: connect a real CAD kernel (e.g. CadQuery), a solver workflow (e.g. CalculiX/OpenFOAM), implement validated SIMP optimization, wire Kotlin Compose screens to the API, and add model training/data pipelines.

## v5 delivered
- Added Beam Lab analytical calculator and shear/moment data output.
- Added tabular RandomForest training/evaluation endpoint for regression/classification.
- Added 2D CFD exported velocity-field post-processing endpoint.
- Added corresponding dashboard tools and regression smoke tests.
- Kept explicit boundaries for full CAD/CAE/FEA/CFD solvers and SIMP optimization.
