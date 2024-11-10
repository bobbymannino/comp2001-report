create or alter procedure new_trail_point(@trail_id int, @long float, @lat float) as
begin
    insert into CW1.trail_points(trail_id, [order], longitude, latitude)
    values (@trail_id, ((select count(*) from CW1.trail_points where trail_id = @trail_id) + 1), @long, @lat);
end;

    exec new_trail_point 1, 45.0, 45.0;
    select * from CW1.trail_points where trail_id = 1;

    create procedure delete_trail_location(@location_id int) as
    begin
        delete from CW1.trail_locations where location_id = @location_id;
    end;

        exec delete_trail_location 4
    select *
    from CW1.trail_locations;

        create procedure update_trail_location(@location_id int, @new_title varchar(25)) as
        begin
            update CW1.trail_locations
            set title = @new_title
            where location_id = @location_id;
        end;

            exec update_trail_location 1, 'New title';

        select *
        from CW1.trail_locations;

            create procedure read_trails_from_city(@city_id int) as
            begin
                select *
                from CW1.trails
                where city_id = @city_id;
            end;

                exec read_trails_from_city 1