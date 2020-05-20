# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#

import logging
import sys
from logging import Formatter, FileHandler
import babel
import dateutil.parser
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from forms import *

# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)



# get '{Jazz,Reggae,Swing,Classical,Folk}' and return ['Jazz', 'Reggae', 'Swing', 'Classical', 'Folk']
def get_genres(str):
    ret = []
    ptr = 1  # pointer to the start of word
    ptr2 = 1  # pointer to the end of word
    for i in range(len(str)):
        if str[i] == '{':
            continue
        elif str[i] == '}':
            to_add = str[ptr:i]
            ret.append(to_add)
            break
        if str[i] != ',':
            ptr2 += 1
        else:
            to_add = str[ptr:ptr2]
            ret.append(to_add)
            ptr = i + 1
            ptr2 = ptr

    return ret


# ------------------------------------- ---------------------------------------#
# Models.
# ----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String())
    facebook_link = db.Column(db.String(120))
    genres = db.Column(db.String(), nullable=False)
    website = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String)
    shows = db.relationship('Show', backref=db.backref('venue', cascade="all,delete", lazy=True))
 


class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(), nullable=False)
    image_link = db.Column(db.String())
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String)
    shows = db.relationship('Show', backref=db.backref('artist', cascade="all,delete", lazy=True))



class Show(db.Model):
    __tablename__ = 'Show'
    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=True)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=True)
    start_time = db.Column(db.DateTime(), nullable=False)




# ----------------------------------------------------------------------------#
# Filters.
# ----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    # return  value
    return babel.dates.format_datetime(date, format, locale='en')


app.jinja_env.filters['datetime'] = format_datetime


# ----------------------------------------------------------------------------#
# Controllers.
# ----------------------------------------------------------------------------#

@app.route('/')
def index():
    return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
 
    #       num_shows should be aggregated based on number of upcoming shows per venue.(DONE)
    places = db.session.query(Venue.city, Venue.state).distinct(
        Venue.city, Venue.state)
    data = []
    for place in places:
        venues_in_place = db.session.query(Venue.id, Venue.name).filter(Venue.city == place[0]).filter(
            Venue.state == place[1])
        data.append({
            "city": place[0],
            "state": place[1],
            "venues": [{
                "id": v.id,
                "name": v.name,
                "num_upcoming_shows": len(
                    Show.query.filter(Show.venue_id == v.id).filter(Show.start_time > datetime.now()).all()),
            } for v in venues_in_place]})
    return render_template('pages/venues.html', areas=data)


@app.route('/venues/search', methods=['POST'])
def search_venues():

    # search for Hop should return "The Musical Hop".
    # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
    search = request.form.get('search_term')
    venue_search_result = Venue.query.filter(
        Venue.name.ilike('%' + search + '%')).all()
    response = {
        "count": len(venue_search_result),
        "data": [{
            "id": v.id,
            "name": v.name,
            "num_upcoming_shows": len(v.shows)
        } for v in venue_search_result]
    }
    return render_template('pages/search_venues.html', results=response,
                           search_term=request.form.get('search_term', ''))


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    # shows the venue page with the given venue_id
    venus = Venue.query.all()
    data1 = [{
        "id": v.id,
        "name": v.name,
        "genres": get_genres(v.genres),
        "address": v.address,
        "city": v.city,
        "state": v.state,
        "phone": v.phone,
        "website": v.website,
        "facebook_link": v.facebook_link,
        "seeking_talent": v.seeking_talent,
        "seeking_description": v.seeking_description,
        "image_link": v.image_link,
        "past_shows": [{
            "artist_id": s.artist_id,
            "artist_name": Artist.query.get(s.artist_id).name,
            "artist_image_link": Artist.query.get(s.artist_id).image_link,
            "start_time": str(s.start_time)
        } for s in Show.query.filter(Show.start_time <= datetime.now(), Show.venue_id == v.id).all()],
        "upcoming_shows": [{
            "artist_id": s.artist_id,
            "artist_name": Artist.query.get(s.artist_id).name,
            "artist_image_link": Artist.query.get(s.artist_id).image_link,
            "start_time": str(s.start_time)
        } for s in Show.query.filter(Show.start_time > datetime.now(), Show.venue_id == v.id).all()],
        "past_shows_count": len(Show.query.filter(Show.start_time <= datetime.now(), Show.venue_id == v.id).all()),
        "upcoming_shows_count": len(Show.query.filter(Show.start_time > datetime.now(), Show.venue_id == v.id).all()),
    } for v in venus]
    data = list(filter(lambda d: d['id'] == venue_id, data1))[0]
    return render_template('pages/show_venue.html', venue=data)


#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    error = False
    form = request.form
    try:
        n_venue = Venue(
            name=form.get('name'),
            city=form.get('city'),
            state=form.get('state'),
            address=form.get('address'),
            phone=form.get('phone'),
            image_link=form.get('image_link'),
            facebook_link=form.get('facebook_link'),
            genres=form.getlist('genres'),
            website=form.get('website'),
            seeking_talent=bool(form.get('seeking_talent')),
            seeking_description=form.get('seeking_description')
        )
        db.session.add(n_venue)
        db.session.commit()
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if not error:
        # on successful db insert, flash success
        flash('Venue ' + request.form['name'] + ' was successfully listed!')
    else:
        # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
        # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
        flash('An error occurred. Venue ' +
              request.form['name'] + ' could not be listed.')

    return render_template('pages/home.html')


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
    try:
        venue = Venue.query.get(venue_id)
        Show.query.filter(Show.venue_id == venue_id).delete()
        db.session.delete(venue)
        db.session.commit()
    except:
        print(sys.exc_info())
        db.session.rollback()
    finally:
        db.session.close()
    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage
    return None


#  Artists
#  ------------------------------------------   ----------------------
@app.route('/artists')
def artists():
    data = Artist.query.all()
    return render_template('pages/artists.html', artists=data)


@app.route('/artists/search', methods=['POST'])
def search_artists():
    # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
    # search for "band" should return "The Wild Sax Band".
    search = request.form.get('search_term')
    artist_search_result = Artist.query.filter(
        Artist.name.ilike('%' + search + '%')).all()
    response = {
        "count": len(artist_search_result),
        "data": [{
            "id": a.id,
            "name": a.name,
            "num_upcoming_shows": len(a.shows),
        } for a in artist_search_result]
    }
    return render_template('pages/search_artists.html', results=response,
                           search_term=request.form.get('search_term', ''))


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    # shows the venue page with the given venue_id
    artist = Artist.query.all()
    data1 = [{
        "id": a.id,
        "name": a.name,
        "genres": get_genres(a.genres),
        "city": a.city,
        "state": a.state,
        "phone": a.phone,
        "website": a.website,
        "facebook_link": a.facebook_link,
        "seeking_venue": a.seeking_venue,
        "seeking_description": a.seeking_description,
        "image_link": a.image_link,
        "past_shows": [{
            "venue_id": s.venue_id,
            "venue_name": Venue.query.get(s.venue_id).name,
            "venue_image_link": Venue.query.get(s.venue_id).image_link,
            "start_time": str(s.start_time)
        } for s in Show.query.filter(Show.start_time < datetime.now(), Show.artist_id == a.id).all()],
        "upcoming_shows": [{
            "venue_id": s.venue_id,
            "venue_name": Venue.query.get(s.venue_id).name,
            "venue_image_link": Venue.query.get(s.venue_id).image_link,
            "start_time": str(s.start_time)
        } for s in Show.query.filter(Show.start_time > datetime.now(), Show.artist_id == a.id).all()],
        "past_shows_count": len(Show.query.filter(Show.start_time <= datetime.now(), Show.artist_id == a.id).all()),
        "upcoming_shows_count": len(Show.query.filter(Show.start_time > datetime.now(), Show.artist_id == a.id).all()),
    } for a in artist]
    data = list(filter(lambda d: d['id'] == artist_id, data1))[0]
    return render_template('pages/show_artist.html', artist=data)


#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    artist = Artist.query.get(artist_id)
    form = ArtistForm(
        name=artist.name,
        genres=artist.genres,
        city=artist.city,
        state=artist.state,
        phone=artist.phone,
        website=artist.website,
        facebook_link=artist.facebook_link,
        seeking_venue=artist.seeking_venue,
        seeking_description=artist.seeking_description,
        image_link=artist.image_link)
    return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<artist_id>', methods=['DELETE'])
def delete_artist(artist_id):
    try:
        artist = Artist.query.get(artist_id)
        Show.query.filter(Show.artist_id == artist_id).delete()
        db.session.delete(artist)
        db.session.commit()
    except:
        print(sys.exc_info())
        db.session.rollback()
    finally:
        db.session.close()
    return None


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    # artist record with ID <artist_id> using the new attributes
    try:
        artist = Artist.query.get(artist_id)
        form = request.form
        artist.name = request.form.get('name')
        artist.city = request.form.get('city')
        artist.state = request.form.get('state')
        artist.phone = request.form.get('phone')
        artist.genres = request.form.getlist('genres')
        artist.facebook_link = request.form.get('facebook_link')
        artist.website = request.form.get('website')
        artist.image_link = request.form.get('image_link')
        artist.seeking_venue = bool(request.form.get('seeking_venue'))
        artist.seeking_description = request.form.get('seeking_description')
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()

    return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    venue = Venue.query.get(venue_id)
    form = VenueForm(
        name=venue.name,
        genres=venue.genres,
        address=venue.address,
        city=venue.city,
        state=venue.state,
        phone=venue.phone,
        website=venue.website,
        facebook_link=venue.facebook_link,
        seeking_talent=venue.seeking_talent,
        seeking_description=venue.seeking_description,
        image_link=venue.image_link
    )
    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    # venue record with ID <venue_id> using the new attributes
    try:
        venue = Venue.query.get(venue_id)
        form = request.form
        venue.name = form.get('name')
        venue.city = form.get('city')
        venue.state = form.get('state')
        venue.address = form.get('address')
        venue.phone = form.get('phone')
        venue.facebook_link = form.get('facebook_link')
        venue.website = form.get('website')
        venue.image_link = form.get('image_link')
        venue.seeking_talent = bool(form.get('seeking_talent'))
        venue.seeking_description = form.get('seeking_description')
        db.session.commit()
        print(sys.exc_info())
    except:
        db.session.rollback()

    finally:
        db.session.close()
    return redirect(url_for('show_venue', venue_id=venue_id))


#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    # called upon submitting the new artist listing form
    error = False
    form = request.form
    try:
        n_artist = Artist(
            name=form.get('name'),
            city=form.get('city'),
            state=form.get('state'),
            phone=form.get('phone'),
            genres=form.getlist('genres'),
            image_link=form.get('image_link'),
            facebook_link=form.get('facebook_link'),
            seeking_venue=bool(form.get('seeking_venue')),
            seeking_description=form.get('seeking_description')
        )
        db.session.add(n_artist)
        db.session.commit()
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if not error:
        flash('Artist ' + request.form['name'] + ' was successfully listed!')
    else:
        flash('An error occurred. Artist ' +
              request.form['name'] + ' could not be listed.')
    return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    # displays list of shows at /shows
    cur_time = datetime.now()
    show = Show.query.filter(Show.start_time > cur_time).filter(
        (Show.venue_id is not None) and (Show.artist_id is not None)).all()
    data = [{
        "venue_id": v.venue_id,
        "venue_name": Venue.query.get(v.venue_id).name,
        "artist_id": v.artist_id,
        "artist_name": Artist.query.get(v.artist_id).name,
        "artist_image_link": Artist.query.get(v.artist_id).image_link,
        "start_time": str(v.start_time)
    } for v in show]
    return render_template('pages/shows.html', shows=data)


@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    # called to create new shows in the db, upon submitting new show listing form
    error = False
    form = request.form
    try:
        n_show = Show(
            start_time=request.form.get('start_time'),
            venue_id=request.form.get('venue_id'),
            artist_id=request.form.get('artist_id')
        )
        db.session.add(n_show)
        db.session.commit()
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if not error:
        flash('Show was successfully listed!')
    # on successful db insert, flash success
    else:
        flash('An error occurred. Show could not be listed.')

    # e.g., flash('An error occurred. Show could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    return render_template('pages/home.html')


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

# ----------------------------------------------------------------------------#
# Launch.
# ----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
