# Week 1 – Database Foundations: MySQL & MongoDB
**Tools:** MySQL, MongoDB

## Capstone tasks
- [x] Create MySQL tables: `products`, `warehouses`, `stock_movements`, `suppliers` → `mysql/01_schema.sql` (plus a helper table `stock_levels` + trigger)
- [x] Insert and update stock levels via CRUD operations → `mysql/02_crud_operations.sql`, `load_mysql.py`
- [x] Write a stored procedure to identify products below reorder level → `mysql/03_stored_procedures.sql` (`sp_products_below_reorder`)
- [x] Use MongoDB to store audit logs / stock adjustment reasons in JSON → `mongodb/audit_logs.js`, `mongodb/load_audit_logs.py`
- [x] Add indexes for quick search by product ID or warehouse → `mysql/04_indexes.sql` and the index section of `mongodb/audit_logs.js`

## Deliverables
- SQL script with schema, CRUD, stored procedure → the four files in `mysql/`
- MongoDB script with audit logs and indexing → `mongodb/audit_logs.js`

## Run order
```bash
# from the project root, after:  python generate_mock_data.py
mysql -u root -p < week1_database_foundations/mysql/01_schema.sql
python week1_database_foundations/load_mysql.py
mysql -u root -p < week1_database_foundations/mysql/02_crud_operations.sql
mysql -u root -p inventory_db < week1_database_foundations/mysql/03_stored_procedures.sql
mysql -u root -p inventory_db < week1_database_foundations/mysql/04_indexes.sql

mongosh "mongodb://localhost:27017" --file week1_database_foundations/mongodb/audit_logs.js
python week1_database_foundations/mongodb/load_audit_logs.py
```
