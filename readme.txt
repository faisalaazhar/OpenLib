OpenLib. Online library management system. User can borrow and return a book. User can create, update and delete a blog post.

Web Framework Django is used with two databases oracle and mongodb.

Steps to run this application:
terminal commands are written after two dash.

Step: 1
Open VS Code
Create virtual environment in the folder that contains the project directory
-- python -m venv venv
Activate virtual env
-- venv/scripts/activate

install requirement.txt modules
--pip install -r requirements.txt

Step: 2
Create a database user for the project
SQL Commands:
----command start
create tablespace openlib_tablespace datafile 'openlib_tablespace.dat' size 10M autoextend on;

create temporary tablespace openlib_tablespace_temp tempfile 'openlib_tablespace_temp.dat' size 5M autoextend on;

create user openlib identified by openlib default tablespace openlib_tablespace temporary tablespace openlib_tablespace_temp;

grant create session to openlib;
grant create table to openlib;
grant unlimited tablespace to openlib;

GRANT CONNECT, RESOURCE, CREATE VIEW, CREATE MATERIALIZED VIEW, 
CREATE PUBLIC SYNONYM TO openlib WITH ADMIN OPTION;

GRANT ALTER ANY ROLE, ALTER ANY SEQUENCE, ALTER ANY TABLE, 
ALTER TABLESPACE, ALTER ANY TRIGGER , COMMENT ANY TABLE, 
CREATE ANY SEQUENCE, CREATE ANY TABLE, CREATE ANY TRIGGER , 
CREATE ROLE, CREATE TABLESPACE, CREATE USER, DROP ANY SEQUENCE, 
DROP ANY TABLE, DROP ANY TRIGGER , DROP TABLESPACE, DROP USER, 
DROP ANY ROLE, GRANT ANY ROLE, INSERT ANY TABLE, SELECT ANY TABLE,
UPDATE ANY TABLE TO openlib;

commit;
----command finish

Create a new connection with the user created and create table, sequence, procedure, function, trigger from project report.

All SQL Commands are available on OpenLib.sql file. 
Run the file in sql in database.

Step: 3
Now migrate models from django into database from terminal

-- cd openlib
-- py manage.py migrate

Run server to view ui/ux
-- py manage.py runserver


Step: 4
Follow the link
http://127.0.0.1:8000/

Then go through the webpages