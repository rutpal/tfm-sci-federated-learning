import uuid
def get_probe_context(
    device_category=None,
    device_year=None
):

    probe_id = str(uuid.uuid4())

    if device_category is None:

        device_category = input(
            "Device category "
            "(laptop, desktop, smartphone, tablet, server): "
        ).strip().lower()

    if device_year is None:

        device_year = int(
            input(
                "Device purchase year: "
            )
        )

    return {
        "probe_id": probe_id,
        "device_category": device_category,
        "device_year": device_year
    }
