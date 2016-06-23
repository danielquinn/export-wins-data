from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string


def generate_officer_email(win):
    body = render_to_string("wins/email/officer-thanks.email", {
        "win": win,
        "feedback_address": settings.FEEDBACK_ADDRESS
    })

    return {
        'subject': "Thank you for submitting a new Export Win.",
        'body': body,
        'from': settings.SENDING_ADDRESS,
        'to': win.target_addresses,
    }


def send_intermediate_officer_email(win):
    """ Send mail to officer notifying them that customer will be sent
    email at some point, when manual process gets around to it.

    """

    email_dict = generate_officer_email(win)
    email_dict['body'] = render_to_string("wins/email/officer-thanks-intermediate.email", {
        "win": win,
        "feedback_address": settings.FEEDBACK_ADDRESS
    })

    send_mail(
        email_dict['subject'],
        email_dict['body'],
        email_dict['from'],
        email_dict['to'],
    )


def send_officer_email(win):
    """ Send mail to officer notifying them customer has been sent link to
    customer response form

    This is not currently used, instead is generated by manual process

    """

    email_dict = generate_officer_email(win)
    send_mail(
        email_dict['subject'],
        email_dict['body'],
        email_dict['from'],
        email_dict['to'],
    )


def generate_customer_email(url, win):

    body = render_to_string("wins/email/customer-notification.email", {
        "win": win,
        "url": url
    })

    return {
        'subject': "Congratulations from {} on your export business success".format(
                        win.lead_officer_name
                    ),
        'body': body,
        'from': settings.SENDING_ADDRESS,
        'to': (win.customer_email_address,),
    }


def send_customer_email(request, win):
    """ Send mail to customer asking them to confirm a win

    Not currently used, instead manual process

    """
    email_dict = generate_customer_email(request.POST.get("url"), win)
    send_mail(
        email_dict['subject'],
        email_dict['body'],
        email_dict['from'],
        email_dict['to'],
    )


def send_officer_notification_of_customer_response(customer_response):
    """ Email win officer(s) to let them know customer has responded """

    subject = "Customer response to Export Win"
    body = render_to_string(
        "wins/email/officer-confirmation.email",
        {
            "customer_response": customer_response,
            "feedback_address": settings.FEEDBACK_ADDRESS,
        },
    )
    send_mail(
        subject,
        body,
        settings.SENDING_ADDRESS,
        customer_response.win.target_addresses,
    )
