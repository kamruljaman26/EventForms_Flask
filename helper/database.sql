CREATE DATABASE eventforms;

-- insert into admin
INSERT INTO admin(name,email,password) VALUES ('Kamrul Jaman','k@gmail.cim','1234');


-- Insert into session
INSERT INTO session(session_id,session_name,session_date,session_time,seat_booked)
VALUES ('26NOV01','Session 1','2020-11-26','11:00:00',0);
INSERT INTO session(session_id,session_name,session_date,session_time,seat_booked)
VALUES ('26NOV02','Session 2','2020-11-26','12:00:00',0);
INSERT INTO session(session_id,session_name,session_date,session_time,seat_booked)
VALUES ('26NOV03','Session 3','2020-11-26','13:00:00',0);
INSERT INTO session(session_id,session_name,session_date,session_time,seat_booked)
VALUES ('26NOV04','Session 4','2020-11-26','14:00:00',0);

INSERT INTO session(session_id,session_name,session_date,session_time,seat_booked)
VALUES ('27NOV01','Session 1','2020-11-27','11:00:00',0);
INSERT INTO session(session_id,session_name,session_date,session_time,seat_booked)
VALUES ('27NOV02','Session 2','2020-11-27','12:00:00',0);
INSERT INTO session(session_id,session_name,session_date,session_time,seat_booked)
VALUES ('27NOV03','Session 3','2020-11-27','13:00:00',0);
INSERT INTO session(session_id,session_name,session_date,session_time,seat_booked)
VALUES ('27NOV04','Session 4','2020-11-27','14:00:00',0);

-- Insert into registration
