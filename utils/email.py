import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import current_app


def send_driver_approval_email(
    recipient_email,
    driver_name,
    member_id
):
    """
    Send an approval email to an approved RTFS driver.
    """

    mail_server = current_app.config.get(
        "MAIL_SERVER"
    )

    mail_port = current_app.config.get(
        "MAIL_PORT"
    )

    mail_username = current_app.config.get(
        "MAIL_USERNAME"
    )

    mail_password = current_app.config.get(
        "MAIL_PASSWORD"
    )

    mail_sender = current_app.config.get(
        "MAIL_DEFAULT_SENDER"
    )

    # -------------------------------------
    # Check email configuration
    # -------------------------------------

    if not mail_username or not mail_password:

        raise ValueError(
            "Email service is not configured. "
            "Set MAIL_USERNAME and MAIL_PASSWORD."
        )

    # -------------------------------------
    # Create email
    # -------------------------------------

    message = MIMEMultipart("alternative")

    message["Subject"] = (
        "Your RTFS Membership Has Been Approved"
    )

    message["From"] = mail_sender

    message["To"] = recipient_email

    # -------------------------------------
    # Plain-text version
    # -------------------------------------

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
{current_app.config.get("SITE_URL", "")}/verify

Welcome to the Resilient Truckers Foundation.

Resilience in Every Mile.
"""

    # -------------------------------------
    # HTML version
    # -------------------------------------

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
<a href="{current_app.config.get("SITE_URL", "")}/verify">
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

    message.attach(
        MIMEText(
            text_body,
            "plain"
        )
    )

    message.attach(
        MIMEText(
            html_body,
            "html"
        )
    )

    # -------------------------------------
    # Send email
    # -------------------------------------

    with smtplib.SMTP(
        mail_server,
        mail_port
    ) as server:

        server.starttls()

        server.login(
            mail_username,
            mail_password
        )

        server.sendmail(
            mail_sender,
            recipient_email,
            message.as_string()
        )