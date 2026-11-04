
db = db.getSiblingDB("course_tracker");

db.feedback.countDocuments();
db.feedback.find().limit(3);


db.feedback.insertOne({
  student_id: 1, course_id: 2, rating: 5,
  comment: "Very clear SQL course", reviewed_on: "2025-10-01"
});


db.feedback.createIndex({ student_id: 1 }, { name: "idx_student" });
db.feedback.createIndex({ course_id: 1 },  { name: "idx_course" });
db.feedback.createIndex({ course_id: 1, rating: 1 }, { name: "idx_course_rating" });
db.feedback.getIndexes();

db.feedback.find({ student_id: 1 }, { _id: 0 });                 
db.feedback.find({ course_id: 2 }, { _id: 0 }).limit(5);       
db.feedback.find({ rating: { $gte: 4 } }).limit(5);             


db.feedback.aggregate([
  { $group: { _id: "$course_id", avg_rating: { $avg: "$rating" }, reviews: { $sum: 1 } } },
  { $sort: { avg_rating: -1 } }
]);


db.feedback.find({ student_id: 1 }).explain("executionStats").queryPlanner.winningPlan;


db.feedback.updateOne({ student_id: 1, course_id: 2 }, { $set: { rating: 4 } });
db.feedback.deleteMany({ rating: { $lt: 2 } });
