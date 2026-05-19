import re

import pytest


@pytest.fixture(autouse=True)
def add_octane_metadata_to_junit(request, record_property):
    """Inject Octane-related metadata into JUnit test report."""

    for marker in request.node.iter_markers():
        marker_name = marker.name

        if marker_name.startswith("TID"):
            full_id = marker_name.replace("TID", "")
            match = re.match(r"(\d+)", full_id)
            short_id = match.group(1) if match else full_id

            record_property("octane.test_id", short_id)
            record_property("octane.full_id", full_id)
            record_property("scenario.name", request.node.name)

            if hasattr(request.node, "fspath"):
                record_property("test.file", str(request.node.fspath))