import random

def initiate_payment(user_id, amount, method="upi"):
    # 💳 Mock payment initiation
    payment_id = f"PAY_{random.randint(100000,999999)}"
    status = "success" if random.random() > 0.05 else "failed"
    print(f"\n--- PAYMENT MOCK ---")
    print(f"User ID   : {user_id}")
    print(f"Amount    : ₹{amount}")
    print(f"Method    : {method}")
    print(f"Status    : {status}")
    print(f"Payment ID: {payment_id}")
    print(f"--- END PAYMENT ---\n")
    return {
        "payment_id": payment_id,
        "status": status,
        "method": method,
        "amount": amount
    }
