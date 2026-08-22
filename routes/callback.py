from flask import (
    Blueprint,
    request,
    jsonify
)

from models import (
    db,
    Donation
)


# =====================================
# Callback Blueprint
# =====================================

callback_bp = Blueprint(
    "callback",
    __name__
)


# =====================================
# M-Pesa Callback
# =====================================

@callback_bp.route(
    "/callback",
    methods=["POST"]
)
def callback():

    data = request.get_json(
        force=True
    )

    print("\n========== M-PESA CALLBACK ==========")
    print(data)
    print("====================================\n")

    try:

        stk_callback = (
            data
            ["Body"]
            ["stkCallback"]
        )

        checkout_request_id = (
            stk_callback
            ["CheckoutRequestID"]
        )

        result_code = (
            stk_callback
            ["ResultCode"]
        )

        result_description = (
            stk_callback
            ["ResultDesc"]
        )

        print(
            "CheckoutRequestID:",
            checkout_request_id
        )

        # =====================================
        # Find Donation
        # =====================================

        donation = Donation.query.filter_by(
            checkout_request_id=checkout_request_id
        ).first()

        print(
            "Donation found:",
            donation
        )

        if donation is None:

            print(
                "No donation found for callback."
            )

            return jsonify({
                "ResultCode": 0,
                "ResultDesc": "Accepted"
            })

        # =====================================
        # Save Result
        # =====================================

        donation.result_code = result_code

        donation.result_description = (
            result_description
        )

        # =====================================
        # Successful Payment
        # =====================================

        if result_code == 0:

            donation.status = "Received"

            callback_metadata = (
                stk_callback
                .get("CallbackMetadata", {})
                .get("Item", [])
            )

            metadata = {}

            for item in callback_metadata:

                name = item.get("Name")

                value = item.get("Value")

                if name:

                    metadata[name] = value

            # =====================================
            # M-Pesa Receipt
            # =====================================

            donation.mpesa_receipt_number = (
                metadata.get(
                    "MpesaReceiptNumber"
                )
            )

            # =====================================
            # Transaction Date
            # =====================================

            transaction_date = (
                metadata.get(
                    "TransactionDate"
                )
            )

            if transaction_date:

                donation.transaction_date = (
                    str(transaction_date)
                )

            print(
                "Payment successful."
            )

            print(
                "Receipt:",
                donation.mpesa_receipt_number
            )

        # =====================================
        # Failed / Cancelled Payment
        # =====================================

        else:

            donation.status = "Failed"

            print(
                "Payment failed:"
            )

            print(
                result_description
            )

        # =====================================
        # Save
        # =====================================

        db.session.commit()

        print(
            "Donation updated successfully."
        )

    except Exception as e:

        db.session.rollback()

        print(
            "\n========== CALLBACK ERROR =========="
        )

        import traceback

        traceback.print_exc()

        print(
            "====================================\n"
        )

    # =====================================
    # Safaricom Response
    # =====================================

    return jsonify({
        "ResultCode": 0,
        "ResultDesc": "Accepted"
    })