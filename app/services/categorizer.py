def categorize_transaction(description: str) -> str:
    description = description.lower()

    categories = {
        "Food": [
            "swiggy",
            "zomato",
            "blinkit",
            "restaurant",
            "cafe",
            "food",
            "pizza",
            "burger"
        ],
        "Transport": [
            "uber",
            "ola",
            "rapido",
            "metro",
            "bus",
            "fuel",
            "petrol",
            "diesel"
        ],
        "Shopping": [
            "amazon",
            "meesho",
            "flipkart",
            "myntra",
            "shopping"
        ],
        "Bills": [
            "electricity",
            "water bill",
            "internet",
            "recharge",
            "phone bill"
            "wifi bill"
        ],
        "Entertainment": [
            "netflix",
            "spotify",
            "crunchyroll",
            "movie",
            "cinema",
            "youtube"
        ]
    }

    for category, keywords in categories.items():
        for keyword in keywords:
            if keyword in description:
                return category

    return "Misc / Other"


if __name__ == "__main__":
    print(categorize_transaction("Swiggy order"))
    print(categorize_transaction("Uber ride"))
    print(categorize_transaction("Amazon purchase"))
    print(categorize_transaction("Netflix subscription"))
    print(categorize_transaction("ABC Electronics"))