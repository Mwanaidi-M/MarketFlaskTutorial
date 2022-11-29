from market import my_db, login_manager

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

import secrets


def gen():
    return secrets.token_hex(6)


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


class Users(my_db.Model, UserMixin):
    user_id = my_db.Column(my_db.Integer(), primary_key=True)
    user_name = my_db.Column(my_db.String(length=30), unique=True, nullable=False)
    user_email = my_db.Column(my_db.String(length=50), unique=True, nullable=False)
    user_password_hash = my_db.Column(my_db.String(length=120), nullable=False)
    user_budget = my_db.Column(my_db.Integer(), nullable=False, default=1000)
    user_items = my_db.relationship('Items', backref='owned_user', lazy=True)

    def set_pwd_hash(self, pwd):
        self.user_password_hash = generate_password_hash(pwd)

    def check_pwd(self, pwd):
        return check_password_hash(self.user_password_hash, pwd)

    def get_id(self):
        return self.user_id

    @property
    def format_budget(self):
        return f'{self.user_budget:,}'

    def can_purchase(self, item_obj):
        return self.user_budget >= item_obj.item_price

    def can_sell(self, item_obj):
        return item_obj in self.user_items

    def __repr__(self):
        return f'User:{self.user_name}'


class Items(my_db.Model):
    item_id = my_db.Column(my_db.Integer(), primary_key=True)
    item_name = my_db.Column(my_db.String(length=48), nullable=False, unique=True)
    item_barcode = my_db.Column(my_db.String(length=12), nullable=False, unique=True, default=gen)
    item_price = my_db.Column(my_db.Integer(), nullable=False)
    item_description = my_db.Column(my_db.String(length=1024), nullable=False, unique=True)
    owner = my_db.Column(my_db.Integer(), my_db.ForeignKey('users.user_id'))

    def make_purchase(self, user):
        self.owner = user.user_id
        user.user_budget -= self.item_price
        my_db.session.commit()

    def sell_item(self, user):
        self.owner = None
        user.user_budget += self.item_price
        my_db.session.commit()

    def __repr__(self):
        return f'Item:{self.item_name}'
