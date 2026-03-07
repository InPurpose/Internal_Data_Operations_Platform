CREATE DATABASE idop; -- <idop> is the name of database, you can choose your own 
CREATE USER idop_user WITH PASSWORD '123456'; -- <idop_user> is also the username, you can choose your own
GRANT ALL PRIVILEGES ON DATABASE idop TO idop_user; -- make sure dataname <idop> and username <idop_user> match you owns
GRANT ALL ON SCHEMA public TO idop_user; -- make sure username <idop_user> match you owns
ALTER SCHEMA public OWNER TO idop_user; -- make sure username <idop_user> match you owns

-- cheatsheet: https://gist.github.com/Kartones/dd3ff5ec5ea238d4c546
-- select current_database() as database;
-- \l


