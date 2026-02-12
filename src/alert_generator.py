def format_monthly_alert(row) -> str:
    """
    Convert a flagged monthly row into a human-readable alert message.
    """

    user = row["user_id"]
    month = row["year_month"]
    amount = row["amount"]
    baseline = row["hist_mean"]
    pct_change = row["pct_change"]*100

    direction = "increase" if pct_change > 0 else "decrease"

    multiple = amount / baseline if baseline != 0 else 0

    message = (
        f"\n Monthly Spending Alert\n"
        f"User: {user}\n"
        f"Month: {month}\n"
        f"You spent ₹{amount:,.2f} this month.\n"
        f"Your usual monthly average is ₹{baseline:,.2f}.\n"
        f"This is a {abs(pct_change):.1f}% {direction} "
        f"({multiple:.2f}× your typical spending).\n"
    )



    return message
