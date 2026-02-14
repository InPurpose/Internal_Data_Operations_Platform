SELECT 
  n.nspname AS "Schema",
  c.relname AS "Name",
  CASE c.relkind 
    WHEN 'r' THEN 'table'
    WHEN 'v' THEN 'view'
    ELSE c.relkind
  END AS "Type",
  r.rolname AS "Owner"
FROM pg_class c
LEFT JOIN pg_namespace n ON n.oid = c.relnamespace
LEFT JOIN pg_roles r ON r.oid = c.relowner
WHERE c.relkind IN ('r','v') 
  AND n.nspname = 'public'
ORDER BY 1,2;
