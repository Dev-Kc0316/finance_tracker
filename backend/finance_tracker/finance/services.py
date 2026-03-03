from .mongo import transactions_col
import datetime
from django.utils.dateparse import parse_date


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



def get_user_transactions(user_id, start_date=None, end_date=None):

    query = {"user_id": user_id}

    if start_date or end_date:
        query["created_at"] = {}

        if start_date:
            start_dt = datetime.datetime.fromisoformat(start_date)
            query["created_at"] ["$gte"] = start_dt

        if end_date:
            end_dt = datetime.datetime.fromisoformat(end_date) + datetime.timedelta(days=1)
            query["created_at"] ["$lt"] = end_dt

    return list(
        transactions_col.find(query).sort("created_at", -1)
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

def calculate_balance(user_id, start_date=None, end_date=None):

    now = datetime.datetime.utcnow()

    if start_date:
        period_start = datetime.datetime.fromisoformat(start_date)
    else:
        period_start = datetime.datetime(now.year, now.month, 1)

    match_stage = {"user_id": user_id}

    if start_date or end_date:
        match_stage["created_at"] = {}

        if start_date:
            match_stage["created_at"]["$gte"] = datetime.datetime.fromisoformat(start_date)

        if end_date:
            end_dt = datetime.datetime.fromisoformat(end_date) + datetime.timedelta(days=1)
            match_stage["created_at"]["$lt"] = end_dt

    pipeline = [
        {"$match": match_stage},
        {
            "$group": {
                "_id": None,


                "starting_balance": {
                    "$sum": {
                        "$cond": [
                            {"$eq": ["$type", "initial_balance"]},
                            "$amount",
                            0
                        ]
                    }
                },

                "income": {
                    "$sum": {
                        "$cond": [
                            {"$eq": ["$type", "income"]},
                            "$amount",
                            0
                        ]
                    }
                },

                "expenses": {
                    "$sum": {
                        "$cond": [
                            {"$eq": ["$type", "expense"]},
                            "$amount",
                            0
                        ]
                    }
                },

                # Period-based totals (month or filter start)
                "period_income": {
                    "$sum": {
                        "$cond": [
                            {
                                "$and": [
                                    {"$eq": ["$type", "income"]},
                                    {"$gte": ["$created_at", period_start]}
                                ]
                            },
                            "$amount",
                            0
                        ]
                    }
                },

                "period_expenses": {
                    "$sum": {
                        "$cond": [
                            {
                                "$and": [
                                    {"$eq": ["$type", "expense"]},
                                    {"$gte": ["$created_at", period_start]}
                                ]
                            },
                            "$amount",
                            0
                        ]
                    }
                },
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

    data = result[0]

    starting_balance = data.get("starting_balance", 0)
    income = data.get("income", 0)
    expenses = data.get("expenses", 0)

    period_income = data.get("period_income", 0)
    period_expenses = data.get("period_expenses", 0)

    balance = starting_balance + income - expenses

    period_savings = period_income - period_expenses

    savings_rate = int((period_savings / period_income) * 100) if period_income > 0 else 0

    return {
        "balance": balance,
        "monthly_expenses": period_expenses,
        "savings_rate": savings_rate
    }