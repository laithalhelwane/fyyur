-- Vanues Data
Insert INTO
    "Venue"(
        name,
        genres,
        address,
        city,
        state,
        phone,
        website,
        facebook_link,
        seeking_talent,
        seeking_description,
        image_link
    )
VALUES
    (
        'The Dueling Pianos Bar',
        'Classical',
        '335 Delancey Street',
        'New York',
        'NY',
        '914-003-1132',
        'https://www.theduelingpianos.com',
        'https://www.facebook.com/theduelingpianos',
        False,
        '',
        'https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80'
    );

Insert INTO
    "Venue"(
        name,
        genres,
        address,
        city,
        state,
        phone,
        website,
        facebook_link,
        seeking_talent,
        seeking_description,
        image_link
    )
VALUES
    (
        'The Musical Hop',
        'Jazz',
        '1015 Folsom Street',
        'San Francisco',
        'CA',
        '123-123-1234',
        'https://www.themusicalhop.com',
        'https://www.facebook.com/TheMusicalHop',
        True,
        'We are on the lookout for a local artist to play every two weeks. Please call us.',
        'https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60'
    );

Insert INTO
    "Venue"(
        name,
        genres,
        address,
        city,
        state,
        phone,
        website,
        facebook_link,
        seeking_talent,
        seeking_description,
        image_link
    )
VALUES
    (
        'Park Square Live Music & Coffee',
        'Folk',
        '34 Whiskey Moore Ave',
        'San Francisco',
        'CA',
        '415-000-1234',
        'https://www.parksquarelivemusicandcoffee.com',
        'https://www.facebook.com/ParkSquareLiveMusicAndCoffee',
        False,
        '',
        'https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80'
    );

-- Artist Data
Insert INTO
    "Artist"(
        name,
        genres,
        city,
        state,
        phone,
        website,
        facebook_link,
        seeking_venue,
        seeking_description,
        image_link
    )
VALUES
    (
        'Guns N Petals',
        'Rock n Roll',
        'San Francisco',
        'CA',
        '326-123-5000',
        'https://www.gunsnpetalsband.com',
        'https://www.facebook.com/GunsNPetals',
        True,
        'Looking for shows to perform at in the San Francisco Bay Area!',
        'https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80'
    );

Insert INTO
    "Artist"(
        name,
        genres,
        city,
        state,
        phone,
        website,
        facebook_link,
        seeking_venue,
        seeking_description,
        image_link
    )
VALUES
    (
        'Matt Quevedo',
        'Jazz',
        'New York',
        'NY',
        '300-400-5000',
        '',
        'https://www.facebook.com/mattquevedo923251523',
        False,
        '',
        'https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80'
    );

Insert INTO
    "Artist"(
        name,
        genres,
        city,
        state,
        phone,
        website,
        facebook_link,
        seeking_venue,
        seeking_description,
        image_link
    )
VALUES
    (
        'The Wild Sax Band',
        'Classical',
        'San Francisco',
        'CA',
        '432-325-5432',
        '',
        '',
        False,
        '',
        'https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80'
    );

-- Shows
INSERT INTO
    "Show"(venue_id, artist_id, start_time)
VALUES
    (2, 1, '2019-05-21T21:30:00.000Z');

INSERT INTO
    "Show"(venue_id, artist_id, start_time)
VALUES
    (3, 2, '2019-06-15T23:00:00.000Z');

INSERT INTO
    "Show"(venue_id, artist_id, start_time)
VALUES
    (3, 3, '2035-04-01T20:00:00.000Z');

INSERT INTO
    "Show"(venue_id, artist_id, start_time)
VALUES
    (3, 3, '2035-04-08T20:00:00.000Z');

INSERT INTO
    "Show"(venue_id, artist_id, start_time)
VALUES
    (3, 3, '2035-04-15T20:00:00.000Z');