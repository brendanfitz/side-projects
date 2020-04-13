SELECT COUNT(*)

FROM visualizations.stock_prices;

SELECT *

FROM visualizations.stock_prices

ORDER BY date DESC

LIMIT 1;

SELECT
  EXTRACT('year' from s.date),
  AVG(close) AS average_closing_price
  

FROM visualizations.stock_prices s

GROUP BY 1

ORDER BY 1;

/* Max Cloing Price with Date Per Year */
WITH prices_with_max_close_date AS (
  SELECT
    EXTRACT('year' from date) AS trading_year,
    date,
    close,
    first_value(date) over (PARTITION BY EXTRACT('year' from date) ORDER BY EXTRACT('year' from date), close DESC) AS max_close_date
  FROM visualizations.stock_prices
)
SELECT
  trading_year,
  date,
  close as max_closing_value
  
FROM prices_with_max_close_date

WHERE date = max_close_date

ORDER BY 1;


/* 25 Largest Changes in Closing Value */
WITH prices_with_daily_delta AS (
  SELECT
    date,
    LAG(close) OVER (ORDER BY date) AS previous_day_stock_price,
    close,
    close / LAG(close) OVER (ORDER BY date) - 1 AS daily_price_delta
  
  FROM visualizations.stock_prices
)
SELECT *

FROM prices_with_daily_delta

WHERE date >= '1957-03-04' /* Start of the S&P, there were too many dates in the 1930s without this filter! */

ORDER BY ABS(daily_price_delta) DESC

LIMIT 25;


/* Average Deviation by Decade */
WITH prices_with_daily_delta AS (
  SELECT
    date,
    LAG(close) OVER (ORDER BY date) AS previous_day_stock_price,
    close,
    close / LAG(close) OVER (ORDER BY date) - 1 AS daily_price_delta
  
  FROM visualizations.stock_prices
)
SELECT 
  EXTRACT('decade' FROM date) AS trading_year,
  AVG(daily_price_delta) * 100 AS average_daily_deviation
  
FROM prices_with_daily_delta

GROUP BY 1

ORDER BY 1;

/* Max Intra-Day Trading Range */
SELECT
  date,
  open,
  low,
  high,
  (high - low) / open  as intraday_trading_range_over_opening
  
FROM visualizations.stock_prices

ORDER BY 5 DESC

LIMIT 25;


/* 200-day close moving-average */
SELECT
  date,
  close,
  AVG(close) OVER (ORDER BY date ROWS BETWEEN 200 - 1 PRECEDING AND CURRENT ROW) AS close_200d_ma
  
FROM visualizations.stock_prices

WHERE date >= '1957-03-04' /* Start of the S&P, there were too many dates in the 1930s without this filter! */;

/* 200-day close moving-average crossings */
WITH prices_with_ma AS (
  SELECT
    date,
    close,
    AVG(close) OVER (ORDER BY date ROWS BETWEEN 200 - 1 PRECEDING AND CURRENT ROW) AS close_200d_ma
  
  FROM visualizations.stock_prices
  
  WHERE date >= '1957-03-04' /* Start of the S&P, there were too many dates in the 1930s without this filter! */
),
prices_with_ma_lagged AS (
SELECT
  *,
  close - close_200d_ma AS close_minus_200d_ma,
  LAG(close - close_200d_ma) OVER (ORDER BY date) AS close_minus_200d_ma_lagged
  

FROM prices_with_ma
)
SELECT *

FROM prices_with_ma_lagged

WHERE (close_minus_200d_ma > 0 and close_minus_200d_ma_lagged < 0)
   OR (close_minus_200d_ma < 0 and close_minus_200d_ma_lagged > 0)
   OR close_minus_200d_ma = 0;
