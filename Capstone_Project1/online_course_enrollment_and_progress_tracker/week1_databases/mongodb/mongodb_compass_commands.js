// Week 1 - MongoDB commands for MongoDB Compass
// HOW TO USE: In Compass click ">_ MONGOSH" at the bottom-left, paste ONE block at a time, press Enter.
// Prerequisite: feedback.json already imported into course_tracker > feedback (see README).

// ---------- 0. Select the database ----------
db = db.getSiblingDB("course_tracker");

// ---------- 1. Check the imported data (expected: 200) ----------
db.feedback.countDocuments();
db.feedback.find().limit(3);

// ---------- 2. CREATE: add a new feedback document ----------
db.feedback.insertOne({
  student_id: 1, course_id: 2, rating: 5,
  comment: "Very clear SQL course", reviewed_on: "2025-10-01"
});

// ---------- 3. INDEXES: search by student or course quickly ----------
db.feedback.createIndex({ student_id: 1 }, { name: "idx_student" });
db.feedback.createIndex({ course_id: 1 },  { name: "idx_course" });
db.feedback.createIndex({ course_id: 1, rating: 1 }, { name: "idx_course_rating" });
db.feedback.getIndexes();

// ---------- 4. READ: queries ----------
db.feedback.find({ student_id: 1 }, { _id: 0 });                 // reviews by one student
db.feedback.find({ course_id: 2 }, { _id: 0 }).limit(5);         // reviews for one course
db.feedback.find({ rating: { $gte: 4 } }).limit(5);              // good reviews

// Average rating per course
db.feedback.aggregate([
  { $group: { _id: "$course_id", avg_rating: { $avg: "$rating" }, reviews: { $sum: 1 } } },
  { $sort: { avg_rating: -1 } }
]);

// ---------- 5. Prove the indexes are used ----------
db.feedback.find({ student_id: 1 }).explain("executionStats").queryPlanner.winningPlan;

// ---------- 6. UPDATE / DELETE ----------
db.feedback.updateOne({ student_id: 1, course_id: 2 }, { $set: { rating: 4 } });
db.feedback.deleteMany({ rating: { $lt: 2 } });
