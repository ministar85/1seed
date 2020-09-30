SELECT * fROM `greenhouse`.`sensorsdata`;

SELECT `datetime`,AVG(`Value`) as AvgValue
FROM TableName
GROUP BY `datetime`

SELECT `date_measured`,AVG(`temperature_indoor`) as AvgValue
FROM sensorsdata
GROUP BY `date_measured`

select temperature_indoor

SELECT `date_measured`,AVG(`temperature_indoor`) as AvgValue
FROM sensorsdata
WHERE date_measured >= DATE(NOW()) - INTERVAL 1 DAY
ORDER BY date_measured DESC

SELECT DayOfWk = DAYOFWEEK(DayOnly)
     , AvgChange = AVG(DayChange)
  FROM (SELECT DayOnly = DATE(TimeStamp)
             , DayChange = SUM(Change)
          FROM table
         GROUP BY DATE(TimeStamp)) dc
 GROUP BY DAYOFWEEK(DayOnly)
 
 
 SELECT day_of_week, AVG(order_count) average_order FROM 
(
  SELECT DAYNAME(order_date) day_of_week, 
         DAYOFWEEK(order_date) day_num, 
         TO_DAYS(order_date) date,
         count(*) order_count
  FROM data 
  GROUP BY date
) temp
GROUP BY day_of_week 
ORDER BY day_num
 
SELECT day_of_week, AVG(temperature_indoor) temperature_indoor FROM 
(
  SELECT DAYNAME(date_measured) day_of_week, 
         DAYOFWEEK(date_measured) day_num, 
         TO_DAYS(date_measured) date,
         count(*) temperature_indoor
  FROM sensorsdata 
  GROUP BY date_measured
) temperature_indoor
GROUP BY day_of_week 
ORDER BY day_num



SET @total_weeks = (
    SELECT
        TIMESTAMPDIFF(
            WEEK,
            MIN(date_measured),
            MAX(date_measured)
        )
     FROM sensorsdata
    );
SELECT
    DAYNAME(date_measured) AS day_of_week,
    ( COUNT(*) / @total_weeks ) AS avgorders,
    COUNT(*) AS total_orders
FROM 
    sensorsdata
GROUP BY
    DAYOFWEEK(date_measured)
    
    
SELECT dayofweek(`date_measured`) as 'Day',count(`temperature_indoor`)/count(DISTINCT day(`date_measured`)) as 'Average' FROM  `sensorsdata` GROUP BY dayofweek(`date_measured`)

SELECT monthname(`date_measured`) as 'Day',round(sum(`temperature_indoor`)/count(month(`date_measured`)),2) as 'Average' FROM  `sensorsdata` where username = "admin" GROUP BY month(`date_measured`)

SELECT dayofweek(`date_measured`) as 'Day',sum(`temperature_indoor`)/count(day(`date_measured`)) as 'Average' FROM  `sensorsdata` GROUP BY dayofweek(`date_measured`)

SELECT DAYNAME(`date_measured`) as 'Day',sum(`temperature_indoor`)/count(day(`date_measured`)) as 'Average' FROM  `sensorsdata` GROUP BY dayofweek(`date_measured`) limit 7

SELECT DAYNAME(`date_measured`) as 'Day',sum(`temperature_indoor`)/count(day(`date_measured`)) as 'Average' FROM  `sensorsdata` GROUP BY dayofweek(`date_measured`)

SELECT dayofmonth(`date_measured`) as 'Day',sum(`temperature_indoor`)/count(day(`date_measured`)) as 'Average' FROM  `sensorsdata` GROUP BY dayofmonth(`date_measured`)




SELECT DAYNAME(`date_measured`) as Day,round(sum(`temperature_outdoor`)/count(day(`date_measured`)),2) as Average FROM  `sensorsdata` where username = "admin" GROUP BY dayofweek(`date_measured`) limit 7 

SELECT monthname(`date_measured`) as 'Day',round(sum(`temperature_indoor`)/count(month(`date_measured`)),2) as 'Average' FROM  `sensorsdata` where username = "admin" GROUP BY month(`date_measured`) limit 12 

SELECT monthname(`date_measured`) as 'Day',round(sum(`temperature_indoor`)/count(month(`date_measured`)),2) as 'Average' FROM  `sensorsdata` where username = "admin" and temperature_outdoor IS NOT NULL GROUP BY month(`date_measured`) limit 12;



SELECT `date_measured` as Period,
round(sum(`temperature_outdoor`)/count(hour(`date_measured`)),2) as Average 
FROM  `sensorsdata` 
where username = "admin" 
and temperature_outdoor IS NOT NULL 
#and  date(date_measured) = CURDATE()
and  (date(date_measured) = CURDATE() or date(date_measured) = CURDATE() - 1)
GROUP BY day(`date_measured`),hour(`date_measured`)  
order by id desc limit 24




select * from  `sensorsdata` where date(date_measured) = CURDATE() - 1

select date(date_measured) from  `sensorsdata` limit 2;
select CURDATE() 



SELECT distinct hour(`date_measured`) as Period,round(sum(`temperature_indoor`)/count(hour(`date_measured`)),2) as Average FROM  `sensorsdata` where username = "admin" and temperature_indoor IS NOT NULL GROUP BY month(`date_measured`) limit 24;







