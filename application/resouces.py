from flask_restful import Resource, Api, reqparse

api = Api(prefix='/api')

# parser = reqparse.RequestParser()
# parser.add_argument('topic', type=int, help='Topic should be ')
# parser.add_argument('Description', type=int, help='Description should be string')
# parser.add_argument('', type=int, help='Rate to charge for this resource')


# class ServiceRequest(Resource):
#     def get(self):
#         return {"message": "Hello from api"}
    
#     def post(self):
#         pass


# api.add_resource(ServiceRequest, '/servic_request')


# from flask_restful import Resource, reqparse, Api
# from application.models import db, User, Role, Customer, Service, Professional, ServiceRequest

# # Parsers for incoming data
# user_parser = reqparse.RequestParser()
# user_parser.add_argument('username', type=str, required=True, help='Username is required')
# user_parser.add_argument('password', type=str, required=True, help='Password is required')

# role_parser = reqparse.RequestParser()
# role_parser.add_argument('name', type=str, required=True, help='Role name is required')
# role_parser.add_argument('description', type=str)

# customer_parser = reqparse.RequestParser()
# customer_parser.add_argument('user_id', type=int, required=True, help='User ID is required')
# customer_parser.add_argument('name', type=str, required=True, help='Name is required')
# customer_parser.add_argument('description', type=str)

# service_parser = reqparse.RequestParser()
# service_parser.add_argument('name', type=str, required=True, help='Service name is required')
# service_parser.add_argument('price', type=int, required=True, help='Price is required')
# service_parser.add_argument('time_required', type=int, required=True, help='Time required is required')
# service_parser.add_argument('description', type=str)

# # Resource classes
# class UserResource(Resource):
#     def get(self, user_id):
#         user = User.query.get(user_id)
#         if not user:
#             return {'message': 'User not found'}, 404
#         return {
#             'id': user.id,
#             'username': user.username,
#             'active': user.active,
#             'roles': [role.name for role in user.roles]
#         }

#     def post(self):
#         args = user_parser.parse_args()
#         new_user = User(username=args['username'], password=args['password'])
#         db.session.add(new_user)
#         db.session.commit()
#         return {'message': 'User created', 'user_id': new_user.id}, 201

# class RoleResource(Resource):
#     def get(self, role_id):
#         role = Role.query.get(role_id)
#         if not role:
#             return {'message': 'Role not found'}, 404
#         return {
#             'id': role.id,
#             'name': role.name,
#             'description': role.description
#         }

#     def post(self):
#         args = role_parser.parse_args()
#         new_role = Role(name=args['name'], description=args['description'])
#         db.session.add(new_role)
#         db.session.commit()
#         return {'message': 'Role created', 'role_id': new_role.id}, 201

# class CustomerResource(Resource):
#     def get(self, customer_id):
#         customer = Customer.query.get(customer_id)
#         if not customer:
#             return {'message': 'Customer not found'}, 404
#         return {
#             'id': customer.id,
#             'user_id': customer.user_id,
#             'name': customer.name,
#             'description': customer.description
#         }

#     def post(self):
#         args = customer_parser.parse_args()
#         new_customer = Customer(user_id=args['user_id'], name=args['name'], description=args['description'])
#         db.session.add(new_customer)
#         db.session.commit()
#         return {'message': 'Customer created', 'customer_id': new_customer.id}, 201

# class ServiceResource(Resource):
#     def get(self, service_id):
#         service = Service.query.get(service_id)
#         if not service:
#             return {'message': 'Service not found'}, 404
#         return {
#             'id': service.id,
#             'name': service.name,
#             'price': service.price,
#             'time_required': service.time_required,
#             'description': service.description
#         }

#     def post(self):
#         args = service_parser.parse_args()
#         new_service = Service(
#             name=args['name'],
#             price=args['price'],
#             time_required=args['time_required'],
#             description=args['description']
#         )
#         db.session.add(new_service)
#         db.session.commit()
#         return {'message': 'Service created', 'service_id': new_service.id}, 201

# # Add more resources for Professional and ServiceRequest as needed.


from flask_restful import Resource, Api, reqparse, fields, marshal
from flask_security import auth_required, roles_required, current_user
from flask import jsonify
from sqlalchemy import or_
from .models import ServiceRequest, Service, Customer, Professional, db
from .instances import cache

api = Api(prefix='/api')

# Request parser for ServiceRequest
parser = reqparse.RequestParser()
parser.add_argument('service_id', type=int, required=True, help='Service ID is required and should be an integer')
parser.add_argument('location', type=str, required=True, help='Location is required and should be a string')
parser.add_argument('remarks', type=str, required=False, help='Remarks should be a string')

class ServiceInfo(fields.Raw):
    def format(self, service):
        return {
            'name': service.name,
            'price': service.price,
            'time_required': service.time_required,
            'description': service.description
        }

class ProfessionalInfo(fields.Raw):
    def format(self, professional):
        return {
            'name': professional.name,
            'specialization': professional.specialization,
            'experience': professional.experience,
            'contact_number': professional.contact_number
        }

service_request_fields = {
    'id': fields.Integer,
    'service': ServiceInfo(attribute='service'),
    'customer_id': fields.Integer,
    'professional': ProfessionalInfo(attribute='professional'),
    'date_of_request': fields.DateTime,
    'date_of_completion': fields.DateTime,
    'service_status': fields.String,
    'remarks': fields.String,
    'location': fields.String
}

class HouseholdService(Resource):
    @auth_required("token")
    @cache.cached(timeout=50)
    def get(self):
        # If the user is a professional, show only their assigned requests.
        if "professional" in current_user.roles:
            service_requests = ServiceRequest.query.filter_by(professional_id=current_user.id).all()
        else:
            # Customers see their own requests; Admin sees all requests.
            service_requests = ServiceRequest.query.filter(
                or_(ServiceRequest.customer_id == current_user.id, "admin" in current_user.roles)).all()
        
        if len(service_requests) > 0:
            return marshal(service_requests, service_request_fields)
        else:
            return {"message": "No Service Requests Found"}, 404

    @auth_required("token")
    @roles_required("customer")
    def post(self):
        args = parser.parse_args()

        # Check if the service exists
        service = Service.query.get(args.get('service_id'))
        if not service:
            return {"message": "Service not found"}, 404

        # Create a new service request
        service_request = ServiceRequest(
            service_id=args.get("service_id"),
            customer_id=current_user.id,
            location=args.get("location"),
            remarks=args.get("remarks"),
            date_of_request=db.func.current_date()
        )

        db.session.add(service_request)
        db.session.commit()
        return {"message": "Service Request Created Successfully"}

api.add_resource(HouseholdService, '/service_request')