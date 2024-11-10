insert into CW1.users (username, first_name, last_name, password, is_admin)
values ('lucy22', 'Lucy', 'Ward', 'lucystar', 1),
       ('bob28', 'Bobby', 'Mannino', 'church', 1);


insert into CW1.trail_locations (title)
values ('Plymouth'),
       ('England'),
       ('Devon'),
       ('Exeter'),
       ('Dartmoor');

insert into CW1.trails (user_id, title, description, elevation, length, route_type, city_id, county_id, country_id)
values (1, 'Plymouth Something Trail',
        'Do deserunt est eut labore laborum dolore. Commodo officia sunt dolor dolore consequat. um commodo nostrud deserunt nostrud.',
        125, 1500, 'Loop', 1, 3, 2);

insert into CW1.trails (user_id, title, description, elevation, length, route_type, city_id, county_id, country_id)
values (2, 'Dartmoor Round',
        'Commodo officia sunt dolor dolore consequat. Aute anim deserunt occaecat reprehlpa labore.',
        100, 1000, 'Loop', 5, 3, 2);

insert into CW1.trail_points (trail_id, [order], longitude, latitude)
values (7, 1, 30.1, 20.005),
       (7, 2, 30.2, 20.005),
       (7, 3, 30.3, 20.005),
       (7, 4, 30.4, 20.005),
       (7, 5, 30.5, 20.005),
       (7, 6, 30.6, 20.005),
       (8, 1, 130.2, 2.005),
       (8, 2, 130.3, 2.005),
       (8, 3, 130.4, 2.005),
       (8, 4, 130.5, 2.005),
       (8, 5, 130.6, 2.005);