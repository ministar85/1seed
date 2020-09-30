from init import *
from _db.db import *

plants = Blueprint("plants", __name__, static_folder="static", template_folder="templates")

#PlantForm Form Class (WTForm)
class PlantForm(Form):
    #botanical data:
    name = StringField('name', [validators.Length(min=1, max=200)])
    latin_name = StringField('latin_name', [validators.Length(min=1, max=200)])
    family = StringField('family', [validators.Length(min=1, max=200)])
    sub_family = StringField('sub_family')
    tribe = StringField('tribe')
    sub_tribe = StringField('sub_tribe')
    genus = StringField ('genus')
    perenial = IntegerField('perenial', [validators.DataRequired()])
    endangered = IntegerField('endangered', [validators.DataRequired()])
    link = StringField ('link')
    Description = StringField ('Description')
    #calculated based on location
    native = IntegerField('native', [validators.DataRequired()])
    flowering_beggining = DateField('flowering_beggining', format='%Y-%m-%d')
    flowering_time = IntegerField('flowering_time', [validators.DataRequired("Field has to be an integer")])
    fruiting_beggining = DateField('fruiting_beggining', format='%Y-%m-%d')
    fruiting_time = IntegerField('fruiting_time', [validators.DataRequired("Field has to be an integer")])
    transplant_time = DateField('transplant_time', format='%Y-%m-%d')   
    #growing data
    SeedTempOpt = IntegerField('SeedTempOpt')
    SeedTempMin = IntegerField('SeedTempMin')
    SeedTempMax = IntegerField('SeedTempMax')
    PlantTempOpt = IntegerField('PlantTempOpt')
    PlantTempMin = IntegerField('PlantTempMin')
    PlantTempMax = IntegerField('PlantTempMax')
    Area_needed = IntegerField('Area_needed', [validators.DataRequired("Field has to be an integer")])
    Spacing = IntegerField('Spacing', [validators.DataRequired("Field has to be an integer")])
    WaterDemands = IntegerField('WaterDemands', [validators.NumberRange(min=1, max=10, message="range from 1 to 10")])
    LightDemands = IntegerField('LightDemands', [validators.NumberRange(min=1, max=10, message="range from 1 to 10")])
    HumidityDemands = IntegerField('HumidityDemands', [validators.NumberRange(min=1, max=10, message="range from 1 to 10")])
    Hardness = IntegerField('Hardness', [validators.NumberRange(min=1, max=10, message="range from 1 to 10")])
    GrowthDetails = StringField('GrowthDetails')
    Pests = StringField('Pests')
    SeedStartDate = DateField('SeedStartDate', format='%Y-%m-%d')
    PlantStartDate = DateField('PlantStartDate', format='%Y-%m-%d')


@plants.route('/')
@is_logged_in
def home():
    #Get user from session
    getuser = user_1seed.query.filter_by(username=session['username']).first()
    getuserid= getuser.id

    #Get plant Items
    #plantitems = plant_1seed.query.filter_by(user_id=session['username']).all()
    plantitems = plant_1seed.query.filter_by(user_id=getuserid).all()

    if plantitems:
        return render_template('plants.html',plantitems=plantitems)
    else:
        msg = 'No Articles Found'
        return render_template('plants.html', msg=msg)

#Add Plant Item
@plants.route('/add_Plant_item', methods=['GET','POST'])
@is_logged_in
def add_Plant_item():
    form = PlantForm(request.form)

    if request.method == 'POST' and form.validate():
    #if request.method == 'POST':
        #botanical data:
        name = form.name.data
        latin_name = form.latin_name.data
        family = form.family.data
        sub_family = form.sub_family.data
        tribe = form.tribe.data
        sub_tribe = form.sub_tribe.data
        genus = form.genus.data
        perenial = form.perenial.data
        endangered = form.endangered.data
        link = form.link.data
        Description = form.Description.data
        #calculated based on location
        native = form.native.data
        flowering_beggining = form.flowering_beggining.data
        flowering_time = form.flowering_time.data
        fruiting_beggining = form.fruiting_beggining.data
        fruiting_time = form.fruiting_time.data
        transplant_time = form.transplant_time.data
		#growing data
        SeedTempOpt = form.SeedTempOpt.data
        SeedTempMin = form.SeedTempMin.data
        SeedTempMax = form.SeedTempMax.data
        PlantTempOpt = form.PlantTempOpt.data
        PlantTempMin = form.PlantTempMin.data
        PlantTempMax = form.PlantTempMax.data
        Area_needed = form.Area_needed.data
        Spacing = form.Spacing.data
        WaterDemands = form.WaterDemands.data
        LightDemands = form.LightDemands.data
        HumidityDemands = form.HumidityDemands.data
        Hardness = form.Hardness.data
        GrowthDetails = form.GrowthDetails.data
        Pests = form.Pests.data
        SeedStartDate = form.SeedStartDate.data
        PlantStartDate = form.PlantStartDate.data

        #Get user from session
        getuser = user_1seed.query.filter_by(username=session['username']).first()
        getuserid= getuser.id

        plant_insert = plant_1seed(name = name,
        #botanical data:
		latin_name  = latin_name,
		family  = family,
		sub_family = sub_family,
		tribe = tribe,
		sub_tribe = sub_tribe, 
        genus = genus,
		perenial = perenial,
		endangered = endangered,
		link = link,
		Description = Description,
        #calculated based on location
		native = native, 
        flowering_beggining = flowering_beggining,
		flowering_time = flowering_time,
		fruiting_beggining = fruiting_beggining,
		fruiting_time = fruiting_time,
		transplant_time = transplant_time,
		#growing data
		SeedTempOpt = SeedTempOpt, 
		SeedTempMin = SeedTempMin, 
        SeedTempMax = SeedTempMax,
		PlantTempOpt = PlantTempOpt,
		PlantTempMin = PlantTempMin,
		PlantTempMax = PlantTempMax,
		Area_needed = Area_needed,
		Spacing = Spacing, 
        WaterDemands = WaterDemands,
		LightDemands = LightDemands,
		HumidityDemands = HumidityDemands,
		Hardness = Hardness,
        GrowthDetails = GrowthDetails,
		Pests = Pests,
		SeedStartDate = SeedStartDate,
		PlantStartDate = PlantStartDate,
		user_id = getuserid)

        db.session.add(plant_insert)
        db.session.commit()

        flash('Plant item created', 'success')

        return redirect(url_for('plants.home'))
    return render_template('add_Plant_item.html', form=form)

#Edit plant Item
@plants.route('/edit_plant_item/<string:id>', methods=['GET','POST'])
@is_logged_in
def edit_plant_item(id):
    #get plant items
    plantitem = plant_1seed.query.filter_by(id=id).first()
    # Get form
    form = PlantForm(request.form)

    # Populate plant item fields
    form.name.data = plantitem.name
    #botanical data:
    form.latin_name.data = plantitem.latin_name
    form.family.data = plantitem.family
    form.sub_family.data = plantitem.sub_family
    form.tribe.data = plantitem.tribe
    form.sub_tribe.data = plantitem.sub_tribe
    form.genus.data = plantitem.genus
    form.perenial.data = plantitem.perenial
    form.endangered.data = plantitem.endangered
    form.link.data = plantitem.link
    form.Description.data = plantitem.Description
    #calculated based on location
    form.native.data = plantitem.native
    form.flowering_beggining.data = plantitem.flowering_beggining
    form.flowering_time.data = plantitem.flowering_time
    form.fruiting_beggining.data = plantitem.fruiting_beggining
    form.fruiting_time.data = plantitem.fruiting_time
    form.transplant_time.data = plantitem.transplant_time
    #growing data
    form.SeedTempOpt.data = plantitem.SeedTempOpt
    form.SeedTempMin.data = plantitem.SeedTempMin
    form.SeedTempMax.data = plantitem.SeedTempMax
    form.PlantTempOpt.data = plantitem.PlantTempOpt
    form.PlantTempMin.data = plantitem.PlantTempMin
    form.PlantTempMax.data = plantitem.PlantTempMax
    form.Area_needed.data = plantitem.Area_needed
    form.Spacing.data = plantitem.Spacing
    form.WaterDemands.data = plantitem.WaterDemands
    form.LightDemands.data = plantitem.LightDemands
    form.HumidityDemands.data = plantitem.HumidityDemands
    form.Hardness.data = plantitem.Hardness
    form.GrowthDetails.data = plantitem.GrowthDetails
    form.Pests.data = plantitem.Pests
    form.SeedStartDate.data = plantitem.SeedStartDate
    form.PlantStartDate.data = plantitem.PlantStartDate

    #if request.method == 'POST' and form.validate():
    if request.method == 'POST':
        name = request.form['name']
        #botanical data:
        latin_name = request.form['latin_name']
        family = request.form['family']
        sub_family = request.form['sub_family']
        tribe = request.form['tribe']
        sub_tribe = request.form['sub_tribe']
        genus = request.form['genus']
        perenial = request.form['perenial']
        endangered = request.form['endangered']
        link = request.form['link']
        Description = request.form['Description']
        #calculated based on location
        native = request.form['native']
        flowering_beggining = request.form['flowering_beggining']
        flowering_time = request.form['flowering_time']
        fruiting_beggining = request.form['fruiting_beggining']
        fruiting_time = request.form['fruiting_time']
        transplant_time = request.form['transplant_time']
        #growing data
        SeedTempOpt = request.form['SeedTempOpt']
        SeedTempMin = request.form['SeedTempMin']
        SeedTempMax = request.form['SeedTempMax']
        PlantTempOpt = request.form['PlantTempOpt']
        PlantTempMin = request.form['PlantTempMin']
        PlantTempMax = request.form['PlantTempMax']
        Area_needed = request.form['Area_needed']
        Spacing = request.form['Spacing']
        WaterDemands = request.form['WaterDemands']
        LightDemands = request.form['LightDemands']
        HumidityDemands = request.form['HumidityDemands']
        Hardness = request.form['Hardness']
        GrowthDetails = request.form['GrowthDetails']
        Pests = request.form['Pests']
        SeedStartDate = request.form['SeedStartDate']
        PlantStartDate = request.form['PlantStartDate']

        #Get user from session
        getuser = user_1seed.query.filter_by(username=session['username']).first()
        getuserid= getuser.id

        plant_update = plant_1seed.query.filter_by(user_id = getuserid,id=id).first()

        plant_update.name = name
        #botanical data:
        plant_update.latin_name = latin_name
        plant_update.family = family
        plant_update.sub_family = sub_family
        plant_update.tribe = tribe
        plant_update.sub_tribe = sub_tribe
        plant_update.genus = genus
        plant_update.perenial = perenial
        plant_update.endangered = endangered
        plant_update.link = link
        plant_update.Description = Description
        #calculated based on location
        plant_update.native = native
        plant_update.flowering_beggining = flowering_beggining
        plant_update.flowering_time = flowering_time
        plant_update.fruiting_beggining = fruiting_beggining
        plant_update.fruiting_time = fruiting_time
        plant_update.transplant_time = transplant_time
		#growing data
        plant_update.SeedTempOpt = SeedTempOpt
        plant_update.SeedTempMin = SeedTempMin
        plant_update.SeedTempMax = SeedTempMax
        plant_update.PlantTempOpt = PlantTempOpt
        plant_update.PlantTempMin = PlantTempMin
        plant_update.PlantTempMax = PlantTempMax
        plant_update.Area_needed = Area_needed
        plant_update.Spacing = Spacing
        plant_update.WaterDemands = WaterDemands
        plant_update.LightDemands = LightDemands
        plant_update.HumidityDemands = HumidityDemands
        plant_update.Hardness = Hardness
        plant_update.GrowthDetails = GrowthDetails
        plant_update.Pests = Pests
        plant_update.SeedStartDate = SeedStartDate
        plant_update.PlantStartDate = PlantStartDate

        db.session.commit()
        flash('Plant item updated', 'success')
        return redirect(url_for('plants.home'))
    return render_template('edit_plant_item.html', form=form)

# Delete plant item
@plants.route('/delete_plant_item/<string:id>', methods=['POST'])
@is_logged_in
def delete_plant_item(id):
    #delete row:
    plant_1seed.query.filter_by(id=id).delete()
    db.session.commit()
    flash('Plant Item Deleted', 'success')
    return redirect(url_for('plants.home'))

#Single plant item
@plants.route('/plantitem/<string:id>/')
def plantitem(id):
    plantitem = plant_1seed.query.filter_by(id = id).first()    
    return render_template('plantitem.html', plantitem=plantitem)