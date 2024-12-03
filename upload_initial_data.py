# from main import app, datastore
# from application.models import db, Role
# from flask_security import hash_password
# from werkzeug.security import generate_password_hash

# with app.app_context():
#     db.create_all()
#     datastore.find_or_create_role(name="admin", description="User is an Admin")
#     datastore.find_or_create_role(name="cust", description="User is an Customer")
#     datastore.find_or_create_role(name="prof", description="User is an Professional")
#     db.session.commit()
#     if not datastore.find_user(email="admin@email.com"):
#         datastore.create_user(email="admin@email.com", password=generate_password_hash("admin"), roles=["admin"])
        
#     if not datastore.find_user(email="cust1@email.com"):
#         datastore.create_user(email="cust1@email.com", password=generate_password_hash("cust1"), roles=["cust"], active=False)
    
#     if not datastore.find_user(email="prof1@email.com"):
#         datastore.create_user(email="prof1@email.com", password=generate_password_hash("prof1"), roles=["prof"])
#     db.session.commit()





#     # admin = Role(id='admin', name='Admin', description='Admin is Smart')
#     # db.session.add(admin)
#     # cust = Role(id = 'cust', name = 'Customer', description = 'Customer is King')
#     # db.session.add(cust)
#     # prof = Role(id='prof', name='professional', desciption='Professionals are rare')
#     # db.session.add(prof)
#     # try:
#     #     db.session.commit()
#     # except:
#     #     pass


from main import app
from application.sec import datastore
from application.models import db, Role
from flask_security import hash_password
from werkzeug.security import generate_password_hash

with app.app_context():
    # Create all tables
    db.create_all()

    # Define roles specific to the Household Service App
    datastore.find_or_create_role(name="admin", description="User is an Admin")
    datastore.find_or_create_role(name="prof", description="User is a Professional")
    datastore.find_or_create_role(name="cust", description="User is a Customer")
    db.session.commit()

    # Create default admin user
    if not datastore.find_user(email="admin@serviceapp.com"):
        datastore.create_user(
            email="admin@serviceapp.com",
            password=generate_password_hash("admin123"),
            roles=["admin"]
        )

    # Create a default professional user
    if not datastore.find_user(email="prof1@serviceapp.com"):
        datastore.create_user(
            email="prof1@serviceapp.com",
            password=generate_password_hash("prof123"),
            roles=["prof"],
            active=False  # Initially inactive
        )

    # Create default customer users
    if not datastore.find_user(email="cust1@serviceapp.com"):
        datastore.create_user(
            email="cust1@serviceapp.com",
            password=generate_password_hash("cust123"),
            roles=["cust"]
        )
    if not datastore.find_user(email="cust2@serviceapp.com"):
        datastore.create_user(
            email="cust2@serviceapp.com",
            password=generate_password_hash("cust123"),
            roles=["cust"]
        )

    # Commit the changes to the database
    db.session.commit()
