
CREATE DATABASE IF NOT EXISTS inventory_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE inventory_db;


DROP TABLE IF EXISTS stock_levels;
DROP TABLE IF EXISTS stock_movements;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS warehouses;
DROP TABLE IF EXISTS suppliers;

CREATE TABLE suppliers (
    supplier_id     INT           NOT NULL AUTO_INCREMENT,
    supplier_name   VARCHAR(100)  NOT NULL,
    contact_person  VARCHAR(100),
    email           VARCHAR(120),
    phone           VARCHAR(30),
    city            VARCHAR(60),
    created_at      TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (supplier_id)
) ENGINE=InnoDB;

CREATE TABLE warehouses (
    warehouse_id    INT           NOT NULL AUTO_INCREMENT,
    warehouse_name  VARCHAR(100)  NOT NULL,
    city            VARCHAR(60),
    state           VARCHAR(60),
    capacity_units  INT,
    created_at      TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (warehouse_id)
) ENGINE=InnoDB;

CREATE TABLE products (
    product_id        INT            NOT NULL AUTO_INCREMENT,
    sku               VARCHAR(20)    NOT NULL,
    product_name      VARCHAR(120)   NOT NULL,
    category          VARCHAR(60)    NOT NULL,
    unit_price        DECIMAL(10,2)  NOT NULL,
    supplier_id       INT            NOT NULL,
    reorder_level     INT            NOT NULL DEFAULT 20,
    max_stock_level   INT            NOT NULL DEFAULT 200,
    reorder_quantity  INT            NOT NULL DEFAULT 50,
    is_active         TINYINT(1)     NOT NULL DEFAULT 1,
    created_at        TIMESTAMP      NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at        TIMESTAMP      NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (product_id),
    UNIQUE KEY uq_products_sku (sku),
    CONSTRAINT fk_products_supplier FOREIGN KEY (supplier_id) REFERENCES suppliers (supplier_id),
    CONSTRAINT chk_products_price   CHECK (unit_price >= 0),
    CONSTRAINT chk_products_levels  CHECK (max_stock_level > reorder_level)
) ENGINE=InnoDB;


CREATE TABLE stock_movements (
    movement_id    INT          NOT NULL AUTO_INCREMENT,
    product_id     INT          NOT NULL,
    warehouse_id   INT          NOT NULL,
    movement_type  ENUM('IN','OUT','ADJUSTMENT') NOT NULL,
    quantity       INT          NOT NULL,
    movement_date  DATE         NOT NULL,
    reference_no   VARCHAR(30),
    reason         VARCHAR(255),
    created_at     TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (movement_id),
    CONSTRAINT fk_mov_product   FOREIGN KEY (product_id)   REFERENCES products (product_id),
    CONSTRAINT fk_mov_warehouse FOREIGN KEY (warehouse_id) REFERENCES warehouses (warehouse_id),
    CONSTRAINT chk_mov_qty_nonzero CHECK (quantity <> 0),
    CONSTRAINT chk_mov_sign CHECK ((movement_type = 'IN' AND quantity > 0)
                                OR (movement_type = 'OUT' AND quantity < 0)
                                OR  movement_type = 'ADJUSTMENT')
) ENGINE=InnoDB;


CREATE TABLE stock_levels (
    product_id        INT        NOT NULL,
    warehouse_id      INT        NOT NULL,
    quantity_on_hand  INT        NOT NULL DEFAULT 0,
    last_updated      TIMESTAMP  NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (product_id, warehouse_id),
    CONSTRAINT fk_sl_product   FOREIGN KEY (product_id)   REFERENCES products (product_id),
    CONSTRAINT fk_sl_warehouse FOREIGN KEY (warehouse_id) REFERENCES warehouses (warehouse_id)
) ENGINE=InnoDB;

DROP TRIGGER IF EXISTS trg_stock_movements_ai;
CREATE TRIGGER trg_stock_movements_ai AFTER INSERT ON stock_movements
FOR EACH ROW
    INSERT INTO stock_levels (product_id, warehouse_id, quantity_on_hand)
    VALUES (NEW.product_id, NEW.warehouse_id, NEW.quantity)
    ON DUPLICATE KEY UPDATE quantity_on_hand = quantity_on_hand + NEW.quantity;

SHOW TABLES;
