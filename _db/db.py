from init import *

############################################################################################################################
#sqlalchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:pw0rd4gr33nhouse!@192.168.0.25/greenhouse'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
############################################################################################################################

############################################################################################################################
##                   user_1seed
############################################################################################################################
class user_1seed(db.Model) :
   id = db.Column(db.Integer, primary_key = True, unique = True)
   name = db.Column(db.String(100), nullable = False)
   email = db.Column(db.String(100), unique = True, nullable = False)
   username = db.Column(db.String(100), unique = True, nullable = False)
   password = db.Column(db.String(100), nullable = False)
   register_date = db.Column(db.DateTime, default = datetime.utcnow, nullable = False) 
   plant = db.relationship('plant_1seed', backref = 'userplant')
   grow = db.relationship('grow_1seed', backref = 'usergrow')
   grow_page = db.relationship('grow_page_1seed', backref = 'growpage')
   storage = db.relationship('grow_1seed', backref = 'userstorage')

   #how the object is printed (for example in python print):
   def __repr__(self):
      return "user_1seed('{self.password}','{self.email}','{self.name}')"

############################################################################################################################
##                   grow_1seed
############################################################################################################################
class grow_1seed(db.Model) :
   id = db.Column(db.Integer, primary_key = True, unique = True)
   create_date = db.Column(db.DateTime, default = datetime.utcnow, nullable = False) 
   title = db.Column(db.String(45), nullable = False)
   plant_name = db.Column(db.Integer, nullable = False)
   plant_id = db.Column(db.String(45), nullable = False)
   spacing = db.Column(db.Integer, nullable = False)
   growitem_surface = db.Column(db.Float, nullable = False)
   growitem_quantity = db.Column(db.Integer, nullable = False)
   event_alert = db.Column(db.String(45), nullable = False)
   time_planted_greenhouse = db.Column(db.DateTime, nullable = False) 
   time_planted_outdoor = db.Column(db.DateTime, default = datetime.utcnow, nullable = False) 
   perenial = db.Column(db.DateTime, nullable = False) 
   grow_time = db.Column(db.Float, nullable = False)
   grow_group_name = db.Column(db.String(45), nullable = False)
   grow_group_type = db.Column(db.String(45), nullable = False)
   user_id = db.Column(db.Integer, db.ForeignKey('user_1seed.id')) 
   grow_page_id = db.Column(db.Integer, db.ForeignKey('grow_page_1seed.id')) 
   #grow_guild_id = db.Column(db.Integer, db.ForeignKey('grow_page_1seed.id')) 
   #storage_id = db.Column(db.Integer, db.ForeignKey('grow_page_1seed.id')) 

   
   #how the object is printed (for example in python print):
   def __repr__(self):
      return "grow_1seed('{self.title}','{self.plant_name}','{self.description}')"

############################################################################################################################
##                   grow_page_1seed
############################################################################################################################
class grow_page_1seed(db.Model) :
   id = db.Column(db.Integer, primary_key = True, unique = True)
   name = db.Column(db.String(45), nullable = False)
   surface = db.Column(db.Float, nullable = False)
   user_id = db.Column(db.Integer, db.ForeignKey('user_1seed.id')) 

   #backref
   grow = db.relationship('grow_1seed', backref = 'growpage')
   
   #how the object is printed (for example in python print):
   def __repr__(self):
      return "grow_1seed('{self.title}','{self.variety}','{self.description}')"

############################################################################################################################


############################################################################################################################
##                   plant_1seed
############################################################################################################################
class plant_1seed(db.Model) :
   id = db.Column(db.Integer, primary_key = True, unique = True)
   name = db.Column(db.String(45), nullable = False)

   #botanical data:
   latin_name = db.Column(db.String(45), nullable = False)
   family = db.Column(db.String(45), nullable = False)
   sub_family = db.Column(db.String(45), nullable = False)
   tribe = db.Column(db.String(45), nullable = False)
   sub_tribe = db.Column(db.String(45), nullable = False)
   genus = db.Column(db.String(45), nullable = False)
   perenial = db.Column(db.Integer, nullable = False)
   endangered = db.Column(db.Integer, nullable = False)
   link = db.Column(db.String(300), nullable = False)
   Description = db.Column(db.String(45), nullable = False)

   #calculated based on location
   native = db.Column(db.Integer, nullable = False)
   flowering_beggining = db.Column(db.DateTime, nullable = False)
   flowering_time = db.Column(db.Integer, nullable = False)
   fruiting_beggining = db.Column(db.DateTime, nullable = False)
   fruiting_time = db.Column(db.Integer, nullable = False)
   transplant_time = db.Column(db.Integer, nullable = False)

   #growing data
   SeedTempOpt = db.Column(db.Integer, nullable = False)
   SeedTempMin = db.Column(db.Integer, nullable = False)
   SeedTempMax = db.Column(db.Integer, nullable = False)
   PlantTempOpt = db.Column(db.Integer, nullable = False)
   PlantTempMin = db.Column(db.Integer, nullable = False)
   PlantTempMax = db.Column(db.Integer, nullable = False)
   Area_needed = db.Column(db.Integer, nullable = False)
   Spacing = db.Column(db.Integer, nullable = False)
   WaterDemands = db.Column(db.Integer, nullable = False)
   LightDemands = db.Column(db.Integer, nullable = False)
   HumidityDemands = db.Column(db.Integer, nullable = False)
   Hardness = db.Column(db.Integer, nullable = False)
   GrowthDetails = db.Column(db.String(500), nullable = False)
   Pests = db.Column(db.String(45), nullable = False)
   SeedStartDate = db.Column(db.DateTime, default = datetime.utcnow, nullable = False) 
   PlantStartDate = db.Column(db.DateTime, default = datetime.utcnow, nullable = False)
  
   user_id = db.Column(db.Integer, db.ForeignKey('user_1seed.id')) 

   def __repr__(self):
      return "plant_1seed('{self.title}','{self.variety}','{self.description}')"

############################################################################################################################
##                   storage_1seed
############################################################################################################################
class storage_1seed(db.Model) :
   id = db.Column(db.Integer, primary_key = True, unique = True)
   author = db.Column(db.String(100), nullable = False)
   title = db.Column(db.String(255), nullable = False)
   type = db.Column(db.String(100), nullable = False)
   body = db.Column(db.Text, nullable = False)
   quantity = db.Column(db.Integer, nullable = False)
   description = db.Column(db.Text, nullable = False)
   create_date = db.Column(db.DateTime, default = datetime.utcnow, nullable = False)
   user_id = db.Column(db.Integer, db.ForeignKey('user_1seed.id')) 

   def __repr__(self):
      return "storage_1seed('{self.title}','{self.variety}','{self.description}')"

############################################################################################################################
#                 call to create db structure:
#db.create_all()
############################################################################################################################
