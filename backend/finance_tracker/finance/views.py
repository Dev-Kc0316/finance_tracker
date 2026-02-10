from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .services import (
    create_transaction,
    get_user_transactions,
    calculate_balance
)
from .serializers import serialize_list, serialize_doc


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_transaction(request):

    data = request.data.copy()
    data["type"] = "expense"

    if not data.get("title") or not data.get("amount"):
        return Response({"error": "Title and amount required"}, status=400)

    tx = create_transaction(request.user.id, data)

    summary = calculate_balance(request.user.id)

    return Response({
        "success": True,
        "transaction": serialize_doc(tx),
        "summary": summary
    })


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def dashboard(request):

    transactions = get_user_transactions(request.user.id)

    summary = calculate_balance(request.user.id)

    return Response({
        "success": True,
        "user": {
            
            "username": request.user.username
        },
        "transactions": serialize_list(transactions),
        "summary": summary
    })
