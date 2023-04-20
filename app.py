from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    books = db.relationship('Book', backref='author', lazy=True)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)


@app.route('/authors', methods=['GET'])
def get_authors():
    authors = Author.query.all()
    result = [{'id': author.id, 'name': author.name} for author in authors]
    return jsonify(result)


@app.route('/authors', methods=['POST'])
def create_author():
    data = request.get_json()
    author = Author(name=data['name'])
    db.session.add(author)
    db.session.commit()
    return jsonify({'message': 'Author created successfully'})


@app.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    result = [{'id': book.id, 'title': book.title, 'author_id': book.author_id} for book in books]
    return jsonify(result)


@app.route('/books', methods=['POST'])
def create_book():
    data = request.get_json()
    book = Book(title=data['title'], author_id=data['author_id'])
    db.session.add(book)
    db.session.commit()
    return jsonify({'message': 'Book created successfully'})


@app.route('/authors/<int:author_id>/books/count', methods=['GET'])
def count_books_by_author(author_id):
    author = Author.query.get(author_id)
    if author is None:
        return jsonify({'message': 'Author not found'}), 404
    count = len(author.books)
    return jsonify({'count': count})

# if __name__ == '__main__':
#     app.run()


if __name__ == '__main__':
    app.run(debug=True)

