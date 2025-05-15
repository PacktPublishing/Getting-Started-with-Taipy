SELECT
    d.fulldatealternatekey AS date,
    CASE
        WHEN d.daynumberofweek = 1 THEN 'Su'
        WHEN d.daynumberofweek = 2 THEN 'Mo'
        WHEN d.daynumberofweek = 3 THEN 'Tu'
        WHEN d.daynumberofweek = 4 THEN 'We'
        WHEN d.daynumberofweek = 5 THEN 'Th'
        WHEN d.daynumberofweek = 6 THEN 'Fr'
        WHEN d.daynumberofweek = 7 THEN 'Sa'
        ELSE '??'
    END AS day,
    CASE 
        WHEN p.productsubcategorykey = 1 THEN 'Mountain'
        WHEN p.productsubcategorykey = 2 THEN 'Road'
        WHEN p.productsubcategorykey = 3 THEN 'Touring'
        ELSE 'UNKNOWN'
    END AS type,
    p.englishproductname AS name,
    p.color AS color,
    TRIM(p.style) AS style,
    CASE 
        WHEN EXTRACT(YEAR FROM c.birthdate) > 1980 THEN 'Millenial'
        WHEN EXTRACT(YEAR FROM c.birthdate) BETWEEN 1966 AND 1980 THEN 'Gen X'
        WHEN EXTRACT(YEAR FROM c.birthdate) BETWEEN 1945 AND 1965 THEN 'Boomers'
        WHEN EXTRACT(YEAR FROM c.birthdate) < 1945 THEN 'Silent'
        ELSE 'Unknown'
    END AS generation,
    c.gender AS gender,
    fis.unitprice AS unit_price,
    SUM(fis.unitprice * fis.orderquantity)::float AS sales,
    COUNT(fis.orderquantity)::int AS items
FROM
    factinternetsales fis
    JOIN dimproduct p ON p.productkey = fis.productkey
    JOIN dimdate d ON d.datekey = fis.orderdatekey
    JOIN dimcustomer c ON c.customerkey = fis.customerkey
WHERE
    p.productsubcategorykey IN (1, 2, 3)
GROUP BY
    d.fulldatealternatekey,
    d.daynumberofweek,
    p.productsubcategorykey,
    p.englishproductname,
    p.color,
    p.style,
    EXTRACT(YEAR FROM c.birthdate),
    c.gender,
    fis.unitprice
ORDER BY
    d.fulldatealternatekey;
