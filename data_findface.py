import pathlib

import flask
import flask_sqlalchemy
import flask_restless

app = flask.Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = flask_sqlalchemy.SQLAlchemy(app)


class Meeting(db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.Unicode)
    photos = db.relationship('Photo', backref='meeting')


class Photo(db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    meeting_id = db.Column(db.Unicode, db.ForeignKey('meeting.id'))
    name: str = db.Column(db.Unicode)
    faces = db.relationship('Face', backref=db.backref('photo'))


class Face(db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    photo_id = db.Column(db.Unicode, db.ForeignKey('photo.id'))
    presisted_face_id: str = db.Column(db.Unicode)
    email: str = db.Column(db.Unicode)
    auto_identified: str = db.Column(db.Boolean)
    top: int = db.Column(db.Integer)
    left: int = db.Column(db.Integer)
    width: int = db.Column(db.Integer)
    height: int = db.Column(db.Integer)


path = pathlib.Path('db.sqlite')
if path.exists():
    path.unlink()

db.create_all()

meeting = Meeting(name='Innovation Meetup')
db.session.add(meeting)

photo = Photo(name='IMG123.jpg', meeting=meeting)
db.session.add(photo)

face = Face(email='axel.delamarre@sgcib.com', auto_identified=True, top=243, left=612, width=120, height=134, photo=photo)
db.session.add(face)
face = Face(auto_identified=False, top=243, left=612, width=120, height=134, photo=photo)
db.session.add(face)

db.session.commit()


def populate_db_from_json():
    import data
    meetings = data.load_meetings()
    for meeting in meetings:
        db.session.add(Meeting(
            name=meeting.name,
        ))
        for photo in meeting.photos:
            db.session.add(Photo(

            ))


# Create the Flask-Restless API manager.
manager = flask_restless.APIManager(app, flask_sqlalchemy_db=db)

# Create API endpoints, which will be available at /api/<tablename> by
# default. Allowed HTTP methods can be specified as well.
manager.create_api(Meeting, methods=['GET'], include_columns=['id', 'photos', 'photos[faces]'])
manager.create_api(Photo, methods=['GET'])
manager.create_api(Face, methods=['GET'])

# start the flask loop
app.run()
