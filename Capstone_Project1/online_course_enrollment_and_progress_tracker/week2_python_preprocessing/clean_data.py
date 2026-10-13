
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW, CLEAN = ROOT / "data" / "raw", ROOT / "data" / "clean"
CLEAN.mkdir(parents=True, exist_ok=True)


students    = pd.read_csv(RAW / "students.csv")
courses     = pd.read_csv(RAW / "courses.csv")
enrollments = pd.read_csv(RAW / "enrollments.csv")
progress    = pd.read_csv(RAW / "progress.csv")
print("Loaded rows:", len(students), len(courses), len(enrollments), len(progress))


students["full_name"] = students["full_name"].astype("string").str.strip()
bad_names = students["full_name"].isna() | (students["full_name"] == "")
print("Students with missing names removed:", int(bad_names.sum()))
students = students[~bad_names].drop_duplicates("student_id")


enrollments["enrollment_date"] = pd.to_datetime(enrollments["enrollment_date"],
                                                format="%Y-%m-%d", errors="coerce")
bad_dates = enrollments["enrollment_date"].isna()
print("Enrollments with invalid dates removed:", int(bad_dates.sum()))
enrollments = enrollments[~bad_dates].drop_duplicates("enrollment_id")

# progress: duplicates, "85%" strings, missing, out of range
before = len(progress)
progress = progress.drop_duplicates()
print("Duplicate progress rows removed:", before - len(progress))
progress["completion"] = (progress["completion"].astype("string")
                          .str.replace("%", "", regex=False)
                          .pipe(pd.to_numeric, errors="coerce"))
print("Missing completion values filled with 0:", int(progress["completion"].isna().sum()))
progress["completion"] = progress["completion"].fillna(0)
progress["completion"] = np.clip(progress["completion"], 0, 100)      # keep within 0-100
progress["last_updated"] = pd.to_datetime(progress["last_updated"], errors="coerce")
progress = progress.dropna(subset=["last_updated"])


enrollments = enrollments[enrollments["student_id"].isin(students["student_id"])
                          & enrollments["course_id"].isin(courses["course_id"])]
progress = progress[progress["enrollment_id"].isin(enrollments["enrollment_id"])]


avg_progress = np.mean(progress["completion"].to_numpy())
print(f"\nOverall average progress (NumPy): {avg_progress:.2f}%")


summary = progress.groupby("course_id")["completion"].mean().round(2)
report = (summary.rename("avg_completion_pct").reset_index()
          .merge(courses[["course_id", "course_name"]], on="course_id")
          .sort_values("avg_completion_pct", ascending=False))
print("\nAverage completion by course:\n", report.to_string(index=False))

students.to_csv(CLEAN / "students_clean.csv", index=False)
courses.to_csv(CLEAN / "courses.csv", index=False)
enrollments.to_csv(CLEAN / "enrollments_clean.csv", index=False)
progress.to_csv(CLEAN / "progress_clean.csv", index=False)
report.to_csv(CLEAN / "course_level_averages.csv", index=False)
print("\nSaved cleaned files to", CLEAN)
