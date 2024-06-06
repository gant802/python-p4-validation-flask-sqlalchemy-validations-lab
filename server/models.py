from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('name')
    def validate_name(self, key, value):
        if not value:
            raise ValueError('Name cannot be empty')
        if Author.query.filter_by(name=value).first():
            raise ValueError('Name already exists')
        return value

    @validates('phone_number')
    def validate_phone_number(self, key, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError('Phone number must be exactly 10 digits')
        return value

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('content', 'summary')
    def validate_length(self, key, string):
        if( key == 'content'):
            if len(string) < 250:
                raise ValueError("Post content must be greater than or equal 250 characters long.")
        if( key == 'summary'):
            if len(string) > 250:
                raise ValueError("Post summary must be less than or equal to 250 characters long.")
        return string
    
    @validates('title')
    def validate_title(self, key, value):
        if len(value) == 0 or not value:
            raise ValueError('Title cannot be empty')

        required_words = ['Guess', 'Top', 'Secret', 'Won\'t Believe']
        if not any(word in value for word in required_words):
            raise ValueError(f"Content must contain at least one of the words: {', '.join(required_words)}")
        return value
    
    @validates('category')
    def validate_category(self, key, value):
        if value != 'Fiction' and value != "Non-Fiction":
            raise ValueError('Category must be Fiction or Non-Fiction')
        return value

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'



