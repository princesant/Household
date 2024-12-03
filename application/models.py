# from flask_sqlalchemy import SQLAlchemy
# from flask_security import UserMixin, RoleMixin


# db = SQLAlchemy()

# # Many-to-Many relationship for Users and Roles
# association_table = db.Table(
#     'roles_users',
#     db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
#     db.Column('role_id', db.Integer, db.ForeignKey('role.id'), primary_key=True)
# )

# class User(db.Model, UserMixin):
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     email = db.Column(db.String(255), unique=True, nullable=False)
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     password = db.Column(db.String(255), nullable=False)
#     active = db.Column(db.Boolean(), default=True)
#     roles = db.relationship('Role', secondary=association_table, backref=db.backref('users', lazy=True))
#     fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)

# class Role(db.Model, RoleMixin):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(80), unique=True, nullable=False)
#     description = db.Column(db.String(255), nullable=True)

# class Customer(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)
#     name = db.Column(db.String(80), unique=True, nullable=False)
#     description = db.Column(db.String(255), nullable=True)

# class Service(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(80), unique=True, nullable=False)
#     price = db.Column(db.Integer, nullable=False)
#     time_required = db.Column(db.Integer, nullable=False)  # Duration in minutes
#     description = db.Column(db.String(255), nullable=True)

# class Professional(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)
#     name = db.Column(db.String(80), unique=True, nullable=False)
#     description = db.Column(db.String(255), nullable=True)
#     service_type = db.Column(db.String(80), nullable=False)
#     experience = db.Column(db.Integer, nullable=False)

# class ServiceRequest(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)
#     customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
#     professional_id = db.Column(db.Integer, db.ForeignKey('professional.id'), nullable=True)
#     date_of_request = db.Column(db.Date, nullable=False)
#     date_of_completion = db.Column(db.Date, nullable=True)
#     service_status = db.Column(db.Boolean(), default=False)
#     remark = db.Column(db.String(255), nullable=True)
#     location = db.Column(db.String(255), nullable=True)  # Added for geographical context


from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin

db = SQLAlchemy()

# Many-to-Many relationship for Users and Roles
association_table = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'), primary_key=True)
)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean(), default=True)
    roles = db.relationship('Role', secondary=association_table, backref=db.backref('users', lazy=True))
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=True)

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)
    name = db.Column(db.String(80), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(15), unique=True, nullable=False)

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    price = db.Column(db.Integer, nullable=False)  # Price in local currency
    time_required = db.Column(db.Integer, nullable=False)  # Duration in minutes
    description = db.Column(db.String(255), nullable=True)

class Professional(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)
    name = db.Column(db.String(80), nullable=False)
    specialization = db.Column(db.String(80), nullable=False)  # Type of service they provide
    experience = db.Column(db.Integer, nullable=False)  # Years of experience
    contact_number = db.Column(db.String(15), unique=True, nullable=False)

class ServiceRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    professional_id = db.Column(db.Integer, db.ForeignKey('professional.id'), nullable=True)
    date_of_request = db.Column(db.Date, nullable=False)
    date_of_completion = db.Column(db.Date, nullable=True)
    service_status = db.Column(db.String(20), default='Pending')  # e.g., Pending, In Progress, Completed
    remarks = db.Column(db.String(255), nullable=True)
    location = db.Column(db.String(255), nullable=True)  # Optional: To specify the service location

