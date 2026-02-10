from .mongo import transactions_col
import datetime


def create_transaction(user_id, data):

    amount = data.get("amount")

    if amount is None:
        raise ValueError("Amount required")

    tx = {
        "user_id": user_id,
        "type": data.get("type"),
        "title": data.get("title"),
        "category": data.get("category"),
        "amount": float(amount),
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
        "amount": float(balance),
        "category": "initial",
        "title": "Starting Balance",
        "created_at": datetime.datetime.utcnow()
    }

    result = transactions_col.insert_one(tx)
    tx["_id"] = result.inserted_id

    return tx

def calculate_balance(user_id):

    pipeline = [
        {"$match": {"user_id": user_id}},
        {
            "$group": {
                "_id": None,
                "income": {
                    "$sum": {
                        "$cond": [
                            {"$in": ["$type", ["income", "initial_balance"]]}, 
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
                # "deposit": {
                #     "$sum": {
                #         "$cond": [{"$eq": ["$type", "deposit"]}, "$amount", 0]
                #     }
                # }
            }
        }
    ]

    result = list(transactions_col.aggregate(pipeline))

    if not result:
        return {
            "balance": 0,
            "monthly_expenses": 0,
            "savings_rate": 0
        }
    
    income = result[0].get("income", 0)
    expenses = result[0].get("expenses", 0)

    balance = income - expenses

    savings_rate = int((balance / income) * 100) if income > 0 else 0

    return {
        "balance": balance,
        "monthly_expenses": expenses,
        "savings_rate": savings_rate
    }
