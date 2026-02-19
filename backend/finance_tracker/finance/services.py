from .mongo import transactions_col
import datetime


def create_transaction(user_id, data):

    VALID_TYPES = ["income", "expense", "initial_balance"]

    tx_type = data.get("type")

    if tx_type not in VALID_TYPES:
        raise ValueError("Invalid transaction type")

    amount = data.get("amount")

    if amount is None:
        raise ValueError("Amount required")

    amount = abs(float(amount))

    tx = {
        "user_id": user_id,
        "type": tx_type,
        "title": data.get("title"),
        "category": data.get("category"),
        "amount": amount,
        "created_at": datetime.datetime.utcnow()
    }

    result = transactions_col.insert_one(tx)
    tx["_id"] = result.inserted_id

    return tx



def get_user_transactions(user_id):

    return list(
        transactions_col.find(
            {"user_id": user_id}
        ).sort("created_at", -1)
    )

def set_initial_balance(user_id, balance):
    tx = {
        "user_id": user_id,
        "type": "initial_balance",
        "amount": abs(float(balance)),
        "category": "initial",
        "title": "Starting Balance",
        "created_at": datetime.datetime.utcnow()
    }

    result = transactions_col.insert_one(tx)
    tx["_id"] = result.inserted_id

    return tx

def calculate_balance(user_id):
    
    now = datetime.datetime.utcnow()
    start_of_month = datetime.datetime(month=now.month, year=now.year, day=1)
    

    pipeline = [
        {"$match": {"user_id": user_id}},
        {
            "$group": {
                "_id": None,
                "starting_balance": {
                    "$sum": {
                        "$cond": [
                            {"$eq": ["$type", "initial_balance"]}, 
                            "$amount", 0
                        ]
                    }
                },

                "income": {
                    "$sum": {
                        "$cond": [
                            {"$eq": ["$type", "income"]},
                            "$amount", 0
                        ]
                    }
                },

                "monthly_income": {
                    "$sum": {
                        "$cond": [
                            {
                                "$and": [
                                    {"$eq": ["$type", "income"]},
                                    {"$gte": ["$created_at", start_of_month]}
                                ]
                            },
                            "$amount", 0
                        ]
                    }
                },

                "expenses": {
                    "$sum": {
                        "$cond": [
                            {"$eq": ["$type", "expense"]}, "$amount", 0
                        ]
                    }
                },

                "monthly_expenses": {
                    "$sum": {
                        "$cond": [
                            {
                                "$and": [
                                    {"$eq": ["$type", "expense"]},
                                    {"$gte": ["$created_at", start_of_month]}
                                ]
                            },
                            "$amount", 0
                        ]
                    }
                },
            }
        }
    ]

    result = list(transactions_col.aggregate(pipeline))

    print("DEBUG RESULT:", result)
   


    if not result:
        return {
            "balance": 0,
            "monthly_expenses": 0,
            "savings_rate": 0
        }

    data = result[0]
    
    starting_balance = data.get("starting_balance", 0)
    income = data.get("income", 0)
    monthly_income = data.get("monthly_income", 0)
    expenses = data.get("expenses", 0)
    monthly_expenses = data.get("monthly_expenses", 0)

    balance = starting_balance + income - expenses
    
    monthly_savings = monthly_income - monthly_expenses

    savings_rate = int((monthly_savings / monthly_income) * 100) if monthly_income > 0 else 0

    return {
        "balance": balance,
        "monthly_expenses": monthly_expenses,
        "savings_rate": savings_rate
    }