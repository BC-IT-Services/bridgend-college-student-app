SELECT session_code, start_date, end_date FROM ebslive.dbo.SESSIONS
WHERE ? BETWEEN start_date AND end_date;