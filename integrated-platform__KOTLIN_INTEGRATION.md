# Kotlin Dashboard ↔ Python Analytics Integration

## What is included in this upgrade
- Original Benchart Kotlin/Compose source and parser retained.
- FastAPI service with health, analysis, comparison, anomaly, optional PyTorch status and FEA result endpoints.
- Three.js interactive 3D benchmark surface and sample beam/stress mesh dashboard at `/dashboard/`.
- FEA post-processing accepts exported nodal results; it does **not** solve finite-element equations.
- Optional OpenCV and PyTorch dependencies remain optional because device/OS wheel support varies.

## Start the Python service

From `python-analytics/`:

```bash
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# Linux/macOS/Termux: source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
uvicorn benchart_ai.api:app --host 127.0.0.1 --port 8000
```

Open:
- Dashboard: http://127.0.0.1:8000/dashboard/
- API docs: http://127.0.0.1:8000/docs
- Health: http://127.0.0.1:8000/health

## Kotlin/JS bridge contract

The Kotlin UI should send normalized rows to the local or configured API base URL. Keep the API base URL configurable; do not hardcode localhost in a deployed web app. For a browser-hosted Kotlin/Compose UI, the browser must be able to reach the API origin and the API must allow that UI origin via a narrowly configured CORS policy.

A small Kotlin/JS adapter pattern (place in `src/jsMain/kotlin/analytics/AnalyticsApi.kt`) is:

```kotlin
package analytics

import kotlinx.browser.window
import kotlin.js.Promise
import kotlin.js.json

class AnalyticsApi(private val baseUrl: String) {
    fun health(): Promise<dynamic> =
        window.asDynamic().fetch("$baseUrl/health").then { response ->
            response.json()
        }

    fun analyze(rows: dynamic): Promise<dynamic> {
        val options = json(
            "method" to "POST",
            "headers" to json("Content-Type" to "application/json"),
            "body" to JSON.stringify(json("rows" to rows))
        )
        return window.asDynamic().fetch("$baseUrl/analyze", options).then { response ->
            if (!response.ok as Boolean) {
                throw IllegalStateException("Analytics API request failed")
            }
            response.json()
        }
    }
}
```

This is an integration adapter example, not yet wired into the existing `HomePageUi()` component. Add UI controls to that page and call this adapter from a coroutine/promise bridge after deciding the deployment origin. The original Kotlin build remains unchanged by this scaffold.

## API payload examples

`POST /fea/analyze`:

```json
{
  "yield_strength_mpa": 250,
  "rows": [
    {"node_id": 1, "x": 0, "y": 0, "z": 0, "displacement": 0.1, "von_mises": 35},
    {"node_id": 2, "x": 1, "y": 0, "z": 0.2, "displacement": 0.4, "von_mises": 82}
  ]
}
```

The response contains peak/mean stress, displacement, critical node, coordinate arrays for 3D rendering, and optional factor of safety. Stress is assumed to be MPa.

## Important engineering limitations
- FEA endpoint is a post-processor for exported nodal result tables, not a solver. It does not generate a mesh, apply boundary conditions, solve stiffness equations, or validate a model.
- 3D dashboard starts with illustrative geometry. Replace it with validated solver-exported node/element data before using it for engineering decisions.
- ML predictions and anomaly flags are exploratory; use repeated runs, uncertainty checks and domain validation.
- Do not expose the API to the public internet without authentication, rate limiting, input-size limits, TLS and deployment hardening.
