import resend

from flask import current_app


def send_driver_approval_email(
    recipient_email,
    driver_name,
    member_id
):
    """
    Send an approval email to an approved RTFS driver
    using the Resend HTTP API.
    """

    resend_api_key = current_app.config.get("RESEND_API_KEY")
    mail_sender = current_app.config.get("MAIL_DEFAULT_SENDER")
    site_url = current_app.config.get(
        "SITE_URL",
        "http://127.0.0.1:5000"
    )

    # -------------------------------------
    # Check email configuration
    # -------------------------------------

    if not resend_api_key:
        raise ValueError(
            "RESEND_API_KEY is not configured."
        )

    if not mail_sender:
        raise ValueError(
            "MAIL_DEFAULT_SENDER is not configured."
        )

    # -------------------------------------
    # Configure Resend
    # -------------------------------------

    resend.api_key = resend_api_key

    # -------------------------------------
    # Email content
    # -------------------------------------

    subject = "Your RTFS Membership Has Been Approved"

    text_body = f"""
Dear {driver_name},

Congratulations!

Your membership application with the
Resilient Truckers Foundation has been approved.

Your official RTFS Registration Number is:

{member_id}

You can use this registration number to verify
your membership with the Resilient Truckers Foundation.

Verification:
{site_url}/verify

Welcome to the Resilient Truckers Foundation.

Resilience in Every Mile.
"""

    html_body = f"""
<html>
<body>

<h2>Membership Approved</h2>

<p>Dear <strong>{driver_name}</strong>,</p>

<p>
Congratulations! Your membership application with the
<strong>Resilient Truckers Foundation</strong>
has been approved.
</p>

<p>
Your official RTFS Registration Number is:
</p>

<h2>{member_id}</h2>

<p>
You can use this registration number to verify
your membership with the Resilient Truckers Foundation.
</p>

<p>
<a href="{site_url}/verify">
Verify Your RTFS Membership
</a>
</p>

<p>
Welcome to the Resilient Truckers Foundation.
</p>

<p>
<strong>Resilience in Every Mile.</strong>
</p>

</body>
</html>
"""

    # -------------------------------------
    # Send through Resend HTTPS API
    # -------------------------------------

    response = resend.Emails.send({
        "from": mail_sender,
        "to": [recipient_email],
        "subject": subject,
        "text": text_body,
        "html": html_body,
    })

    return response