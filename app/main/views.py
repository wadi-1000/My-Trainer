from flask import render_template,request,url_for,abort,redirect
from . import main
from flask_login import login_required, current_user
from ..models import  User,Role
from .forms import UpdateProfile
from .. import db,photos
import markdown2
from ..requests import get_exercises


@main.route('/')
def index():

    title = 'My Trainer'
    return render_template('index.html', title = title)


@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username=uname).first()
    
    if user is None:
        abort(404)
        
    return render_template("profile/profile.html", user=user)    

@main.route('/user/<uname>/update',methods=['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username=uname).first()
    if user is None:
        abort(404)
        
    form = UpdateProfile()
    
    if form.validate_on_submit():
        user.bio = form.bio.data
        
        db.session.add(user)
        db.session.commit()
        
        return redirect(url_for('.profile', uname=user.username))
    
    return render_template('profile/update.html',form=form)    

@main.route('/user/<uname>/update/pic', methods=['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))  

@main.route('/api')
def api():
    exercises = get_exercises()
    print(exercises)
    title ='My Trainer'
    return render_template('api.html', title = title , exercises = exercises)  

