def get_customer_satisfaction(n):
    if 0 <= n <= 100:
        return 100
    elif 100 < n <= 200:
        return 100 - 0.25 * (n - 100)
    elif 200 < n <= 300:
        return 75 - 0.75 * (n - 200)
    else:
        return 0