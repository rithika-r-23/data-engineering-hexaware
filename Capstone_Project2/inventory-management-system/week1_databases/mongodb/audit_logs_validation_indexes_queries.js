

const auditDb = db.getSiblingDB("inventory_audit");
const logs = auditDb.stock_audit_logs;

print("Documents in stock_audit_logs: " + logs.countDocuments({}));


auditDb.runCommand({
  collMod: "stock_audit_logs",
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["product_id", "action", "quantity_change", "reason", "performed_by", "timestamp"],
      properties: {
        movement_id:     { bsonType: "number", description: "stock_movements.movement_id in MySQL" },
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
  },
  validationLevel: "moderate",
  validationAction: "error"
});
print("Validation rules added");


logs.createIndex({ product_id: 1 },                                 { name: "idx_product" });
logs.createIndex({ warehouse_id: 1 },                               { name: "idx_warehouse" });
logs.createIndex({ product_id: 1, warehouse_id: 1, timestamp: -1 }, { name: "idx_product_wh_time" });
logs.createIndex({ reason_category: 1, timestamp: -1 },             { name: "idx_reason_time" });
logs.createIndex({ movement_id: 1 },                                { name: "uq_movement_id", unique: true, sparse: true });

print("Indexes on stock_audit_logs:");
printjson(logs.getIndexes().map(function (i) { return i.name; }));


print("--- audit entries of product 1 (newest first) ---");
printjson(logs.find({ product_id: 1 },
                    { _id: 0, movement_id: 1, warehouse_id: 1, quantity_change: 1, reason: 1, timestamp: 1 })
              .sort({ timestamp: -1 }).limit(5).toArray());

print("--- adjustments in warehouse 4 that removed stock ---");
printjson(logs.find({ warehouse_id: 4, action: "STOCK_ADJUSTMENT", quantity_change: { $lt: 0 } },
                    { _id: 0, product_id: 1, quantity_change: 1, reason: 1 })
              .limit(5).toArray());

print("--- reorder level changes (policy) ---");
printjson(logs.find({ action: "REORDER_LEVEL_CHANGE" }, { _id: 0, product_id: 1, reason: 1, details: 1 }).toArray());

print("--- proof the index is used (look for IXSCAN) ---");
printjson(logs.find({ product_id: 1 }).explain("queryPlanner").queryPlanner.winningPlan);


print("--- units lost per reason category ---");
printjson(logs.aggregate([
  { $match: { action: "STOCK_ADJUSTMENT", quantity_change: { $lt: 0 } } },
  { $group: { _id: "$reason_category", entries: { $sum: 1 }, units_lost: { $sum: "$quantity_change" } } },
  { $sort: { units_lost: 1 } }
]).toArray());

print("--- adjustments per warehouse ---");
printjson(logs.aggregate([
  { $match: { action: "STOCK_ADJUSTMENT" } },
  { $group: { _id: "$warehouse_id", adjustments: { $sum: 1 }, net_change: { $sum: "$quantity_change" } } },
  { $sort: { _id: 1 } }
]).toArray());

