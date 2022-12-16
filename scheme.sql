-- drop table if exists users;
-- create table users (
--     id integer primary key autoincrement,
--     telegram_uid int not null,
--     nickname text not null,
--     balance int not null,
--     chat_state int not null,
--     game_id int not null,
--     games_num int not null,
--     wins_num int not null
-- );

delete from users where nickname='kefir';
-- update users set nickname='ked2006' where nickname='Доманин'


-- update users set balance = 100000000000 where nickname='kefir'