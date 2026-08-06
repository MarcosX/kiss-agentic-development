from orders import apply_coupon


def checkout(subtotal, coupon):
    total = apply_coupon(subtotal, coupon)
    if total >= subtotal:
        return {"error": "Invalid coupon code", "total": total}
    return {"success": True, "total": total}
