from flask import Flask, render_template, flash, request, redirect, url_for, session, send_from_directory
from app import models
from .models import user, admin, product
from app import app, db
from app import models
from flask_login import login_user, logout_user, current_user
from flask_session import Session
from werkzeug.utils import secure_filename
import os

app.config['UPLOAD_IMAGES'] = "/Demo_flask/app/static/images/uploads"
ALLOWED_EXTENSIONS = set({'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'})


@app.route('/')
def index():
    return render_template('index.html', data=product.query.all())


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['username']
        password = request.form['password']
        email = request.form['email']
        add_user = user(username=name, password=password, email=email)
        db.session.add(add_user)
        db.session.commit()
        flash("Đăng kí thành công!!! Vui lòng đăng nhập!!!")
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        check = user.query.filter(user.username == username,
                                   user.password == password).first()
        if check:
            session["username"] = request.form.get('username')
            flash("Login sucssess!!!")
            return redirect(url_for('index'))
        flash("Vui lòng kiểm tra lại mật khẩu hoặc tài khoản!!!")
    return render_template('register.html')


@app.route('/cart')
def cart():
    return render_template('cart.html')


@app.route('/detail/<int:id>')
def detail(id):
    return render_template('detail.html', data = product.query.filter_by(id=id).first())


@app.route("/logout_")
def logout():
    session.pop("username", None)
    return redirect(url_for('login'))

# xu li admin
@app.route('/admin', methods=['GET', 'POST'])
def login_admin():
    if request.method == 'POST':
        account = request.form.get('account')
        password = request.form.get('password')
        check = admin.query.filter(admin.account == account,
                                   admin.password == password).first()
        if check:
            session["account"] = request.form.get('account')
            return redirect(url_for('dashboard'))
    return render_template('admin/login.html')


@app.route("/logout_admin")
def logout_admin():
    session.pop("account", None)
    return redirect(url_for('login_admin'))


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if session.get('account') is None:
        return render_template('admin/login.html')
    if request.method == "POST":
        name_product = request.form.get('name_product')
        price = request.form.get('price')
        images = request.files.get('image')
        if images and allowed_file(images.filename):
            filename = secure_filename(images.filename)
            images.save(os.path.join(app.config['UPLOAD_IMAGES'], filename))
            data = product(name_product=name_product, price=price, images=filename)
            db.session.add(data)
            db.session.commit()
            return redirect(url_for('dashboard'))

    return render_template('admin/layout.html', data=product.query.all())


# edididididididididididdiiddididididididtdtdtdtdtdtdtdt

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    data = product.query.filter_by(id=id).first()
    if request.method == 'POST':
        data.name_product = request.form.get('name_product')
        data.price = request.form.get('price')

        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('admin/update.html', data=data)


# ham xoaaooxoaoaoaoaaaoaoaoaoaooaoaoaoaoaoaoxoxoaoaxoxoao
@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    data = product.query.filter_by(id=id).first()
    db.session.delete(data)
    db.session.commit()
    return redirect(url_for('dashboard'))


@app.route('/dashboard/<filename>')
def send_image(filename):
    return send_from_directory("images", filename)
