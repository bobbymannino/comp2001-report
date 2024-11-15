-- TODO create views
-- TODO refine procedures

create schema CW2;

create table CW2.users
(
    user_id    int primary key identity (1, 1),
    username   varchar(16)  not null unique check (len(username) > 2),
    first_name varchar(24),
    last_name  varchar(24),
    email      varchar(50)  not null unique,
    password   varchar(max) not null,
    is_admin   bit          not null default 0,
    created_at datetime     not null default getdate()
);

create table CW2.trail_locations
(
    location_id int primary key identity (1, 1),
    title       varchar(50) not null
);

create table CW2.trails
(
    trail_id    int primary key identity (1, 1),
    user_id     int          not null references CW2.users (user_id),
    title       varchar(50)  not null,
    description varchar(max) not null,
    elevation   smallint     not null,
    length      smallint     not null,
    route_type  varchar(25)  not null,
    city_id     int          not null references CW2.trail_locations (location_id),
    county_id   int          not null references CW2.trail_locations (location_id),
    country_id  int          not null references CW2.trail_locations (location_id),
    created_at  datetime     not null default getdate()
);

create table CW2.trail_points
(
    trail_id  int references CW2.trails (trail_id),
    pos       smallint not null check (pos > 0),
    longitude real     not null check (longitude >= -180.0 and longitude <= 180),
    latitude  real     not null check (latitude >= -90.0 and latitude <= 90),
    primary key (trail_id, pos)
);

create table CW2.trail_logs
(
    id         int primary key identity (1,1),
    user_id    int        not null references CW2.users (user_id),
    trail_id   int        not null references CW2.trails (trail_id),
    action     varchar(6) not null, -- this will be either "create" or "update"
    created_at datetime   not null default getdate()
);

----------------------------
----------TRIGGERS----------
----------------------------

-- Trigger for when new trails are created
create trigger CW2.log_new_trail_trigger
    on CW2.trails
    for insert
    as
begin
    insert into CW2.trail_logs (user_id, trail_id, action)
    values ((select user_id from inserted), (select trail_id from inserted), 'create');
end;

-- Trigger for when existing trails are edited
    create trigger CW2.log_existing_trail_trigger
        on CW2.trails
        for update
        as
    begin
        insert into CW2.trail_logs (user_id, trail_id, action)
        values ((select user_id from inserted), (select trail_id from inserted), 'update');
    end;

----------------------------
-----------VIEWS------------
----------------------------

create view CW2.trail_view as
    select t.title from CW2.trails t
        join CW2.trail_points tp on tp.trail_id = t.trail_id
        join CW2.trail_locations tl on tl.location_id in (t.country_id, t.county_id, t.city_id);