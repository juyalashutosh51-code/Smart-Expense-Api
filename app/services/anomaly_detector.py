import statistics

def detect_anomalies(transactions, threshold=2):

    if len(transactions) < 3:
        return[]

    amounts = [
        float(transaction.amount)
        for transaction in transactions
    ]

    mean = statistics.mean(amounts)
    standard_deviation=statistics.stdev(amounts)

    if standard_deviation == 0:
        return[]

    anomalies = []

    for transaction in transactions:

        amount = float(transaction.amount)

        z_score = (amount - mean) / standard_deviation

        if abs(z_score) >= threshold:
            anomalies.append({
                "transaction_id":transaction.id,
                "description":transaction.description,
                "amount": amount,
                "date":transaction.date,
                "z_score": round(z_score,2),
                "reason": "Unusually high expense"
            })

    return anomalies