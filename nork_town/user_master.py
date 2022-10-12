from nork_town import db
from nork_town.models import User

name = 'admin'
phone_number = '551100000000'
email = 'admin@example.com'
password = '123456'

user = User(name=name, phone_number=phone_number, email=email, password=password)
db.session.add(user)
db.session.commit()