from init import *
from _db.db import *
from wtforms import SelectField
from wtforms.ext.sqlalchemy.fields import QuerySelectField

grow = Blueprint("grow", __name__, static_folder="static", template_folder="templates")

def choice_query():
    return plant_1seed.query

#GrowForm Form Class
class GrowForm(Form):
    title = StringField('title', [validators.Length(min=1, max=200)])
    #plant_name = StringField('plant_name', [validators.Length(min=1, max=200)])
    #plant_name = QuerySelectField(query_factory=lambda: plant_1seed.query().all())
    plant_name = QuerySelectField(query_factory=choice_query, allow_blank=False, get_label='name')

    growitem_surface = IntegerField('growitem_surface', [validators.DataRequired("Field has to be float")])
    growitem_quantity = IntegerField('growitem_quantity', [validators.DataRequired("Field has to be an integer")])
    event_alert = StringField('event_alert', [validators.Length(min=1, max=200)])
    time_planted_greenhouse = DateField('time_planted_greenhouse', format='%Y-%m-%d')
    time_planted_outdoor = DateField('time_planted_outdoor', format='%Y-%m-%d')
    perenial = IntegerField('perenial', [validators.DataRequired("Field has to be integer")])
    grow_time = IntegerField('grow_time', [validators.DataRequired("Field has to be integer")])
    grow_group_name = StringField('grow_group_name', [validators.Length(min=1, max=200)])
    grow_group_type = StringField('grow_group_type', [validators.Length(min=1, max=200)])


class GrowFormEdit(Form):
    title = StringField('title', [validators.Length(min=1, max=200)])
    #plant_name = StringField('plant_name', [validators.Length(min=1, max=200)])
    #plant_name = QuerySelectField(query_factory=lambda: plant_1seed.query().all())
    plant_name = StringField('plant_name', [validators.Length(min=1, max=200)])

    growitem_surface = IntegerField('growitem_surface', [validators.DataRequired("Field has to be integer")])
    growitem_quantity = IntegerField('growitem_quantity', [validators.DataRequired("Field has to be an integer")])
    event_alert = StringField('event_alert', [validators.Length(min=1, max=200)])
    time_planted_greenhouse = DateField('time_planted_greenhouse', format='%Y-%m-%d')
    time_planted_outdoor = DateField('time_planted_outdoor', format='%Y-%m-%d')
    perenial = IntegerField('perenial', [validators.DataRequired("Field has to be integer")])
    grow_time = IntegerField('grow_time', [validators.DataRequired("Field has to be integer")])
    grow_group_name = StringField('grow_group_name', [validators.Length(min=1, max=200)])
    grow_group_type = StringField('grow_group_type', [validators.Length(min=1, max=200)])

class GrowPageForm(Form):
    name = StringField('name', [validators.Length(min=1, max=200)])
    surface = StringField('surface', [validators.DataRequired("Field has to be an integer")])

#first load of the grow module without selected grow page
@grow.route('/')
@is_logged_in
#def storage(username):
def home_init():
    #Get user from session
    getuser = user_1seed.query.filter_by(username=session['username']).first()
    getuserid= getuser.id

    #Get grow pages
    growpages = grow_page_1seed.query.filter_by(user_id=getuserid).all()
    
    return render_template('Grow.html', growpages=growpages)

#Add Grow Page
@grow.route('/add_Grow_page', methods=['GET','POST'])
@is_logged_in
def add_Grow_page():
    form = GrowPageForm(request.form)

    if request.method == 'POST' and form.validate():
        name = form.name.data
        surface = form.surface.data

        #Get user from session
        getuser = user_1seed.query.filter_by(username=session['username']).first()
        getuserid= getuser.id

        grow_page_insert = grow_page_1seed(
            name = name,
            surface = surface,
            user_id = getuserid)
            
        db.session.add(grow_page_insert)
        db.session.commit()

        flash('Grow Page item created', 'success')
        #return redirect(url_for('grow.home', grow_page_id = 2))
        return redirect(url_for('grow.home_init'))
    return render_template('add_Grow_Page.html', form=form)

#Edit Grow Page
@grow.route('/edit_Grow_Page/<string:id>', methods=['GET','POST'])
@is_logged_in
def edit_Grow_Page(id):
    growpage = grow_page_1seed.query.filter_by(id=id).first()

    #Get grow page

    # Get form
    form = GrowPageForm(request.form)

    # Populate Grow item fields
    form.name.data = growpage.name
    form.surface.data = growpage.surface
    
    if request.method == 'POST' and form.validate():
        name = request.form['name']
        surface = request.form['surface']
        
        #Get user from session
        getuser = user_1seed.query.filter_by(username=session['username']).first()
        getuserid= getuser.id

        grow_update = grow_page_1seed.query.filter_by(user_id = getuserid, id = id).first()

        grow_update.name = name
        grow_update.surface = surface

        db.session.commit()
        
        flash('Grow Page updated', 'success')
        return redirect(url_for('grow.home', grow_page_id = id))
    return render_template('edit_Grow_Page.html', form=form)

# Delete Grow Page
@grow.route('/delete_Grow_Page/<string:id>', methods=['POST'])
@is_logged_in
def delete_Grow_Page(id):
    #delete row:
    grow_page_1seed.query.filter_by(id=id).delete()
    db.session.commit()

    flash('Grow Page Deleted', 'success')
    return redirect(url_for('grow.home_init'))



#page not loaded
@grow.route('/add_Grow_item/')
@is_logged_in
#def storage(username):
def home_grownotselected():

    flash('No Grow Page selected : Select grow page', 'warning')
    
    return redirect(url_for('grow.home_init'))

#selected grow page
@grow.route('/<string:grow_page_id>')
@is_logged_in
#def storage(username):
def home(grow_page_id):
    #Get user from session
    getuserid= user_1seed.query.filter_by(username=session['username']).first().id
    #Get grow pages
    growpages = grow_page_1seed.query.filter_by(user_id=getuserid).all()
    ###### get selected page items :
    growitems = grow_1seed.query.filter_by(user_id=getuserid, grow_page_id=grow_page_id).all()
    #get selected grow page
    selected_grow_page_name = grow_page_1seed.query.filter_by(id=grow_page_id).first().name
    selected_grow_page_id = grow_page_1seed.query.filter_by(id=grow_page_id).first().id
    ####################################################
                # calculation for grow page
    ####################################################
    #calculate remaining space
    remaining_space = grow_page_1seed.query.filter_by(id=grow_page_id).first().surface 
    perenial_percentage = 0
    n_grow_items = grow_1seed.query.filter_by(grow_page_id=grow_page_id).count()
    all_grow_items = grow_1seed.query.filter_by(grow_page_id=grow_page_id).all()
    grow_surface_used = 0
    perenialtotal = 0
    total_plants = 0
    if (n_grow_items > 0):
        print("number of grow items =",n_grow_items)
        for i in range(0,n_grow_items):
            ######################################
            ####make this adjustable later on#####
            ######################################

            #grow_location paths = 10%
            grow_location_paths = 1.1
            
            #plant data
            total_plants += all_grow_items[i].growitem_quantity
            plant_id = all_grow_items[i].plant_id

            #surface used
            grow_surface_used += all_grow_items[i].growitem_quantity * all_grow_items[i].growitem_surface * grow_location_paths

            #perenial %
            perenialtotal += plant_1seed.query.filter_by(id=plant_id).first().perenial * all_grow_items[i].growitem_quantity

            #

        remaining_space = grow_page_1seed.query.filter_by(id=grow_page_id).first().surface - grow_surface_used
        print("total plants growing:",total_plants)
        print("total perenials:",perenialtotal)
        perenial_percentage = 100*perenialtotal/total_plants
        print("perenial percentage:",perenial_percentage)

    #options = ("select user.Name as Label, case when assigned.id is null then 0 else 1 end as Selected from user_table as user left join assign as assigned on assigned.user_id = user.id
    return render_template('Grow.html', growitems=growitems, growpages=growpages, selected_grow_page_name = selected_grow_page_name,
    selected_grow_page_id = selected_grow_page_id, remaining_space = remaining_space, perenial_percentage = perenial_percentage) 

#Timetable
@grow.route('/Timetable/<string:grow_page_id>')
@is_logged_in
#def storage(username):
def timetable(grow_page_id):
    #Get user from session
    getuserid= user_1seed.query.filter_by(username=session['username']).first().id
    #Get grow pages
    growpages = grow_page_1seed.query.filter_by(user_id=getuserid).all()
    ###### get selected page items :
    growitems = grow_1seed.query.filter_by(user_id=getuserid, grow_page_id=grow_page_id).all()
    #get selected grow page
    selected_grow_page_name = grow_page_1seed.query.filter_by(id=grow_page_id).first().name
    selected_grow_page_id = grow_page_1seed.query.filter_by(id=grow_page_id).first().id


    #starttimes = grow_1seed.query.filter_by(user_id=getuserid, grow_page_id=grow_page_id).id
    print("*******************")
    print("*******************")
    print("*******************")
    print("*******************")

    #options = ("select user.Name as Label, case when assigned.id is null then 0 else 1 end as Selected from user_table as user left join assign as assigned on assigned.user_id = user.id
    return render_template('GrowTimetable.html', growitems=growitems, growpages=growpages, selected_grow_page_name = selected_grow_page_name, selected_grow_page_id = selected_grow_page_id)

#Add Grow Item
@grow.route('/add_Grow_item/<string:grow_page_id>', methods=['GET','POST'])
@is_logged_in
def add_Grow_item(grow_page_id):
    form = GrowForm(request.form)

    if request.method == 'POST' and form.validate():
        title = form.title.data
        plant_name = form.plant_name.data
        #plant_id = form.plant_id.data
        #growitem_surface = form.growitem_surface.data
        growitem_quantity = form.growitem_quantity.data
        event_alert = form.event_alert.data
        time_planted_greenhouse = form.time_planted_greenhouse.data
        time_planted_outdoor = form.time_planted_outdoor.data
        perenial = form.perenial.data
        grow_time = form.grow_time.data
        
        grow_group_name = form.grow_group_name.data
        grow_group_type = form.grow_group_type.data
        
        print("******************* :",plant_name)
        print("******************* :",plant_name.name)
        print("******************* :",plant_name.id)
   

        #Get user from session
        getuser = user_1seed.query.filter_by(username=session['username']).first()
        getuserid= getuser.id

        grow_insert = grow_1seed(
            title = title,
            plant_name = plant_name.name, 
            plant_id = plant_name.id, 
            growitem_surface = plant_name.Area_needed, 
            spacing = plant_name.Spacing, 
            growitem_quantity = growitem_quantity, 
            event_alert = event_alert, 
            time_planted_greenhouse = time_planted_greenhouse,
            time_planted_outdoor = time_planted_outdoor, 
            perenial = perenial, 
            grow_time = grow_time, 
            grow_group_name = grow_group_name, 
            grow_group_type = grow_group_type,
            user_id = getuserid,
            grow_page_id = grow_page_id)
            
        db.session.add(grow_insert)
        db.session.commit()

        flash('Grow item created', 'success')
        return redirect(url_for('grow.home', grow_page_id = grow_page_id))
    return render_template('add_Grow_item.html', form=form)


#Edit Grow Item
@grow.route('/edit_Grow_item/<string:id>', methods=['GET','POST'])
@is_logged_in
def edit_Grow_item(id):
    growitem = grow_1seed.query.filter_by(id=id).first()

    #Get grow page
    grow_page_id = grow_1seed.query.filter_by(id=id).first().grow_page_id

    # Get form
    form = GrowFormEdit(request.form)

    # Populate Grow item fields
    form.title.data = growitem.title
    form.plant_name.data = growitem.plant_name
    #form.plant_id.data = growitem.plant_id
    form.growitem_surface.data = growitem.growitem_surface
    form.growitem_quantity.data = growitem.growitem_quantity
    form.event_alert.data = growitem.event_alert
    form.time_planted_greenhouse.data = growitem.time_planted_greenhouse
    form.time_planted_outdoor.data = growitem.time_planted_outdoor
    form.perenial.data = growitem.perenial
    form.grow_time.data = growitem.grow_time
    form.grow_group_name.data = growitem.grow_group_name
    form.grow_group_type.data = growitem.grow_group_type


    #if request.method == 'POST' and form.validate():
    if request.method == 'POST':
        title = request.form['title']
        #plant_name = request.form['plant_name']
        #plant_id = request.form['plant_id']
        growitem_surface = request.form['growitem_surface']
        growitem_quantity = request.form['growitem_quantity']
        event_alert = request.form['event_alert']
        time_planted_greenhouse = request.form['time_planted_greenhouse']
        time_planted_outdoor = request.form['time_planted_outdoor']
        perenial = request.form['perenial']
        grow_time = request.form['grow_time']
        grow_group_name = request.form['grow_group_name']
        grow_group_type = request.form['grow_group_type']

        #Get user from session
        getuser = user_1seed.query.filter_by(username=session['username']).first()
        getuserid= getuser.id

        grow_update = grow_1seed.query.filter_by(user_id = getuserid, id = id).first()

        grow_update.title = title
        #grow_update.plant_name = plant_name
        #grow_update.plant_id = plant_id
        grow_update.growitem_surface = growitem_surface
        grow_update.growitem_quantity = growitem_quantity
        grow_update.event_alert = event_alert
        grow_update.time_planted_greenhouse = time_planted_greenhouse
        grow_update.time_planted_outdoor = time_planted_outdoor
        grow_update.perenial = perenial
        grow_update.grow_time = grow_time
        grow_update.grow_group_name = grow_group_name
        grow_update.grow_group_type = grow_group_type
        grow_update.grow_page_id = grow_page_id

        db.session.commit()
        
        flash('Grow item updated', 'success')
        return redirect(url_for('grow.home', grow_page_id = grow_page_id))
    return render_template('edit_Grow_item.html', form=form)

# Delete Article
@grow.route('/delete_Grow_item/<string:id>', methods=['POST'])
@is_logged_in
def delete_Grow_item(id):
    #Get grow page
    grow_page_id = grow_1seed.query.filter_by(id=id).first().grow_page_id
    
    #delete row:
    grow_1seed.query.filter_by(id=id).delete()
    db.session.commit()

    flash('Grow Item Deleted', 'success')
    return redirect(url_for('grow.home', grow_page_id = grow_page_id))

#Single grow item
@grow.route('/growitem/<string:id>/')
def growitem(id):
    #if query.filter_by(id = id).all()  [] is returned which is list of lists (even though there is one) therefore .first() has to be used ~ fetch one
    growitem = grow_1seed.query.filter_by(id = id).first()

    return render_template('growitem.html', growitem=growitem)

