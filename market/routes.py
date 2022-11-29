from market import my_app, my_db

from .models import Items, Users
from .forms import RegisterForm, LoginForm, BuyItemForm, SellItemForm

from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user


@my_app.route('/')
@my_app.route('/home')
def home():
    return render_template('index.html')


@my_app.route('/market', methods=['GET', 'POST'])
@login_required
def market_page():
    # items = [
    #     {'id': 1, 'name': 'Phone', 'barcode': '893212299897', 'price': 500},
    #     {'id': 2, 'name': 'Laptop', 'barcode': '123985473165', 'price': 900},
    #     {'id': 3, 'name': 'Keyboard', 'barcode': '231985128446', 'price': 150}
    # ]
    purchase_form = BuyItemForm()
    sale_form = SellItemForm()

    if request.method == 'POST':
        # purchase item logic
        purchased_item = request.form.get('purchased_item')
        purchased_item_obj = Items.query.filter_by(item_name=purchased_item).first()

        if purchased_item_obj is not None:
            if current_user.can_purchase(purchased_item_obj):
                purchased_item_obj.make_purchase(current_user)
                flash(f'Item {purchased_item_obj.item_name} purchased successfully!', category='success')
            else:
                flash(f'Insufficient funds to make a purchase for Item: {purchased_item_obj.item_name}.',
                      category='danger')

        # sell item logic
        sold_item = request.form.get('sold_item')
        sold_item_obj = Items.query.filter_by(item_name = sold_item).first()

        if sold_item_obj is not None:
            if current_user.can_sell(sold_item_obj):
                sold_item_obj.sell_item(current_user)
                flash(f'Item:{sold_item_obj.item_name} is now back on the market', category='success')
            else:
                flash(f'Sorry. You do not have ownership of Item:{sold_item_obj.item_name}', category='danger')

        return redirect(url_for('market_page'))

    if request.method == 'GET':
        free_items = Items.query.filter_by(owner=None)
        owned_items = Items.query.filter_by(owner=current_user.user_id)
        return render_template('market.html', m_items=free_items, o_items=owned_items, buy_form=purchase_form, sell_form=sale_form)


@my_app.route('/sign-up', methods=['GET', 'POST'])
def register_page():
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        new_user = Users(user_name=register_form.username.data,
                         user_email=register_form.email.data,
                         user_password_hash=register_form.pwd1.data)

        new_user.set_pwd_hash(register_form.pwd1.data)

        my_db.session.add(new_user)
        my_db.session.commit()
        login_user(new_user)
        flash(f'Account created successfully. Logged In as: {new_user.user_name}', category='success')
        return redirect(url_for('market_page'))
    return render_template('sign-up.html', form=register_form)


@my_app.route('/login', methods=['GET', 'POST'])
def login_page():
    login_form = LoginForm()

    if login_form.validate_on_submit():
        attempted_user = Users.query.filter_by(user_name=login_form.username.data).first()
        if attempted_user is None or not attempted_user.check_pwd(login_form.pwd.data):
            flash('Invalid username or password', category='danger')
            return redirect(url_for('login_page'))
        login_user(attempted_user)
        flash(f'Login Successful for {attempted_user.user_name}', category='success')
        return redirect(url_for('market_page'))
    return render_template('login.html', form=login_form)


@my_app.route('/logout')
def logout_page():
    logout_user()
    flash('You are logged out!', category='info')
    return redirect(url_for('home'))
