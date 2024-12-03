# from flask import current_app as app, jsonify
# from flask_security import auth_required, roles_required
# from .models import Professional, db

# @app.get('/')
# def home():
#     return "Hello World!"

# @app.get("/admin")
# @auth_required("token")
# @roles_required("admin")
# def admin():
#     return "Welcome admin"

# @app.get('/activate/prof/<int:prof_id>')
# @auth_required("token")
# @roles_required("admin")
# def activate_professional(prof_id):
#     professional = Professional.query.get(prof_id)
#     if not professional:
#         return jsonify({"message": "Professional not found"}), 404

#     # Check if the user has the "prof" role
#     prof_role = next((role for role in professional.roles if role.name == "prof"), None)
#     if not prof_role:
#         return jsonify({"message": "User is not a professional"}), 400

#     professional.active = True
#     db.session.commit()
#     return jsonify({"message": "Professional activated"})


from flask import current_app as app, jsonify, request, render_template, send_file
from flask_security import auth_required, roles_required
from werkzeug.security import check_password_hash
from flask_restful import marshal, fields
import flask_excel as excel
from celery.result import AsyncResult
from .tasks import create_service_request_csv
from .models import User, db, HouseholdServiceRequest
from .sec import datastore


@app.get('/')
def home():
    return render_template("index.html")


@app.get('/admin')
@auth_required("token")
@roles_required("admin")
def admin():
    return "Hello Admin"


@app.get('/activate/provider/<int:provider_id>')
@auth_required("token")
@roles_required("admin")
def activate_provider(provider_id):
    provider = User.query.get(provider_id)
    if not provider or "provider" not in provider.roles:
        return jsonify({"message": "Provider not found"}), 404

    provider.active = True
    db.session.commit()
    return jsonify({"message": "Provider Activated"})


@app.post('/user-login')
def user_login():
    data = request.get_json()
    email = data.get('email')
    if not email:
        return jsonify({"message": "Email not provided"}), 400

    user = datastore.find_user(email=email)

    if not user:
        return jsonify({"message": "User Not Found"}), 404

    if check_password_hash(user.password, data.get("password")):
        return jsonify({"token": user.get_auth_token(), "email": user.email, "role": user.roles[0].name})
    else:
        return jsonify({"message": "Wrong Password"}), 400


user_fields = {
    "id": fields.Integer,
    "email": fields.String,
    "active": fields.Boolean
}


@app.get('/users')
@auth_required("token")
@roles_required("admin")
def all_users():
    users = User.query.all()
    if len(users) == 0:
        return jsonify({"message": "No User Found"}), 404
    return marshal(users, user_fields)


@app.get('/household-service/<int:id>/approve')
@auth_required("token")
@roles_required("provider")
def approve_service_request(id):
    service_request = HouseholdServiceRequest.query.get(id)
    if not service_request:
        return jsonify({"message": "Service Request Not Found"}), 404
    service_request.is_approved = True
    db.session.commit()
    return jsonify({"message": "Approved"})


@app.get('/download-csv')
def download_csv():
    task = create_service_request_csv.delay()
    return jsonify({"task-id": task.id})


@app.get('/get-csv/<task_id>')
def get_csv(task_id):
    res = AsyncResult(task_id)
    if res.ready():
        filename = res.result
        return send_file(filename, as_attachment=True)
    else:
        return jsonify({"message": "Task Pending"}), 404
