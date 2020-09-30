from init import *
from _modules.grow.grow import grow
from _modules.storage.storage import storage
from _modules.plants.plants import plants
from _modules.user.user import user
from _modules.dashboard.dashboard import dashboard


#grow module
app.register_blueprint(grow, url_prefix="/grow")

#plants module
app.register_blueprint(plants, url_prefix="/plants")

#storage module
app.register_blueprint(storage, url_prefix="/storage")

#user module
app.register_blueprint(user, url_prefix="/")

#dashboard module
app.register_blueprint(dashboard, url_prefix="/dashboard")

#Index
@app.route('/')
def index():
    return render_template('home.html')

#About
@app.route('/about')
def about():
    return render_template('about.html')



if __name__ == '__main__':
    app.secret_key='secret123'
    #app.run(debug=True)
    
    #for docker :
    app.run(debug=True, host='0.0.0.0')