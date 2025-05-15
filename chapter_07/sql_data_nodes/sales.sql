SELECT
	fulldatealternatekey AS date,
	CASE
		WHEN daynumberofweek = 1 THEN 'Su'
		WHEN daynumberofweek = 2 THEN 'Mo'
		WHEN daynumberofweek = 3 THEN 'Tu'
		WHEN daynumberofweek = 4 THEN 'We'
		WHEN daynumberofweek = 5 THEN 'Th'
		WHEN daynumberofweek = 6 THEN 'Fr'
		WHEN daynumberofweek = 7 THEN 'Sa'
		ELSE '??'
	END AS day,
	productalternatekey AS product,
	CASE 
		WHEN productsubcategorykey = 1 THEN 'Mountain'
		WHEN productsubcategorykey = 2 THEN 'Road'
		WHEN productsubcategorykey = 3 THEN 'Touring'
		ELSE 'UNKNOWN'
	END AS type,
	englishproductname AS name,
	color AS color,
	trim(style) AS style, 
	customeralternatekey AS customer,
	extract(year from birthdate) AS birth,
	CASE WHEN extract(year from birthdate) > 1980 THEN 'Millenial'
		WHEN extract(year from birthdate) BETWEEN 1966 AND 1980 THEN 'Gen X'
        WHEN extract(year from birthdate) BETWEEN 1945 AND 1965 THEN 'Boomers'
        WHEN extract(year from birthdate) < 1945 THEN 'Silent'
        ELSE 'Unknown'
    END AS generation,
	gender AS gender,
	unitprice AS unit_price,
	orderquantity::int AS items,
	unitprice * orderquantity::float AS sales
FROM
    factinternetsales
	JOIN dimproduct ON dimproduct.productkey = factinternetsales.productkey
	JOIN dimdate on  dimdate.datekey = factinternetsales.orderdatekey
	JOIN dimcustomer on dimcustomer.customerkey = factinternetsales.customerkey
WHERE 
	productsubcategorykey IN (1, 2, 3)