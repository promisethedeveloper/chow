from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


favorites = db.Table("favorites",
        db.Column("id", db.Integer, primary_key=True, autoincrement=True),
        db.Column("user_id", db.Integer, db.ForeignKey("users.id", ondelete="CASCADE")),
        db.Column("business_id", db.Integer, db.ForeignKey("businesses.id", ondelete="CASCADE"))
)


class User(db.Model):
    """Site user."""

    __tablename__ = "users"

    id = db.Column(db.Integer, 
                   primary_key=True, 
                   autoincrement=True)
    first_name = db.Column(db.Text, 
                         nullable=False)
    last_name = db.Column(db.Text, 
                         nullable=False) 
    email = db.Column(db.Text, 
                         nullable=False, 
                         unique=True)
    password = db.Column(db.Text, 
                         nullable=False)

    
    @classmethod
    def register(cls, first_name, last_name, email, password):
        """Register user w/hashed password & return user."""

        hashed = bcrypt.generate_password_hash(password)
         # turn bytestring into normal (unicode utf8) string
        hashed_utf8 = hashed.decode("utf8")

        user = cls(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=hashed_utf8
        )
        # return instance of user w/username and hashed pwd
        return user

    @classmethod
    def authenticate(cls, email, password):
        """Validate that user exists & password is correct.

        Return user if valid; else return False.
        """

        u = User.query.filter_by(email=email).first()

        if u and bcrypt.check_password_hash(u.password, password):
            # return user instance
            return u
        else:
            return False


class Business(db.Model):
    """Businesses from Yelp API."""

    __tablename__ = "businesses"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    business_yelp_id = db.Column(db.String, nullable=False, unique=True)

    users = db.relationship("User", secondary=favorites, backref="businesses", cascade="all,delete")





