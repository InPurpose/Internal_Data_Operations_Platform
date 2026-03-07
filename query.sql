-- select count(*) from orders;
-- select status, count(*) from orders group by status;


-- status = 'paid'

-- created_at >= now() - interval '7 days'

-- sum(total_amount)

select * from orders limit 5;

EXPLAIN ANALYZE
select sum(O.total_amount) 
from orders O 
where O.order_time >= now() - interval '7 days' and O.status = 'paid';

UPDATE users
SET role = analyst
WHERE id = 20101;

INSERT INTO table_name VALUES (value1, value2, value3, ...);
-- ================================================================================================================================================
INSERT INTO users values ('admin@example.com',NOW(),'$2b$12$o7dZdlGATZRkAPY9uQAT8.2bRr7OcRrWVRulqL3HWKt1AVyHx2fvy','admin',True);

INSERT INTO users (email, country, device_type, register_time, hashed_password, role, is_active)
VALUES (
    'admin@example.com', 
    NULL, 
    NULL, 
    NOW(), 
    '$2b$12$o7dZdlGATZRkAPY9uQAT8.2bRr7OcRrWVRulqL3HWKt1AVyHx2fvy', 
    'admin', 
    True
);
-- ================================================================================================================================================


select * 
from orders O
where O.user_id in (select OS.user_id from orders OS group by OS.user_id limit 1) and O.status = 'paid';
