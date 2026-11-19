SELECT
    order_date,
    Region,
    State,
    Category,
    `Sub-Category`,
    Segment,
    Sales,
    Profit,
    Quantity
FROM superstore_sales
ORDER BY Profit DESC
LIMIT 10;