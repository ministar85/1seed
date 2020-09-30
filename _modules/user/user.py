from init import *
from _db.db import *

user = Blueprint("user", __name__, static_folder="static", template_folder="templates")

#Register form class
class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('UserName', [validators.Length (min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')

################################################################################################
################################################################################################
#User Register
@user.route('register', methods =['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        username = form.username.data
        name = form.name.data
        email = form.email.data
        #encrypt password:
        password = sha256_crypt.encrypt(str(form.password.data))

        exists = db.session.query(user_1seed).filter_by(username=username).scalar() is not None

        #print("- exists :",exists) 
         
        if exists:
            error = 'Username already taken! Are you registered already?'
            return render_template('login.html', error=error)
            #return render_template('register.html', error=error)
        
        #prepare insert
        user_insert = user_1seed(username = username, name = name, email = email, password = password)

        #stage insert
        db.session.add(user_insert)

        #commit to db
        db.session.commit()

        flash('You are now registered and can log in', 'success')
        
        return redirect(url_for('user.login'))
    return render_template('register.html', form=form)

################################################################################################
################################################################################################
# User login
@user.route('login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        #Get Form Fields
        username = request.form['username']
        password_candidate = request.form['password']

        result = user_1seed.query.filter_by(username=[username]).first()

        if result:
            #print("---- result",result) 
            password = result.password

            #Compare Passwords
            if sha256_crypt.verify(password_candidate, password):
                
                #radi: #app.logger.info('PASSWORD MATCHED')
                #Passed
                session['logged_in'] = True
                session['username'] = username
                flash('You are now logged in','success')
                #return redirect(url_for('Grow'))
                return redirect(url_for('grow.home_init'))
            else:
                error = 'Invalid login'
                return render_template('login.html', error=error)
                #app.logger.info('PASSWORD NOT MATCHED')
        else:
            error = 'Username not found'
            return render_template('login.html', error=error)
            #app.logger.info('NO USER')
    return render_template('login.html')

################################################################################################
################################################################################################
#Logout
@user.route('logout')
def logout():
        session.clear()
        flash('You are now logged out', 'success')
        return redirect(url_for('user.login'))
