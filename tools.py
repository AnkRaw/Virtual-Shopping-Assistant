import random

# E-Commerce Search Aggregator
def search_products(query, color=None, size=None, max_price=None):
    """Simulate searching products on multiple e-commerce platforms."""
    products = [
        {"name": "Floral Skirt", "price": 35, "color": "red", "size": "S", "stock": True},
        {"name": "Casual Denim Jacket", "price": 80, "color": "blue", "size": "M", "stock": True},
        {"name": "White Sneakers", "price": 65, "color": "white", "size": "8", "stock": False},
        {"name": "Leather Jacket", "price": 140, "color": "black", "size": "L", "stock": True},
        {"name": "Running Shoes", "price": 120, "color": "gray", "size": "10", "stock": True},
        {"name": "Graphic T-Shirt", "price": 25, "color": "yellow", "size": "M", "stock": False},
        {"name": "Formal Trousers", "price": 50, "color": "navy", "size": "32", "stock": True},
        {"name": "Sunglasses", "price": 90, "color": "black", "size": "One Size", "stock": True},
        {"name": "Backpack", "price": 60, "color": "green", "size": "Medium", "stock": False},
        {"name": "Winter Coat", "price": 110, "color": "gray", "size": "XL", "stock": True}
    ]
    # Filter based on user criteria
    results = [
        p for p in products if
        (not color or p["color"].lower() == color.lower()) and
        (not size or p["size"].lower() == size.lower()) and
        (not max_price or p["price"] <= max_price)
    ]
    return results

# Shipping Time Estimator
def estimate_shipping(location, delivery_deadline):
    """Estimate shipping cost and feasibility based on location and deadline."""
    shipping_options = {
        "standard": {"cost": 5, "days": 5},
        "express": {"cost": 15, "days": 2},
        "overnight": {"cost": 25, "days": 1}
    }
    # Choose the fastest available option
    for method, details in shipping_options.items():
        if details["days"] <= delivery_deadline:
            return {"method": method, "cost": details["cost"], "days": details["days"]}
    return {"error": "Delivery not possible within the requested deadline."}

# Discount Checker
def apply_discount(base_price, promo_code):
    """Check if a discount code is valid and apply it."""
    valid_codes = {"SAVE10": 0.1, "FASHION20": 0.2, "FREESHIP": 0.0, "WELCOME15": 0.15}
    discount = valid_codes.get(promo_code, 0)
    final_price = base_price * (1 - discount)
    return {"original_price": base_price, "discount_applied": discount, "final_price": final_price}

# Competitor Price Comparison
def compare_prices(product_name):
    """Simulate price comparison across multiple stores."""
    competitors = {
    "Casual Denim Jacket": {"SiteA": 80, "SiteB": 75, "SiteC": 85, "SiteD": 78},
    "White Sneakers": {"SiteA": 70, "SiteB": 65, "SiteC": 68, "SiteD": 72},
    "Leather Jacket": {"SiteA": 145, "SiteB": 140, "SiteC": 135, "SiteD": 138},
    "Running Shoes": {"SiteA": 125, "SiteB": 118, "SiteC": 122, "SiteD": 119}
    }
    return competitors.get(product_name, {"error": "Product not found in competitor stores."})

# Return Policy Checker
def get_return_policy(store_name):
    """Retrieve return policy for a given e-commerce store."""
    policies = {
        "SiteA": "Returns accepted within 30 days. Free return shipping.",
        "SiteB": "Returns accepted within 14 days. Buyer pays return shipping.",
        "SiteC": "No returns on discounted items.",
        "SiteD": "Returns allowed within 21 days. Store credit only.",
        "SiteE": "Exchanges allowed within 15 days. No cash refunds."
    }
    return policies.get(store_name, "Return policy not available.")
