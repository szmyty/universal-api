from spdx_license_list import LICENSES, License


def get_license_data(license_id: str) -> License | None:
    """Retrieve license data by SPDX identifier."""
    return LICENSES.get(license_id)

def get_spdx_url(license_id: str) -> str:
    """Construct the SPDX URL for a given license ID."""
    return f"https://spdx.org/licenses/{license_id}.html"

def get_license_info(license_id: str) -> dict[str, str]:
    """Retrieve license information by SPDX identifier."""
    license: License | None = get_license_data(license_id)

    if not license:
        raise ValueError(f"Unknown license ID: {license_id}")

    return {
        "name": license_id,
        "url": get_spdx_url(license_id),
    }
