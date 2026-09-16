def validate_order(data):
    if not data.get("customer_id"):
        raise ValueError("missing customer_id")
    if not data.get("items"):
        raise ValueError("missing items")
    if not isinstance(data["items"], list):
        raise ValueError("items must be a list")
    if len(data["items"]) == 0:
        raise ValueError("items cannot be empty")