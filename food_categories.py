"""
Food category mappings for consistent categorization.
"""

FOOD_CATEGORIES = {
    "vegetable biryani": "cooked_veg",
    "chicken curry": "cooked_meat",
    "rice": "cooked_starch",
    "bread": "packaged",
    "dairy dessert": "dairy",
}

CATEGORY_PROPERTIES = {
    "cooked_veg": {
        "safe_temp_c": 57,
        "safe_hours": 4,
        "description": "Cooked vegetables and vegetarian curry"
    },
    "cooked_meat": {
        "safe_temp_c": 60,
        "safe_hours": 3,
        "description": "Cooked poultry and meat"
    },
    "cooked_starch": {
        "safe_temp_c": 55,
        "safe_hours": 4,
        "description": "Cooked rice, pasta, bread"
    },
    "packaged": {
        "safe_temp_c": 20,
        "safe_hours": 8,
        "description": "Pre-packaged shelf-stable foods"
    },
    "dairy": {
        "safe_temp_c": 5,
        "safe_hours": 2,
        "description": "Dairy products and frozen desserts"
    },
}
