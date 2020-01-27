-- Query 1:
SELECT e.kg
FROM electricity_per_capita e, country_code c
WHERE c.country_name = “India” AND c.country_code = e.country_code AND e.Year = 1985;

-- Query 2:
SELECT DISTINCT p.population*e.kg AS total_electricity, p.country_code, p.year
FROM country_population p, electricity_per_capita e, country_code c
WHERE p.country_code = e.country_code and p.year = e.year and p.country_code = "USA" AND p.year = 2000;

-- Query 3:
SELECT AVG(e.Percentage)
FROM electricity_from_renewable_percentage e, country_code c
WHERE c.country_name = “Germany” AND c.country_code = e.country_code AND e.Year >= 1999 AND e.Year <= 2014;

--- Query 4:
CREATE VIEW country1_resource1
AS
    SELECT DISTINCT year, kg
    FROM energy_per_thousand_dollars as e, country_code as c
    WHERE e.country_code = c.country_code AND c.country_name = "tanzania" AND year <= 2010 AND year >= 2005
;

CREATE VIEW country2_resource2
AS
    SELECT DISTINCT year, percentage
    FROM access_to_electricity_percentage as e, country_code as c
    WHERE e.country_code = c.country_code AND c.country_name = "Tanzania" AND year <= 2010 AND year >= 2005
;

SELECT
    AVG((s.kg - (SELECT AVG(s.kg)
    FROM country1_resource1 s))*(i.percentage - (SELECT AVG(i.percentage)
    FROM country2_resource2 i)))/((SELECT STDDEV(s1.kg)
    from country1_resource1 s1)*(SELECT STDDEV(s2.percentage)
    FROM country2_resource2 s2))
FROM country1_resource1 as s, country2_resource2 as i
WHERE s.year = i.year;

drop view if exists country1_resource1, country2_resource2;

-- Query 5:
CREATE VIEW country1_resource1
AS
    SELECT DISTINCT year, kg
    FROM electricity_per_capita as e, country_code as c
    WHERE e.country_code = c.country_code AND c.country_name = "switzerland" AND year <= 2010 AND year >= 2000
;
CREATE VIEW country2_resource2
AS
    SELECT DISTINCT year, kg
    FROM electricity_per_capita as e, country_code as c
    WHERE e.country_code = c.country_code AND c.country_name = "italy" AND year <= 2010 AND year >= 2000
;
SELECT
    AVG((s.kg - (SELECT AVG(s.kg)
    FROM country1_resource1 s))*(i.kg - (SELECT AVG(i.kg)
    FROM country2_resource2 i)))/((SELECT STDDEV(s1.kg)
    from country1_resource1 s1)*(SELECT STDDEV(s2.kg)
    FROM country2_resource2 s2))
FROM country1_resource1 as s, country2_resource2 as i
WHERE s.year = i.year;
drop view if exists country1_resource1, country2_resource2;


--- Query 6:
SELECT c.country_name
FROM country_code c, electricity_from_renewable_percentage r
WHERE c.country_code = r.country_code AND r.year = 2000
ORDER BY r.percentage DESC
LIMIT 5;

--- Query 7:
SELECT c.country_name
FROM country_code c, electricity_from_renewable_percentage r
WHERE c.country_code = r.country_code
GROUP BY r.country_code
ORDER BY AVG(r.percentage) DESC
LIMIT 5;

-- Query 8:
SELECT c.country_name
FROM country_code c, electricity_from_renewable_percentage r
WHERE c.country_code = r.country_code AND r.year >= 2013 AND r.year < 2018
GROUP BY r.country_code
ORDER BY AVG(r.Percentage) DESC
Limit 5;

-- Query 9:
SELECT DISTINCT c.country_name
FROM country_code c, electricity_from_renewable_percentage r, electricity_from_coal_percentage cl, electricity_from_oil_percentage o
WHERE c.country_code = r.country_code AND r.year >= 1988 AND r.year < 2018 AND cl.country_code = r.country_code AND o.country_code = r.country_code AND r.year = cl.year AND cl.year = o.year
GROUP BY c.country_code
HAVING AVG(cl.percentage) + AVG(o.percentage) < AVG(r.percentage);

-- Query 10:
CREATE VIEW avg_renewable_energy
AS
    SELECT Year, AVG(Percentage) as avg_energy
    FROM electricity_from_renewable_percentage
    GROUP BY Year;

SELECT AVG((r.avg_energy - (SELECT AVG(r.avg_energy)
    FROM avg_renewable_energy r))*(p.real_value_dollar - (SELECT AVG(p.real_value_dollar)
    FROM usa_crude_oil_prices p)))/((SELECT STDDEV(r.avg_energy)
    FROM avg_renewable_energy r)*(SELECT STDDEV(p.real_value_dollar)
    FROM usa_crude_oil_prices p))
FROM avg_renewable_energy r, usa_crude_oil_prices p
WHERE r.year = p.year;

DROP VIEW avg_renewable_energy;

--- Query 11:

CREATE VIEW total_energy_global
AS
    SELECT e.year, SUM(e.kg*p.population) as total_energy
    FROM electricity_per_capita e, country_population p
    WHERE e.country_code = p.country_code AND e.year = p.year
    GROUP BY e.year;

SELECT AVG((r.total_energy - (SELECT AVG(r.total_energy)
    FROM total_energy_global r))*(p.real_value_dollar - (SELECT AVG(p.real_value_dollar)
    FROM usa_crude_oil_prices p)))/((SELECT STDDEV(r.total_energy)
    FROM total_energy_global r)*(SELECT STDDEV(p.real_value_dollar)
    FROM usa_crude_oil_prices p))
FROM total_energy_global r, usa_crude_oil_prices p
WHERE r.year = p.year;

DROP VIEW total_energy_global;

--- Query 12:

CREATE VIEW total_energy_global
AS
    SELECT e.year, SUM(e.kg*p.population) as total_energy
    FROM electricity_per_capita e, country_population p, electricity_from_coal_percentage cl, electricity_from_oil_percentage o
    WHERE e.country_code = p.country_code AND e.year = p.year AND cl.country_code = e.country_code AND o.country_code = cl.country_code AND o.year = cl.year AND o.year = e.year
    GROUP BY e.year
    HAVING AVG(cl.percentage) + AVG(o.percentage) > 70;

SELECT AVG((r.total_energy - (SELECT AVG(r.total_energy)
    FROM total_energy_global r))*(p.real_value_dollar - (SELECT AVG(p.real_value_dollar)
    FROM usa_crude_oil_prices p)))/((SELECT STDDEV(r.total_energy)
    FROM total_energy_global r)*(SELECT STDDEV(p.real_value_dollar)
    FROM usa_crude_oil_prices p))
FROM total_energy_global r, usa_crude_oil_prices p
WHERE r.year = p.year;

DROP VIEW total_energy_global;




-------------------------CREATE TABLE COMMANDS---------------------------------------

CREATE TABLE IF NOT EXISTS 
access_to_electricity_percentage (
country_code varchar(5) NOT NULL,                   
year INT NOT NULL,          
percentage FLOAT CHECK(percentage>=0 AND percentage <=100),                   
id INT(10) NOT NULL AUTO_INCREMENT,
PRIMARY KEY (id)          
);

CREATE TABLE IF NOT EXISTS 
electricity_from_renewable_percentage (
country_code varchar(5) NOT NULL,                   
year INT NOT NULL,          
percentage FLOAT CHECK(percentage>=0 AND percentage <=100),                   
id INT(10) NOT NULL AUTO_INCREMENT,
PRIMARY KEY (id)
);

DROP TABLE electricity_from_coal_percentage;
CREATE TABLE IF NOT EXISTS 
electricity_from_coal_percentage (
country_code varchar(5) NOT NULL,                   
year INT NOT NULL,          
percentage FLOAT CHECK(percentage>=0 AND percentage <=100),                   
id INT(10) NOT NULL AUTO_INCREMENT,
PRIMARY KEY (id)           
);

DROP TABLE electricity_from_nuclear_percentage;
CREATE TABLE IF NOT EXISTS 
electricity_from_nuclear_percentage (
country_code varchar(5) NOT NULL,                   
year INT NOT NULL,          
percentage FLOAT CHECK(percentage>=0 AND percentage <=100),                   
id INT(10) NOT NULL AUTO_INCREMENT,
PRIMARY KEY (id)           
);

DROP TABLE electricity_from_oil_percentage;
CREATE TABLE IF NOT EXISTS 
electricity_from_oil_percentage (
country_code varchar(5) NOT NULL,                   
year INT NOT NULL,          
percentage FLOAT CHECK(percentage>=0 AND percentage <=100),                   
id INT(10) NOT NULL AUTO_INCREMENT,
PRIMARY KEY (id)           
);

DROP TABLE country_population;
CREATE TABLE IF NOT EXISTS 
country_population (
country_code varchar(5) NOT NULL,                   
year INT NOT NULL,          
population INT,
id INT(10) NOT NULL AUTO_INCREMENT,
PRIMARY KEY (id)                   
);

DROP TABLE electricity_per_capita;
CREATE TABLE IF NOT EXISTS 
electricity_per_capita (
country_code varchar(5) NOT NULL,                   
year INT NOT NULL,          
kg FLOAT,                   
id INT(10) NOT NULL AUTO_INCREMENT,
PRIMARY KEY (id)
);

DROP TABLE energy_per_thousand_dollars;
CREATE TABLE IF NOT EXISTS 
energy_per_thousand_dollars (
country_code varchar(5) NOT NULL,                   
year INT NOT NULL,          
kg FLOAT,                   
id INT(10) NOT NULL AUTO_INCREMENT,
PRIMARY KEY (id)                 
);

CREATE TABLE IF NOT EXISTS 
country_metadata (
country_code varchar(5) NOT NULL UNIQUE,          
region varchar(50) NOT NULL,                   
IncomeGroup varchar(50) NOT NULL,
PRIMARY KEY (country_code)               
);


DROP TABLE world_happiness_index;
CREATE TABLE IF NOT EXISTS 
world_happiness_index (
country varchar(50) NOT NULL UNIQUE,                   
happiness_score FLOAT CHECK(happiness_score>0 AND happiness_score <10),
life_expectancy FLOAT CHECK(life_expectancy>0 AND life_expectancy <1),
government_corruption FLOAT CHECK(government_corruption>0 AND government_corruption <1),
PRIMARY KEY (country)         
);

CREATE TABLE IF NOT EXISTS 
country_code (
country_name varchar(50) NOT NULL UNIQUE,          
country_code varchar(5) NOT NULL UNIQUE,                   
PRIMARY KEY (country_code)               
);

CREATE TABLE IF NOT EXISTS 
usa_crude_oil_prices (
year INT NOT NULL UNIQUE,          
real_value_dollar FLOAT NOT NULL,                   
nominal_value_dollar FLOAT NOT NULL,                   
PRIMARY KEY (year) 
);

CREATE TABLE IF NOT EXISTS 
Imported_Crude_Oil_Prices (
year INT NOT NULL UNIQUE,          
real_value_dollar FLOAT NOT NULL,                  
PRIMARY KEY (year) 
);
