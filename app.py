from form import SearchForm, LoginForm
from db import BookDatabase

from flask import Flask, request, sessions, redirect, url_for, render_template
from flask_login import UserMixin


app = Flask(__name__)
app.secret_key = b'\xfd_W9\xd6_\xee\x0e\x18l\x88\x1fl>=\x97'


class User(UserMixin):
    def __init__(self, id):
        self.database = BookDatabase
        self.id = id

        db = self.database()
        self.name = db.get_username_by_id(id)
        self.password = db.get_password_by_id(id)

    def __repr__(self):
        return '<{}, {}, {}>'.format(self.id, self.name, self.password)


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    # return search_front()
    form = SearchForm()
    if form.validate_on_submit():
        return redirect(url_for('search', book_name=form.book_name.data))
    return render_template('index.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        submit_form = request.form
        username = submit_form['username']
        password = submit_form['password']
        db = BookDatabase()
        if db.validate_login(username, password):
            return redirect(url_for('reviews'))
        else:
            return redirect(url_for('login'))
    return render_template('login.html', form=form)


@app.route('/search', methods=['GET', 'POST'])
def search_front():
    form = SearchForm()
    if form.validate_on_submit():
        return redirect(url_for('search', book_name=form.book_name.data))
    return render_template('search.html', form=form)


@app.route('/search?book_name=<book_name>')
def search(book_name):
    db = BookDatabase()
    searchKey=book_name
    book_list = db.search_with_book_name(book_name)
    form = SearchForm()
    return render_template('search.html', form=form, book_list=book_list, searchKey=searchKey)

@app.route('/book?book_id=<book_id>')
def book_detail(book_id):
    db = BookDatabase()
    searchKey=book_id
    book_list = db.get_book_detail(book_id)
    reviews_list = db.get_reviews_by_book_id(book_id)
    form = SearchForm()
    return render_template('book.html', form=form, book_list=book_list, reviews_list=reviews_list, searchKey=searchKey)

@app.route('/reviews')
def reviews():
    db = BookDatabase()
    review_list = db.get_reviews()
    return render_template('reviews.html', review_list=review_list)


if __name__ == '__main__':
    app.run(debug=True)
