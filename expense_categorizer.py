def categorize_expense(description):
    desc = description.lower()
    if 'food' in desc or 'grocer' in desc:
        return 'Food'
    elif 'electricity' in desc or 'water' in desc:
        return 'Utilities'
    elif 'uber' in desc or 'bus' in desc:
        return 'Transport'
    elif 'course' in desc or 'book' in desc:
        return 'Education'
    else:
        return 'Other'
