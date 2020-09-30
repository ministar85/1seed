from init import db

from init import user_1seed

#prepare insert
user_insert = user_1seed(username = 'username', name = 'name', email = 'email', password = 'password')

#stage insert
db.session.add(user_insert)

#commit to db
db.session.commit()

#query all:
user_1seed.query.all()

#query 1st
user_1seed.query.first()

#filter
user_1seed.query.filter_by(username='admin').all()

user_1seed.query.filter_by(username='admin').first()

#save query in variable
user = user_1seed.query.filter_by(username='admin').first()

