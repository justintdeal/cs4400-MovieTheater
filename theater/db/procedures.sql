USE `team50`;

DROP VIEW IF EXISTS scheduled_movies;
CREATE VIEW scheduled_movies
AS SELECT t.manager as manager, t.street as street, t.city as city, t.state as state, t.zipcode as zipcode,
t.name as theater, t.company as company, mP.movie as movie, mP.releaseDate as releaseDate, mP.date as date, m.duration as duration
FROM theater AS t, moviePlay AS mP, movie as m
WHERE (t.name = mP.theater) AND 
(t.company = mP.company) AND
(mP.movie = m.name) AND 
(mP.releaseDate = m.release);

DROP VIEW IF EXISTS visited_theaters;
CREATE VIEW visited_theaters
AS SELECT v.username, v.theater, v.company, v.date, t.street, t.city, t.state, t.zipcode
FROM visit AS v, theater AS t
WHERE (t.company = v.company) AND
(t.name = v.theater);

DROP VIEW IF EXISTS cust_cc_count;
CREATE VIEW cust_cc_count
AS SELECT username, count(*) AS creditCardCount, status 
FROM user NATURAL JOIN creditCard
GROUP BY username;

DROP FUNCTION IF EXISTS num_emp;
DELIMITER $$
CREATE FUNCTION `num_emp` (i_compName VARCHAR(50))
	RETURNS INT
    DETERMINISTIC
    READS SQL DATA
BEGIN
	RETURN (Select count(*) from `manager` where company = i_compName);
END$$ 
DELIMITER ;

DROP FUNCTION IF EXISTS num_movie_scheduled;
DELIMITER $$
CREATE FUNCTION `num_movie_scheduled` (i_thName VARCHAR(50), i_compName VARCHAR(50), i_movPlayDate DATE)
	RETURNS INT
    DETERMINISTIC
    READS SQL DATA
BEGIN
	RETURN (Select count(*) from `scheduled_movies` where (company = i_compName) and (theater = i_thName) and (date = i_movPlayDate));
END$$ 
DELIMITER ;
 
DROP FUNCTION IF EXISTS get_type;
DELIMITER $$
CREATE FUNCTION `get_type` (i_username VARCHAR(50))
	RETURNS VARCHAR(50)
    DETERMINISTIC
    READS SQL DATA
BEGIN
	IF (is_Customer(i_username) = 1 and is_Manager(i_username) = 1) THEN
		RETURN 'CustomerManager';
	elseIF (is_Customer(i_username) = 1 and is_Admin(i_username) = 1) THEN
		RETURN 'CustomerAdmin';
	elseIF (is_Customer(i_username) = 1) THEN
		RETURN 'Customer';
	elseIF (is_Manager(i_username) = 1) THEN
		RETURN 'Manager';
	elseIF (is_Admin(i_username) = 1) THEN
		RETURN 'Admin';
	else
		RETURN 'User';
    END IF;
END$$ 
DELIMITER ;
 
DROP FUNCTION IF EXISTS is_Customer;
DELIMITER $$
CREATE FUNCTION `is_Customer` (i_username VARCHAR(50))
	RETURNS INT
    DETERMINISTIC
    READS SQL DATA
BEGIN
	RETURN EXISTS(Select * from `customer` where username = i_username);
END$$ 
DELIMITER ;
 
DROP FUNCTION IF EXISTS is_Manager;
DELIMITER $$
CREATE FUNCTION `is_Manager` (i_username VARCHAR(50))
	RETURNS INT
    DETERMINISTIC
    READS SQL DATA
BEGIN 
	RETURN EXISTS(Select * from `manager` where username = i_username);
END$$ 
DELIMITER ;
 
DROP FUNCTION IF EXISTS is_Admin;
DELIMITER $$
CREATE FUNCTION `is_Admin` (i_username VARCHAR(50))
	RETURNS INT
    DETERMINISTIC
    READS SQL DATA
BEGIN
	RETURN EXISTS(Select * from `admin` where username = i_username);
END$$ 
DELIMITER ;

-- 1 
DROP PROCEDURE IF EXISTS user_login;
DELIMITER $$
CREATE PROCEDURE `user_login`(IN i_username VARCHAR(50), IN i_password VARCHAR(50))
BEGIN
	DROP TABLE IF EXISTS UserLogin;
    CREATE TABLE UserLogin
		SELECT username, status, is_Customer(i_username) as isCustomer, is_Admin(i_username) as isAdmin, is_Manager(i_username) as isManager
		FROM user
        where i_username = username and md5(i_password) = password;
END$$
DELIMITER ;

-- 3
DROP PROCEDURE IF EXISTS user_register;
DELIMITER $$
CREATE PROCEDURE `user_register`(IN i_username VARCHAR(50), IN i_password VARCHAR(50), 
IN i_firstname VARCHAR(50), IN i_lastname VARCHAR(50))
BEGIN
	INSERT INTO user (username, password, firstname, lastname) VALUES
	(i_username, MD5(i_password), i_firstname, i_lastname);
END$$
DELIMITER ;
 
-- 4a
DROP PROCEDURE IF EXISTS customer_only_register;
DELIMITER $$
CREATE PROCEDURE `customer_only_register`(IN i_username VARCHAR(50), IN i_password VARCHAR(50), 
IN i_firstname VARCHAR(50), IN i_lastname VARCHAR(50))
BEGIN
	INSERT INTO user (username, password, firstname, lastname) VALUES
	(i_username, MD5(i_password), i_firstname, i_lastname);
    INSERT INTO customer (username) VALUES
    (i_username);
END$$
DELIMITER ;
 
-- 4b
DROP PROCEDURE IF EXISTS customer_add_creditcard;
DELIMITER $$
CREATE PROCEDURE `customer_add_creditcard`(IN i_username VARCHAR(50), IN i_creditCardNum CHAR(16))
BEGIN
	INSERT INTO creditCard (username, creditCardNum) VALUES
	(i_username, cc_num);
END$$
DELIMITER ;
 
-- 5
DROP PROCEDURE IF EXISTS manager_only_register;
DELIMITER $$
CREATE PROCEDURE `manager_only_register`(IN i_username VARCHAR(50), IN i_password VARCHAR(50), 
IN i_firstname VARCHAR(50), IN i_lastname VARCHAR(50), IN i_comName VARCHAR(50),
IN i_empStreet VARCHAR(50), IN i_empCity VARCHAR(50), IN i_empState CHAR(2), IN i_empZipcode CHAR(5))
BEGIN
	INSERT INTO user (username, password, firstname, lastname) VALUES
	(i_username, MD5(i_password), i_firstname, i_lastname);
    INSERT INTO employee (username) VALUES
    (i_username);
	INSERT INTO manager (username, company, street, city, state, zipcode) VALUES
	(i_username, i_comName, i_empStreet, i_empCity, i_empState, i_empZipcode);
END$$
DELIMITER ;
 
-- 6a
DROP PROCEDURE IF EXISTS manager_customer_register;
DELIMITER $$
CREATE PROCEDURE `manager_customer_register`(IN i_username VARCHAR(50), IN i_password VARCHAR(50), 
IN i_firstname VARCHAR(50), IN i_lastname VARCHAR(50), IN i_comName VARCHAR(50),
IN i_empStreet VARCHAR(50), IN i_empCity VARCHAR(50), IN i_empState CHAR(2), IN i_empZipcode CHAR(5))
BEGIN
	INSERT INTO user (username, password, firstname, lastname) VALUES
	(i_username, MD5(i_password), i_firstname, i_lastname);
    INSERT INTO employee (username) VALUES
    (i_username);
    INSERT INTO manager (username, company, street, city, state, zipcode) VALUES
	(i_username, i_comName, i_empStreet, i_empCity, i_empState, i_empZipcode);
    INSERT INTO customer (username) VALUES
    (i_username);
END$$
DELIMITER ;
 
-- 6b
DROP PROCEDURE IF EXISTS manager_customer_add_creditcard;
DELIMITER $$
CREATE PROCEDURE `manager_customer_add_creditcard`(IN i_username VARCHAR(50), IN i_creditCardNum CHAR(16))
BEGIN
	INSERT INTO creditCard (username, creditCardNum) VALUES
	(i_username, cc_num);
END$$
DELIMITER ;
 
-- 13a
DROP PROCEDURE IF EXISTS admin_approve_user;
DELIMITER $$
CREATE PROCEDURE `admin_approve_user`(IN i_username VARCHAR(50))
BEGIN
	update user
	set status = 'Approved'
	where username = i_username;
END$$
DELIMITER ;
 
-- 13b
DROP PROCEDURE IF EXISTS admin_decline_user;
DELIMITER $$
CREATE PROCEDURE `admin_decline_user`(IN i_username VARCHAR(50))
BEGIN
-- cannot alter an approved user
	update user
	set status = 'Declined'
	where username = i_username and not status = 'Approved';
END$$
DELIMITER ;
 
-- 13c
DROP PROCEDURE IF EXISTS admin_filter_user;
DELIMITER $$
CREATE PROCEDURE `admin_filter_user`(IN i_username VARCHAR(50), IN i_status ENUM('Pending','Approved','Declined','ALL'), 
IN i_sortBy ENUM('username','creditCardCount','userType','status', ''), IN i_sortDirection ENUM('ASC','DESC', ''))
BEGIN
	DROP TABLE IF EXISTS AdFilterUser;
	CREATE TABLE AdFilterUser
	SELECT username, creditCardCount, get_type(username) as userType, status
	FROM cust_cc_count 
		WHERE (username = i_username OR i_username = '') AND
		(status = i_status OR i_status = "ALL")
	UNION
    SELECT username, 0 as creditCardCount, get_type(username) as userType, status
    FROM user
		WHERE (username NOT IN (select username from cust_cc_count)) AND
        (username = i_username OR i_username = '') AND
		(status = i_status OR i_status = "ALL")
	GROUP BY username
	ORDER BY 
        case when i_sortBy = '' and (i_sortDirection = '' or i_sortDirection = 'DESC') then username end DESC,
        case when i_sortBy = "username" and (i_sortDirection = '' or i_sortDirection = 'DESC') then username end DESC,
        case when i_sortBy = "creditCardCount" and (i_sortDirection = '' or i_sortDirection = 'DESC') then creditCardCount end DESC,
        case when i_sortBy = "userType" and (i_sortDirection = '' or i_sortDirection = 'DESC') then userType end DESC,
        case when i_sortBy = "status" and (i_sortDirection = '' or i_sortDirection = 'DESC') then status end DESC,
        case when i_sortBy = '' and i_sortDirection = 'ASC' then username end ASC,
        case when i_sortBy = "username" and i_sortDirection = 'ASC' then username end ASC,
        case when i_sortBy = "creditCardCount" and i_sortDirection = 'ASC' then creditCardCount end ASC,
        case when i_sortBy = "userType" and i_sortDirection = 'ASC' then userType end ASC,
        case when i_sortBy = "status" and i_sortDirection = 'ASC' then status end ASC;
END$$
DELIMITER ;
 
-- 14
DROP PROCEDURE IF EXISTS admin_filter_company;
DELIMITER $$
CREATE PROCEDURE `admin_filter_company`(IN i_comName VARCHAR(50), 
IN i_minCity INT, IN i_maxCity INT, IN i_minTheater INT, IN i_maxTheater INT,
IN i_minEmployee INT, IN i_maxEmployee INT,
IN i_sortBy ENUM('comName','numCityCover','numTheater','numEmployee', ''),
IN i_sortDirection ENUM('ASC','DESC', ''))
BEGIN
    DROP TABLE IF EXISTS AdFilterCom;
    CREATE TABLE AdFilterCom
    SELECT c.name as comName, count(distinct concat(t.city,t.state)) as numCityCover, count(t.name) as numTheater, num_emp(c.name) as numEmployee
    FROM company as c right outer join theater as t on (t.company = c.name)
    WHERE (c.name = i_comName or i_comName = 'ALL')
    GROUP BY comName
    HAVING (i_minCity IS NULL or i_maxCity IS NULL or numCityCover >= i_minCity and numCityCover <= i_maxCity) and
    (i_minTheater IS NULL or i_maxTheater IS NULL or numTheater >= i_minTheater and numTheater <= i_maxTheater) and
    (i_minEmployee IS NULL or i_maxEmployee IS NULL or numEmployee >= i_minEmployee and numEmployee <= i_maxEmployee)
    ORDER BY 
        case when i_sortBy = '' and (i_sortDirection = '' or i_sortDirection = 'DESC') then comName end DESC,
        case when i_sortBy = "comName" and (i_sortDirection = '' or i_sortDirection = 'DESC') then comName end DESC,
        case when i_sortBy = "numCityCover" and (i_sortDirection = '' or i_sortDirection = 'DESC') then numCityCover end DESC,
        case when i_sortBy = "numTheater" and (i_sortDirection = '' or i_sortDirection = 'DESC') then numTheater end DESC,
        case when i_sortBy = "numEmployee" and (i_sortDirection = '' or i_sortDirection = 'DESC') then numEmployee end DESC,
        case when i_sortBy = '' and i_sortDirection = 'ASC' then comName end ASC,
        case when i_sortBy = "comName" and i_sortDirection = 'ASC' then comName end ASC,
        case when i_sortBy = "numCityCover" and i_sortDirection = 'ASC' then numCityCover end ASC,
        case when i_sortBy = "numTheater" and i_sortDirection = 'ASC' then numTheater end ASC,
        case when i_sortBy = "numEmployee" and i_sortDirection = 'ASC' then numEmployee end ASC;
END$$
DELIMITER ;
 
-- 15
DROP PROCEDURE IF EXISTS admin_create_theater;
DELIMITER $$
CREATE PROCEDURE `admin_create_theater`(IN i_thName VARCHAR(50),
IN i_comName VARCHAR(50), IN i_thStreet VARCHAR(50), IN i_thCity VARCHAR(50),
IN i_thState CHAR(2), IN i_thZipcode VARCHAR(50), IN i_capacity INT,
IN i_managerUsername VARCHAR(50))
BEGIN
	INSERT INTO theater (company, name, street, city, state, zipcode, capacity, manager)
    VALUES (i_comName, i_thName, i_thStreet, i_thCity, i_thState, i_thZipcode, i_capacity, i_managerUsername);
END$$
DELIMITER ;
 
-- 16a
DROP PROCEDURE IF EXISTS admin_view_comDetail_emp;
DELIMITER $$
CREATE PROCEDURE `admin_view_comDetail_emp`(IN i_comName VARCHAR(50))
BEGIN
	DROP TABLE IF EXISTS AdComDetailEmp;
    CREATE TABLE AdComDetailEmp
		SELECT firstname as empFirstname, lastname as empLastName
		FROM user natural join manager
        where i_comName = company;
END$$
DELIMITER ;
 
-- 16b
DROP PROCEDURE IF EXISTS admin_view_comDetail_th;
DELIMITER $$
CREATE PROCEDURE `admin_view_comDetail_th`(IN i_comName VARCHAR(50))
BEGIN
	DROP TABLE IF EXISTS AdComDetailTh;
    CREATE TABLE AdComDetailTh
		SELECT name as thName, manager as thManagerUsername, city as thCity, state as thState, capacity as thCapacity
		FROM theater
        where i_comName = company;
END$$
DELIMITER ;
 
-- 17
DROP PROCEDURE IF EXISTS admin_create_movie;
DELIMITER $$
CREATE PROCEDURE `admin_create_movie`(IN i_movName VARCHAR(50), IN i_movDuration INT, IN i_movReleaseDate DATE)
BEGIN
	INSERT INTO movie
    VALUES (i_movName, i_movReleaseDate, i_movDuration);
END$$
DELIMITER ;

-- 18
DROP PROCEDURE IF EXISTS manager_filter_th;
DELIMITER $$
CREATE PROCEDURE `manager_filter_th`(IN i_manUsername VARCHAR(50), IN i_movName VARCHAR(50),
IN i_minMovDuration INT, IN i_maxMovDuration INT, IN i_minMovReleaseDate DATE, IN i_maxMovReleaseDate DATE,
IN i_minMovPlayDate DATE, IN i_maxMovPlayDate DATE, IN i_includeNotPlayed BOOLEAN)
BEGIN
	DROP TABLE IF EXISTS ManFilterTh;
	CREATE TABLE ManFilterTh
	SELECT movie as movName, duration as movDuration, releaseDate as movReleaseDate, date as movPlayDate
	FROM scheduled_movies
 	WHERE (manager = i_manUsername) AND
	(i_movName = "" OR LOCATE(i_movName, movie)>0) AND
	(i_minMovPlayDate IS NULL OR date >= i_minMovPlayDate) AND
	(i_maxMovPlayDate IS NULL OR date <= i_maxMovPlayDate) AND
	(i_minMovReleaseDate IS NULL OR date >= i_minMovReleaseDate) AND
	(i_maxMovReleaseDate IS NULL OR date <= i_maxMovReleaseDate) AND
	(i_minMovDuration IS NULL OR duration >= i_minMovDuration) AND
	(i_maxMovDuration IS NULL OR duration <= i_maxMovDuration) AND
    (i_includeNotPlayed = FALSE OR i_includeNotPlayed IS NULL)
    UNION
    SELECT name as movName, duration as movDuration, movie.release as movReleaseDate, NULL as movPlayDate
    FROM movie
    WHERE (concat(movie.name,movie.release) NOT IN (SELECT concat(movie,releaseDate) FROM scheduled_movies WHERE manager = i_manUsername)) AND
    (i_movName = "" OR LOCATE(i_movName, name)>0) AND
	(i_minMovReleaseDate IS NULL OR movie.release >= i_minMovReleaseDate) AND
	(i_maxMovReleaseDate IS NULL OR movie.release <= i_maxMovReleaseDate);    

END$$
DELIMITER ;

-- 19
DROP PROCEDURE IF EXISTS manager_schedule_mov; 
DELIMITER $$
CREATE PROCEDURE `manager_schedule_mov`(IN i_manUsername VARCHAR(50), IN i_movName VARCHAR(50),
IN i_movReleaseDate DATE, IN i_movPlayDate DATE)
BEGIN
	INSERT INTO moviePlay VALUES (i_movName, i_movReleaseDate,
    (SELECT name FROM theater WHERE manager=i_manUsername), 
    (SELECT company FROM theater WHERE manager=i_manUsername), i_movPlayDate);
END$$
DELIMITER ;

-- 20a
DROP PROCEDURE IF EXISTS customer_filter_mov; 
DELIMITER $$
CREATE PROCEDURE `customer_filter_mov`(IN i_movName VARCHAR(50), IN i_comName VARCHAR(50), IN i_city VARCHAR(50), 
IN i_state VARCHAR(3), IN i_minMovPlayDate DATE, IN i_maxMovPlayDate DATE)
BEGIN
	DROP TABLE IF EXISTS CosFilterMovie;
	CREATE TABLE CosFilterMovie
	SELECT movie as movName, theater as thName, street as thStreet, city as thCity, state as thState, zipcode as thZipcode,
		company as comName, date as movPlayDate, releaseDate as movReleaseDate 
	FROM scheduled_movies
	WHERE
        (i_movName = "ALL" OR movie = i_movName) AND
		(i_comName = "" OR company = i_comName) AND
        (i_city = "" OR city = i_city) AND
        (i_state = "" OR state = i_state) AND
		(i_minMovPlayDate IS NULL OR date >= i_minMovPlayDate) AND
		(i_maxMovPlayDate IS NULL OR date <= i_maxMovPlayDate) ;
END$$
DELIMITER ;

-- 20b
DROP PROCEDURE IF EXISTS customer_view_mov; 
DELIMITER $$
CREATE PROCEDURE `customer_view_mov`(IN i_creditCardNum CHAR(16), IN i_movName VARCHAR(50),
IN i_movReleaseDate DATE, IN i_thName VARCHAR(50),IN i_comName VARCHAR(50), IN i_movPlayDate DATE)
BEGIN
	INSERT INTO ccTransaction VALUES (i_creditCardNum, i_movName, i_movReleaseDate, i_thName, i_comName, i_movPlayDate);
END$$
DELIMITER ;

-- 21
DROP PROCEDURE IF EXISTS customer_view_history; 
DELIMITER $$
CREATE PROCEDURE `customer_view_history`(IN i_cusUsername VARCHAR(50))
BEGIN
	DROP TABLE IF EXISTS CosViewHistory;
	CREATE TABLE CosViewHistory
		SELECT movie as movName, theater as thName, company as comName, creditCardNum as creditCardNum, date as movPlayDate
		FROM ccTransaction NATURAL JOIN creditCard
		WHERE (username = i_cusUsername);
END$$
DELIMITER ;

-- 22a
DROP PROCEDURE IF EXISTS user_filter_th; 
DELIMITER $$
CREATE PROCEDURE `user_filter_th`(IN i_thName VARCHAR(50), IN i_comName
VARCHAR(50), IN i_city VARCHAR(50), IN i_state VARCHAR(3))
BEGIN
   DROP TABLE IF EXISTS UserFilterTh;
   CREATE TABLE UserFilterTh
   SELECT name as thName, street as thStreet, city as thCity, state as thState, zipcode as thZipcode, company as comName
   FROM theater
   WHERE (name = i_thName OR i_thName = "ALL") AND
       (company = i_comName OR i_comName = "ALL") AND
       (city = i_city OR i_city = "") AND
       (state = i_state OR i_state = "ALL");
END$$
DELIMITER ;
 
-- 22b
DROP PROCEDURE IF EXISTS user_visit_th; 
DELIMITER $$
CREATE PROCEDURE `user_visit_th`(IN i_thName VARCHAR(50), IN i_comName VARCHAR(50),
IN i_visitDate DATE, IN i_username VARCHAR(50))
BEGIN
   INSERT INTO visit (theater, company, date, username)
   VALUES (i_thName, i_comName, i_visitDate, i_username);
END$$
DELIMITER ;
 
-- 23
DROP PROCEDURE IF EXISTS user_filter_visitHistory; 
DELIMITER $$
CREATE PROCEDURE `user_filter_visitHistory`(IN i_username VARCHAR(50), IN
i_minVisitDate DATE, IN i_maxVisitDate DATE)
BEGIN
	DROP TABLE IF EXISTS UserVisitHistory;
	CREATE TABLE UserVisitHistory
	SELECT theater as thName, street as thStreet, city as thCity, state as thState, zipcode as thZipcode, 
    company as comName, date as visitDate
        FROM visited_theaters
        WHERE (username = i_username) AND
		(i_minVisitDate IS NULL OR date >= i_minVisitDate) AND
		(i_maxVisitDate IS NULL OR date <= i_maxVisitDate);
END$$   
DELIMITER ;
