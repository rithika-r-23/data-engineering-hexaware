
import json
from pathlib import Path
from pymongo import MongoClient, ASCENDING

FEEDBACK_FILE = Path(__file__).resolve().parents[2] / "data" / "feedback.json"

client = MongoClient("mongodb://localhost:27017", serverSelectionTimeoutMS=3000)
col = client["course_tracker"]["feedback"]


col.drop()
docs = json.loads(FEEDBACK_FILE.read_text(encoding="utf-8"))
col.insert_many(docs)
print(f"Inserted {col.count_documents({})} feedback documents")


col.insert_one({"student_id": 1, "course_id": 2, "rating": 5,
                "comment": "Very clear SQL course", "reviewed_on": "2025-10-01"})


col.create_index([("student_id", ASCENDING)], name="idx_student")
col.create_index([("course_id", ASCENDING)], name="idx_course")
col.create_index([("course_id", ASCENDING), ("rating", ASCENDING)], name="idx_course_rating")
print("Indexes:", [i["name"] for i in col.list_indexes()])


print("\nReviews by student 1:")
for d in col.find({"student_id": 1}, {"_id": 0}): print(" ", d)

print("\nAverage rating per course:")
for r in col.aggregate([
        {"$group": {"_id": "$course_id", "avg_rating": {"$avg": "$rating"}, "reviews": {"$sum": 1}}},
        {"$sort": {"avg_rating": -1}}]):
    print(f"  course {r['_id']:>2}: {r['avg_rating']:.2f} ({r['reviews']} reviews)")


col.update_one({"student_id": 1, "course_id": 2}, {"$set": {"rating": 4}})
col.delete_many({"rating": {"$lt": 2}})
print("\nDone.")
