----Creating a user for django application----

--logged in as system user

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

--logged in as openlib

--book table
CREATE TABLE book(
	book_id number,
	title varchar2(100) NOT NULL,
	publisher varchar2(200) NOT NULL,
	author varchar2(100) NOT NULL,
	cover_photo varchar2(100),
	category varchar2(200),
	num_of_copies number NOT NULL,
	num_of_pages number NOT NULL,
	price number(10,3),
	book_description varchar2(3999),
	PRIMARY KEY (book_id)
);

--borrow_book table
CREATE TABLE borrow_book(
	borrow_id number,
	user_id number,
	book_id number,
	date_borrowed date NOT NULL,
	date_returned date,
	PRIMARY KEY (borrow_id),
	CONSTRAINT FK_USER FOREIGN KEY (user_id) REFERENCES auth_user(id),
	CONSTRAINT FK_BOOK FOREIGN KEY (book_id) REFERENCES book(book_id)
);

--book_transaction table
CREATE TABLE book_transaction(
	book_transaction_id number,
	borrow_id number,
	borrow_cost number(10,3),
	fines number(10,3),
	PRIMARY KEY (book_transaction_id),
	CONSTRAINT FK_borrow FOREIGN KEY (borrow_id) REFERENCES borrow_book(borrow_id)
);

--function calc_borrow_cost
CREATE OR REPLACE FUNCTION calc_borrow_cost(cost NUMBER) 
RETURN NUMBER IS     
borrow_cost NUMBER; 
BEGIN     
    IF cost > 500 THEN 
        borrow_cost := cost*0.1;
        RETURN borrow_cost;
    ELSIF cost < 500 THEN
        borrow_cost := cost*0.05;
        RETURN borrow_cost;
    END IF;
END;

--function is_friday
CREATE OR REPLACE FUNCTION is_friday
RETURN BOOLEAN IS   
day_c VARCHAR2(20); 
BEGIN     
    day_c := TO_CHAR(SYSDATE, 'DAY');
    IF day_c = 'FRIDAY' THEN
        RETURN TRUE;
    ELSE
        RETURN FALSE;
    END IF;
END;

--function stock_count 
create or replace FUNCTION stock_count(b_id number) return number IS 
stk_count NUMBER;
BEGIN     
    SELECT num_of_copies INTO stk_count
    FROM book 
    where book_id=b_id;
    return stk_count;
END;

--procedure insert_book_transaction
CREATE OR REPLACE PROCEDURE insert_book_transaction(u_id NUMBER, b_id NUMBER) IS
borrow_cost NUMBER;
price_of_book NUMBER;
borrow_id NUMBER := seq_book.NEXTVAL;
BEGIN
    SELECT price into price_of_book from book where book_id=b_id;
    borrow_cost := calc_borrow_cost(price_of_book);
    
    insert into borrow_book (borrow_id, user_id, book_id, date_borrowed) values (borrow_id, u_id, b_id, sysdate);
    
    insert into book_transaction (book_transaction_id, borrow_id, borrow_cost, total_cost) values (book_tr_num.NEXTVAL, borrow_id, borrow_cost, borrow_cost);
END;

-- procedure return_book

CREATE OR REPLACE PROCEDURE return_book(b_id NUMBER) IS
bor_cost NUMBER;
calc_fines NUMBER;
total_amount NUMBER;
diff NUMBER;
BEGIN
    UPDATE borrow_book
    SET date_returned = sysdate
    WHERE borrow_id = b_id;
    
    select trunc(date_returned - date_borrowed) into diff
    from borrow_book where borrow_id=b_id;
    
    select borrow_cost into bor_cost
    from book_transaction where borrow_id=b_id;
    
    if diff > 21 then
        calc_fines := (diff-21)*5;
    else
        calc_fines := 0;
    end if;
    total_amount := bor_cost+calc_fines;
    
    UPDATE book_transaction
    SET fines = calc_fines, total_cost = total_amount
    WHERE borrow_id = b_id;
    
END;

---trigger dec_book_copies 
CREATE OR REPLACE TRIGGER dec_book_copies
  AFTER INSERT ON borrow_book
  FOR EACH ROW
BEGIN
    UPDATE book
    SET num_of_copies = (num_of_copies-1)
    WHERE book_id = :new.book_id;
END;

---trigger inc_book_copies 
CREATE OR REPLACE TRIGGER inc_book_copies
  AFTER UPDATE ON borrow_book
  FOR EACH ROW
BEGIN
    UPDATE book
    SET num_of_copies = (num_of_copies+1)
    WHERE book_id = :new.book_id;
END;