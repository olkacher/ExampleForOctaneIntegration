import html
import json
import time
import traceback
from pathlib import Path


def _is_worker(config):
    """Return whether pytest is running inside xdist worker process."""
    return hasattr(config, "workerinput")


def _get_worker_id(config):
    """Return pytest-xdist worker id or master for non-parallel run."""
    if _is_worker(config):
        return config.workerinput["workerid"]

    return "master"


def _worker_result_file(config):
    """Return path to worker-specific Octane result JSON file."""
    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)

    return reports_dir / f"octane-results-{_get_worker_id(config)}.json"


def _get_tid_tag(node):
    """
    Extract TID marker from pytest node.

    Example:
        TID12345REV0.1.0 -> @TID12345REV0.1.0
    """
    for marker in node.iter_markers():
        if marker.name.startswith("TID"):
            return f"@{marker.name}"

    return ""


def pytest_sessionstart(session):
    """Remove old Octane report files before test session starts."""
    if _is_worker(session.config):
        return

    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)

    for file in reports_dir.glob("octane-results-*.json"):
        file.unlink()

    result_file = reports_dir / "octane-result.xml"

    if result_file.exists():
        result_file.unlink()


def pytest_bdd_before_scenario(request, feature, scenario):
    """Initialize Octane scenario metadata before scenario execution."""
    request.node._octane_started = int(time.time() * 1000)
    request.node._octane_steps = []
    request.node._octane_scenario_status = "passed"


def pytest_bdd_before_step(request, feature, scenario, step, step_func):
    """Store step start time before BDD step execution."""
    request.node._octane_step_started = time.time()


def pytest_bdd_after_step(
    request,
    feature,
    scenario,
    step,
    step_func,
    step_func_args,
):
    """Add passed BDD step execution data to Octane scenario metadata."""
    duration_ms = int(
        (time.time() - request.node._octane_step_started) * 1000
    )

    request.node._octane_steps.append(
        {
            "name": step.name,
            "duration": duration_ms,
            "status": "Passed",
        }
    )


def pytest_bdd_step_error(
    request,
    feature,
    scenario,
    step,
    step_func,
    step_func_args,
    exception,
):
    """Add failed BDD step execution data and error details to metadata."""
    duration_ms = int(
        (time.time() - request.node._octane_step_started) * 1000
    )

    request.node._octane_scenario_status = "failed"

    request.node._octane_steps.append(
        {
            "name": step.name,
            "duration": duration_ms,
            "status": "Failed",
            "error": {
                "type": type(exception).__name__,
                "message": str(exception),
                "trace": "".join(
                    traceback.format_exception(
                        type(exception),
                        exception,
                        exception.__traceback__,
                    )
                ),
            },
        }
    )


def pytest_bdd_after_scenario(request, feature, scenario):
    """Write scenario execution result to worker-specific JSON file."""
    feature_path = str(getattr(feature, "filename", ""))
    feature_text = ""

    if feature_path and Path(feature_path).exists():
        feature_text = Path(feature_path).read_text(encoding="utf-8")

    steps = request.node._octane_steps
    duration_ms = sum(step["duration"] for step in steps)

    result = {
        "feature_name": feature.name,
        "feature_path": feature_path,
        "feature_started": request.node._octane_started,
        "feature_tag": _get_tid_tag(request.node),
        "feature_text": feature_text,
        "scenario_name": scenario.name,
        "scenario_status": request.node._octane_scenario_status,
        "status": request.node._octane_scenario_status,
        "duration": duration_ms,
        "steps": steps,
    }

    worker_file = _worker_result_file(request.config)

    if worker_file.exists():
        existing = json.loads(worker_file.read_text(encoding="utf-8"))
    else:
        existing = []

    existing.append(result)

    worker_file.write_text(
        json.dumps(existing, indent=2),
        encoding="utf-8",
    )


def pytest_sessionfinish(session, exitstatus):
    """
    Generate final Octane XML report after test execution.

    Workflow:
    1. Read all worker JSON result files.
    2. Merge feature/scenario results.
    3. Generate Octane-compatible XML structure.
    4. Write final XML report to disk.
    """
    if _is_worker(session.config):
        return

    reports_dir = Path("reports")
    result_file = reports_dir / "octane-result.xml"

    results = []

    for file in reports_dir.glob("octane-results-*.json"):
        results.extend(json.loads(file.read_text(encoding="utf-8")))

    features = {}

    for result in results:
        feature_path = result["feature_path"]

        if feature_path not in features:
            features[feature_path] = {
                "feature_name": result["feature_name"],
                "feature_path": result["feature_path"],
                "feature_started": result["feature_started"],
                "feature_tag": result["feature_tag"],
                "feature_text": result["feature_text"],
                "duration": 0,
                "status": "passed",
                "scenarios": [],
            }

        features[feature_path]["duration"] += result["duration"]

        if result["status"] == "failed":
            features[feature_path]["status"] = "failed"

        features[feature_path]["scenarios"].append(
            {
                "scenario_name": result["scenario_name"],
                "scenario_status": result["scenario_status"],
                "steps": result["steps"],
            }
        )

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        "<test_result>",
        "  <test_runs>",
    ]

    for feature in features.values():
        run_status = (
            "Passed"
            if feature["status"] == "passed"
            else "Failed"
        )

        lines.append(
            f'    <gherkin_test_run duration="{feature["duration"]}" '
            f'name="{html.escape(feature["feature_name"], quote=True)}" '
            f'status="{run_status}">'
        )

        lines.append(
            f'      <feature '
            f'name="{html.escape(feature["feature_name"], quote=True)}" '
            f'path="{html.escape(feature["feature_path"], quote=True)}" '
            f'started="{feature["feature_started"]}" '
            f'tag="{html.escape(feature["feature_tag"], quote=True)}">'
        )

        lines.append("        <file><![CDATA[")
        lines.append(feature["feature_text"])
        lines.append("]]></file>")

        lines.append("        <scenarios>")

        for scenario in feature["scenarios"]:
            scenario_status = (
                "Passed"
                if scenario["scenario_status"] == "passed"
                else "Failed"
            )

            lines.append(
                f'          <scenario '
                f'name="{html.escape(scenario["scenario_name"], quote=True)}" '
                f'status="{scenario_status}">'
            )

            lines.append("            <steps>")

            for step in scenario["steps"]:
                step_name = html.escape(step["name"], quote=True)
                step_status = step["status"]

                if step.get("error"):
                    error_type = html.escape(
                        step["error"].get("type", "Error"),
                        quote=True,
                    )
                    error_message = html.escape(
                        step["error"].get("message", ""),
                        quote=True,
                    )

                    lines.append(
                        f'              <step duration="{step["duration"]}" '
                        f'name="{step_name}" '
                        f'status="{step_status}">'
                    )
                    lines.append(
                        f'                <error '
                        f'type="{error_type}" '
                        f'message="{error_message}" />'
                    )
                    lines.append("              </step>")
                else:
                    lines.append(
                        f'              <step duration="{step["duration"]}" '
                        f'name="{step_name}" '
                        f'status="{step_status}" />'
                    )

            lines.append("            </steps>")
            lines.append("          </scenario>")

        lines.append("        </scenarios>")
        lines.append("      </feature>")
        lines.append("    </gherkin_test_run>")

    lines.extend(
        [
            "  </test_runs>",
            "</test_result>",
        ]
    )

    result_file.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )