SELECT
    d.fulldatealternatekey AS date,
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
    d.fulldatealternatekey
ORDER BY
    d.fulldatealternatekey;