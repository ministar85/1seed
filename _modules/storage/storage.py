from init import *
from _db.db import *

storage = Blueprint("storage", __name__, static_folder="static", template_folder="templates")

#Storage Form Class
class StorageForm(Form):
    title = StringField('Title', [validators.Length(min=1, max=200)])
    body = TextAreaField('Body', [validators.Length (min=5)])
    description = TextAreaField('Description', [validators.Length (min=10)])
    type = StringField('Type', [validators.Length(min=1, max=200)])
    quantity = IntegerField('Quantity', [validators.DataRequired("Field has to be an integer")])
    
#Storage
@storage.route('/')
@is_logged_in
def home():
    #Get user from session
    getuser = user_1seed.query.filter_by(username=session['username']).first()
    getuserid= getuser.id

    #Get grow Items
    storageitem = storage_1seed.query.filter_by(user_id=getuserid).all()

    if storageitem:
        return render_template('storage.html', storageitem = storageitem)
    else:
        msg = 'No Articles Found'
        return render_template('storage.html', msg=msg)
    
#Single item
@storage.route('/storageitem/<string:id>/')
def storageitem(id):
    storageitem = storage_1seed.query.filter_by(id = id).first()    
    return render_template('storageitem.html', storageitem=storageitem)

#Add Storage Item
@storage.route('/add_storage_item', methods=['GET','POST'])
@is_logged_in
def add_storage_item():
    form = StorageForm(request.form)
    if request.method == 'POST' and form.validate():
        title = form.title.data
        body = form.body.data
        description = form.description.data
        type = form.type.data
        quantity = form.quantity.data

        #Get user from session
        getuser = user_1seed.query.filter_by(username=session['username']).first()
        getuserid= getuser.id

        storage_insert = storage_1seed(title  = title, body  = body, description = description, type = type,
        quantity = quantity, user_id = getuserid)
        db.session.add(storage_insert)
        db.session.commit()

        flash('Storage item created', 'success')

        return redirect(url_for('storage.home'))
    return render_template('add_storage_item.html', form=form)

#Edit Storage Item
@storage.route('/edit_storage_item/<string:id>', methods=['GET','POST'])
@is_logged_in
def edit_storage_item(id):
    #get storage items
    storagetitem = storage_1seed.query.filter_by(id=id).first()
    # Get form
    form = StorageForm(request.form)
    # Populate storage storagetitem fields
    form.title.data = storagetitem.title
    form.body.data = storagetitem.body
    form.description.data = storagetitem.description
    form.type.data = storagetitem.type
    form.quantity.data = storagetitem.quantity

    if request.method == 'POST' and form.validate():
        title = request.form['title']
        body = request.form['body']
        description = request.form['description']
        type = request.form['type']
        quantity = request.form['quantity']

        #Get user from session
        getuser = user_1seed.query.filter_by(username=session['username']).first()
        getuserid= getuser.id

        storage_update = storage_1seed.query.filter_by(user_id = getuserid).first()

        storage_update.title = title
        storage_update.body  = body
        storage_update.description  = description
        storage_update.type = type
        storage_update.quantity = quantity
        db.session.commit()
        flash('Storage item updated', 'success')
        return redirect(url_for('storage.home'))
    return render_template('edit_storage_item.html', form=form)

# Delete Article
@storage.route('/delete_storage_item/<string:id>', methods=['POST'])
@is_logged_in
def delete_storage_item(id):
    storage_1seed.query.filter_by(id=id).delete()
    db.session.commit()
    flash('Storage Item Deleted', 'success')

    return redirect(url_for('storage.home'))


