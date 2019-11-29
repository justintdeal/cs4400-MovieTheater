USE `team50`;

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
 
-- 1 questionable
DROP PROCEDURE IF EXISTS user_login;
DELIMITER $$
CREATE PROCEDURE `user_login`(IN i_username VARCHAR(50), IN i_password
VARCHAR(50))
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
CREATE PROCEDURE `user_register`(IN i_username VARCHAR(50), IN i_password
VARCHAR(50), IN i_firstname VARCHAR(50), IN i_lastname VARCHAR(50))
BEGIN
    INSERT INTO user (username, password, firstname, lastname) VALUES
    (i_username, MD5(i_password), i_firstname, i_lastname);
END$$
DELIMITER ;
 
-- 4a
DROP PROCEDURE IF EXISTS customer_only_register;
DELIMITER $$
CREATE PROCEDURE `customer_only_register`(IN i_username VARCHAR(50), IN i_password
VARCHAR(50), IN i_firstname VARCHAR(50), IN i_lastname VARCHAR(50))
BEGIN
    INSERT INTO customer (username, password, firstname, lastname) VALUES
    (i_username, MD5(i_password), i_firstname, i_lastname);
END$$
DELIMITER ;
 
-- 4b
DROP PROCEDURE IF EXISTS customer_add_creditcard;
DELIMITER $$
CREATE PROCEDURE `customer_add_creditcard`(IN i_username VARCHAR(50), IN cc_num CHAR(16))
BEGIN
    INSERT INTO creditCard (username, creditCardNum) VALUES
    (i_username, cc_num);
END$$
DELIMITER ;
 
-- 5
DROP PROCEDURE IF EXISTS manager_only_register;
DELIMITER $$
CREATE PROCEDURE `manager_only_register`(IN i_username VARCHAR(50), IN i_password
VARCHAR(50), IN i_firstname VARCHAR(50), IN i_lastname VARCHAR(50), IN i_comName VARCHAR(50),
    IN i_empStreet VARCHAR(50), IN i_empCity VARCHAR(50), IN i_empState CHAR(2), IN i_empZipcode CHAR(5))
BEGIN
    INSERT INTO user (username, password, firstname, lastname) VALUES
    (i_username, MD5(i_password), i_firstname, i_lastname);
    INSERT INTO manager (username, company, street, city, state, zipcode) VALUES
    (i_username, i_comName, i_empStreet, i_empCity, i_empState, i_empZipcode);
END$$
DELIMITER ;
 
-- 6a
DROP PROCEDURE IF EXISTS manager_customer_register;
DELIMITER $$
CREATE PROCEDURE `manager_customer_register`(IN i_username VARCHAR(50), IN i_password
VARCHAR(50), IN i_firstname VARCHAR(50), IN i_lastname VARCHAR(50), IN i_comName VARCHAR(50),
    IN i_empStreet VARCHAR(50), IN i_empCity VARCHAR(50), IN i_empState CHAR(2), IN i_empZipcode CHAR(5))
BEGIN
    INSERT INTO user (username, password, firstname, lastname) VALUES
    (i_username, MD5(i_password), i_firstname, i_lastname);
    INSERT INTO manager (username, company, street, city, state, zipcode) VALUES
    (i_username, i_comName, i_empStreet, i_empCity, i_empState, i_empZipcode);
END$$
DELIMITER ;
 
-- 6b
DROP PROCEDURE IF EXISTS manager_customer_add_creditcard;
DELIMITER $$
CREATE PROCEDURE `manager_customer_add_creditcard`(IN i_username VARCHAR(50), IN cc_num CHAR(16))
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
    set status = 'approved'
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
    set status = 'declined'
    where username = i_username and not status = 'approved';
END$$
DELIMITER ;
 
-- 13c
DROP PROCEDURE IF EXISTS admin_filter_user;
DELIMITER $$
CREATE PROCEDURE `admin_filter_user`(IN i_username VARCHAR(50), IN i_status
ENUM('pending','approved','declined','ALL'), 
IN i_sortBy ENUM('username','creditCardCount','userType','status'),
IN i_sortDirection ENUM('ASC','DESC'))
BEGIN
    DROP TABLE IF EXISTS AdFilterUser;
    CREATE TABLE AdFilterUser
    SELECT username, count(*) as creditCardCount, get_type(username) as userType, status
    FROM user
    NATURAL JOIN creditCard
        WHERE (username = i_username OR i_username = '') AND
        (status = i_status OR i_status = "ALL")
    GROUP BY username
    UNION
    SELECT username, 0 as creditCardCount, get_type(username) as userType, status
    FROM user
        WHERE (username = i_username OR i_username = '') AND
        (status = i_status OR i_status = "ALL")
    GROUP BY username
    ORDER BY 
        case when i_sortBy IS NULL and (i_sortDirection IS NULL or i_sortDirection = 'DESC') then username end DESC,
        case when i_sortBy = "username" and (i_sortDirection IS NULL or i_sortDirection = 'DESC') then username end DESC,
        case when i_sortBy = "creditCardCount" and (i_sortDirection IS NULL or i_sortDirection = 'DESC') then creditCardCount end DESC,
        case when i_sortBy = "userType" and (i_sortDirection IS NULL or i_sortDirection = 'DESC') then userType end DESC,
        case when i_sortBy = "status" and (i_sortDirection IS NULL or i_sortDirection = 'DESC') then status end DESC,
        case when i_sortBy IS NULL and i_sortDirection = 'ASC' then username end ASC,
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
IN i_sortBy ENUM('comName','numCityCover','numTheater','numEmployee'),
IN i_sortDirection ENUM('ASC','DESC'))
BEGIN
    DROP TABLE IF EXISTS AdFilterCom;
    CREATE TABLE AdFilterCom
    SELECT company.name as compName,
count(distinct theater.city) as numCityCover, count(theater.name) as numTheater, num_emp(company.name) as numEmployee
    FROM company, theater
    where theater.company = company.name
    GROUP BY compName
    ORDER BY 
        case when i_sortBy IS NULL and (i_sortDirection IS NULL or i_sortDirection = 'DESC') then comName end DESC,
        case when i_sortBy = "comName" and (i_sortDirection IS NULL or i_sortDirection = 'DESC') then comName end DESC,
        case when i_sortBy = "numCityCover" and (i_sortDirection IS NULL or i_sortDirection = 'DESC') then numCityCover end DESC,
        case when i_sortBy = "numTheater" and (i_sortDirection IS NULL or i_sortDirection = 'DESC') then numTheater end DESC,
        case when i_sortBy = "numEmployee" and (i_sortDirection IS NULL or i_sortDirection = 'DESC') then numEmployee end DESC,
        case when i_sortBy IS NULL and i_sortDirection = 'ASC' then comName end ASC,
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
IN i_thState VARCHAR(50), IN i_thZipcode VARCHAR(50), IN i_capacity INT,
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
CREATE PROCEDURE `admin_create_movie`(IN i_movName VARCHAR(50),
IN i_movDuration INT, IN i_movReleaseDate DATE)
BEGIN
    INSERT INTO movie
    VALUES (i_movName, i_movDuration, i_movReleaseDate);
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
    SELECT movie,theater,street,city,state,zipcode,name,date,releaseDate 
    FROM moviePlay NATURAL JOIN theater
    WHERE (i_movName = "ALL" OR movie = i_movName) AND
        (i_comName = "" OR name = i_comName) AND
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
        SELECT movie, theater, company, creditCardNum, date
        FROM ccTransaction NATURAL JOIN creditCard
        WHERE username = i_cusUsername;
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
SELECT thName, thStreet, thCity, thState, thZipcode, comName
   FROM theater
   WHERE
(thName = i_thName OR i_thName = "ALL") AND
       (comName = i_comName OR i_comName = "ALL") AND
       (thCity = i_city OR i_city = "") AND
       (thState = i_state OR i_state = "ALL");
END$$
DELIMITER ;
 
-- 22b
DROP PROCEDURE IF EXISTS user_visit_th;
DELIMITER $$
CREATE PROCEDURE `user_visit_th`(IN i_thName VARCHAR(50), IN i_comName VARCHAR(50),
IN i_visitDate DATE, IN i_username VARCHAR(50))
BEGIN
   INSERT INTO UserVisitTheater (thName, comName, visitDate, username)
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
SELECT thName, thStreet, thCity, thState, thZipcode, comName, visitDate
   FROM UserVisitTheater
NATURAL JOIN
       Theater
WHERE
(username = i_username) AND
       (i_minVisitDate IS NULL OR visitDate >= i_minVisitDate) AND
       (i_maxVisitDate IS NULL OR visitDate <= i_maxVisitDate);
END$$
DELIMITER ;
