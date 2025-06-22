import pytest
from spdx_license_list import LICENSES

from app.utils.license import get_license_info

@pytest.mark.parametrize("license_id", list(LICENSES.keys()))
def test_get_license_info(license_id: str) -> None:
    """Ensure license info is returned and contains expected fields."""
    info: dict[str, str] = get_license_info(license_id)

    print(f"🔎 {license_id} → {info['name']} — {info['url']}")

    assert info["name"] == license_id
    assert info["url"].startswith("https://spdx.org/licenses/")
    assert info["url"].endswith(f"{license_id}.html")
