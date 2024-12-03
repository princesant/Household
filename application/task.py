from celery import shared_task
from .models import ServiceRequest, User, Role
import flask_excel as excel
from .mail_service import send_message
from jinja2 import Template


@shared_task(ignore_result=False)
def create_service_request_csv():
    # Query service requests to extract service name, customer, status, and location
    service_requests = ServiceRequest.query.with_entities(
        ServiceRequest.service_id, 
        ServiceRequest.customer_id, 
        ServiceRequest.service_status,
        ServiceRequest.location
    ).all()

    # Convert query result to CSV
    csv_output = excel.make_response_from_query_sets(
        service_requests, ["service_id", "customer_id", "service_status", "location"], "csv")
    filename = "service_requests.csv"

    with open(filename, 'wb') as f:
        f.write(csv_output.data)

    return filename


@shared_task(ignore_result=True)
def daily_reminder(to, subject):
    # Fetch all admin users
    users = User.query.filter(User.roles.any(Role.name == 'admin')).all()

    # Read the reminder email template
    with open('reminder_template.html', 'r') as f:
        template = Template(f.read())

    # Send reminders to all admins
    for user in users:
        send_message(user.email, subject, template.render(email=user.email))

    return "OK"
