insert into CW2.users (username, first_name, last_name, email, password, is_admin) values
    ('graceh', 'Grace', 'Hopper', 'grace@plymouth.ac.uk', 'ISAD123!', 1),
    ('tbl', 'Tim', 'Berners-Lee', 'tim@plymouth.ac.uk', 'COMP2001!', 1),
    ('adal', 'Ada', 'Lovelace', 'ada@plymouth.ac.uk', 'insecurePassword', 1),
    ('testi', 'Bob', 'Lucee', 'december@gmail.com', 'password', 0),
    ('besti', 'Joe', 'Ward', 'seventies@yahoo.co.uk', 'password', 0);

insert into CW2.trail_locations (title)
values ('Plymouth'),
       ('England'),
       ('Devon'),
       ('Exeter'),
       ('Dartmoor');

insert into CW2.trails (user_id, title, description, elevation, length, route_type, city_id, county_id, country_id)
values (1, 'Plymouth Something Trail',
        'Do deserunt est eut labore laborum dolore. Commodo officia sunt dolor dolore consequat. um commodo nostrud deserunt nostrud.',
        125, 1500, 'Loop', 1, 3, 2),
        (2, 'Dartmoor Round',
        'Commodo officia sunt dolor dolore consequat. Aute anim deserunt occaecat reprehlpa labore.',
        100, 1000, 'Loop', 5, 3, 2),
       (2, 'Exeter Coast',
        'Commodo officia sunt dolor dolore consequat. Aute anim deserunt occaecat reprehlpa labore.',
        50, 800, 'Straight', 5, 3, 1);

insert into CW2.trail_points (trail_id, pos, longitude, latitude)
values (1, 1, 30.1, 20.005),
       (1, 2, 30.2, 20.005),
       (1, 3, 30.3, 20.005),
       (2, 1, 30.4, 20.005),
       (2, 2, 30.5, 20.005),
       (2, 3, 30.6, 20.005),
       (3, 1, 130.2, 2.005),
       (3, 2, 130.3, 2.005),
       (3, 3, 130.4, 2.005),
       (4, 1, 130.5, 2.005),
       (4, 2, 130.6, 2.005);