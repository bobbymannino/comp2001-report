----------------------------
-----------TABLES-----------
----------------------------
create schema CW2;

create table CW2.users
(
    user_id int primary key identity (1, 1),
    email   varchar(100) not null unique,
    role    varchar(100) not null check (role in ('ADMIN', 'USER'))
);

create table CW2.trails
(
    trail_id       int primary key identity (1, 1),
    author_id      int          not null references CW2.users (user_id),
    name           varchar(100) not null,
    summary        varchar(100) not null,
    description    varchar(max) not null,
    location       varchar(max) not null,
    length         int          not null,
    elevation_gain int          not null,
    route_type     varchar(100) not null
);

create table CW2.features
(
    feature_id int primary key identity (1, 1),
    name       varchar(100) not null
);

create table CW2.trail_features
(
    trail_id   int references CW2.trails (trail_id),
    feature_id int references CW2.features (feature_id),
    primary key (trail_id, feature_id)
);

create table CW2.points
(
    point_id    int primary key identity (1, 1),
    longitude   real not null check (
        longitude >= -180.0
            and longitude <= 180
        ),
    latitude    real not null check (
        latitude >= -90.0
            and latitude <= 90
        ),
    description varchar(max)
);

create table CW2.trail_points
(
    trail_id int references CW2.trails (trail_id),
    point_id int references CW2.points (point_id),
    position int not null,
    primary key (trail_id, point_id)
);

----------------------------
------------SEED------------
----------------------------
insert into CW2.users (email, role)
values ('grace@plymouth.ac.uk', 'ADMIN'),
       ('tim@plymouth.ac.uk', 'ADMIN'),
       ('ada@plymouth.ac.uk', 'ADMIN'),
       ('user@plymouth.ac.uk', 'USER'),
       ('testme@test.com', 'USER');

insert into CW2.trails (author_id,
                        name,
                        summary,
                        description,
                        location,
                        length,
                        elevation_gain,
                        route_type)
values (1,
        'Easy Day Walk',
        'A short and easy walk for beginners',
        'This is a beautiful walk in the woods.',
        'Plymouth, England',
        500,
        100,
        'Day Hike'),
       (2,
        'Challenging Peak Climb',
        'A difficult hike to reach the top of a mountain',
        'The views from the top are breathtaking.',
        'Dartmoor, England',
        1000,
        2000,
        'Peak Climbing'),
       (3,
        'Fun City Walk',
        'A trail created by one of our user accounts',
        'This is just an example trail.',
        'Blackpool, England',
        3000,
        500,
        'Day Hike');

insert into CW2.features (name)
values ('City'),
       ('Fun'),
       ('Short'),
       ('Tiring');

insert into CW2.trail_features (trail_id, feature_id)
values (1, 1),
       (1, 2),
       (1, 3),
       (1, 4),
       (2, 1),
       (2, 4),
       (3, 2),
       (3, 1);

insert into CW2.points (longitude, latitude, description)
values (30.0, 30.0, 'Nice Mountain'),
       (31.0, 31.0, 'Cold River'),
       (32.0, 32.0, 'Big Forest'),
       (33.0, 33.0, 'City Centre'),
       (34.0, 34.0, 'Beach'),
       (35.0, 35.0, 'Park'),
       (36.0, 36.0, 'Lake'),
       (37.0, 37.0, 'Hill'),
       (38.0, 38.0, 'Valley'),
       (39.0, 39.0, 'Cave');

insert into CW2.trail_points (trail_id, point_id, position)
values (1, 1, 1),
       (1, 2, 2),
       (1, 3, 3),
       (2, 4, 1),
       (2, 5, 2),
       (2, 6, 3),
       (3, 4, 1),
       (3, 5, 2),
       (3, 6, 3),
       (3, 3, 4),
       (3, 10, 5),
       (3, 9, 6);