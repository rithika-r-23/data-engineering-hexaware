
const database = db.getSiblingDB("inventory_audit");
database.stock_audit_logs.drop();


database.createCollection("stock_audit_logs", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["product_id", "warehouse_id", "action", "quantity_change", "reason", "performed_by", "timestamp"],
      properties: {
        movement_id:     { bsonType: "number" },
        product_id:      { bsonType: "number", description: "products.product_id in MySQL" },
        warehouse_id:    { bsonType: "number", description: "warehouses.warehouse_id in MySQL" },
        action:          { enum: ["STOCK_IN", "STOCK_OUT", "STOCK_ADJUSTMENT", "REORDER_LEVEL_CHANGE"] },
        quantity_change: { bsonType: "number" },
        reason:          { bsonType: "string" },
        reason_category: { bsonType: "string" },
        performed_by:    { bsonType: "string" },
        timestamp:       { bsonType: "date" }
      }
    }
  }
});

// 2) Sample audit documents (flexible JSON - 'details' can differ per document)
database.stock_audit_logs.insertMany([
  {
    movement_id: 3801, product_id: 5, warehouse_id: 1, action: "STOCK_ADJUSTMENT",
    quantity_change: -4, previous_quantity: 12, new_quantity: 8,
    reason: "Damaged goods", reason_category: "DAMAGE", performed_by: "meena.s",
    timestamp: new Date("2026-10-05T10:15:00Z"),
    details: { reference_no: "ADJ-482913", approved_by: "ravi.k", notes: "Water damage in bay C4", photos: ["IMG_2201.jpg"] }
  },
  {
    movement_id: 3802, product_id: 5, warehouse_id: 1, action: "STOCK_ADJUSTMENT",
    quantity_change: 2, previous_quantity: 8, new_quantity: 10,
    reason: "Found stock during audit", reason_category: "COUNT_CORRECTION", performed_by: "meena.s",
    timestamp: new Date("2026-10-06T08:40:00Z"),
    details: { reference_no: "ADJ-482950", approved_by: "ravi.k" }
  },
  {
    movement_id: 3803, product_id: 17, warehouse_id: 2, action: "STOCK_ADJUSTMENT",
    quantity_change: -6, previous_quantity: 794, new_quantity: 788,
    reason: "Theft / shrinkage", reason_category: "LOSS", performed_by: "arjun.p",
    timestamp: new Date("2026-10-07T14:05:00Z"),
    details: { reference_no: "ADJ-483011", approved_by: "divya.n", police_report_no: "FIR-2026-0412" }
  },
  {
    movement_id: 3804, product_id: 24, warehouse_id: 1, action: "STOCK_IN",
    quantity_change: 260, previous_quantity: 11, new_quantity: 271,
    reason: "Purchase order receipt", reason_category: "PURCHASE", performed_by: "system",
    timestamp: new Date("2026-10-08T09:00:00Z"),
    details: { reference_no: "PO-771245", supplier: "Coromandel Traders" }
  },
  {
    product_id: 9, warehouse_id: 2, action: "REORDER_LEVEL_CHANGE",
    quantity_change: 0, reason: "Seasonal demand - raised reorder level from 80 to 105",
    reason_category: "POLICY", performed_by: "divya.n",
    timestamp: new Date("2026-10-09T11:30:00Z"),
    details: { old_reorder_level: 80, new_reorder_level: 105 }
  }
]);

// 3) INDEXES - quick search by product ID or warehouse
const logs = database.stock_audit_logs;
logs.createIndex({ product_id: 1 },                                   { name: "idx_product" });
logs.createIndex({ warehouse_id: 1 },                                 { name: "idx_warehouse" });
logs.createIndex({ product_id: 1, warehouse_id: 1, timestamp: -1 },   { name: "idx_product_wh_time" });
logs.createIndex({ reason_category: 1, timestamp: -1 },               { name: "idx_reason_time" });
logs.createIndex({ movement_id: 1 },                                  { name: "uq_movement", unique: true, sparse: true });
printjson(logs.getIndexes().map(i => i.name));

// 4) Example queries (and proof the index is used)
print("--- all audit entries for product 5 ---");
printjson(logs.find({ product_id: 5 }, { _id: 0, action: 1, quantity_change: 1, reason: 1, timestamp: 1 }).toArray());

print("--- adjustments in warehouse 1, newest first ---");
printjson(logs.find({ warehouse_id: 1, action: "STOCK_ADJUSTMENT" }).sort({ timestamp: -1 }).toArray());

print("--- explain: should say IXSCAN, not COLLSCAN ---");
printjson(logs.find({ product_id: 5 }).explain("queryPlanner").queryPlanner.winningPlan.inputStage);

print("--- units lost per reason category ---");
printjson(logs.aggregate([
  { $match: { action: "STOCK_ADJUSTMENT", quantity_change: { $lt: 0 } } },
  { $group: { _id: "$reason_category", entries: { $sum: 1 }, units_lost: { $sum: "$quantity_change" } } },
  { $sort: { units_lost: 1 } }
]).toArray());
