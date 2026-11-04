
from pathlib import Path
import numpy as np
import pandas as pd

BASE = Path(__file__).resolve().parent
INPUT, OUTPUT = BASE / "input", BASE / "output"
OUTPUT.mkdir(exist_ok=True)
log = []                                   


def note(msg):
    print(msg)
    log.append(msg)



students    = pd.read_csv(INPUT / "students.csv")
courses     = pd.read_csv(INPUT / "courses.csv")
enrollments = pd.read_csv(INPUT / "enrollments.csv")
df          = pd.read_csv(INPUT / "progress.csv")         

note(f"students={len(students)}  courses={len(courses)}  enrollments={len(enrollments)}  progress={len(df)}")
print("\nFirst rows of progress:\n", df.head(), "\n")




students["full_name"] = students["full_name"].astype("string").str.strip()
bad_names = students["full_name"].isna() | (students["full_name"] == "")
note(f"Students with missing names removed : {int(bad_names.sum())}")
students = students[~bad_names].drop_duplicates("student_id")

enrollments["enrollment_date"] = pd.to_datetime(enrollments["enrollment_date"],
                                                format="%Y-%m-%d", errors="coerce")
bad_dates = enrollments["enrollment_date"].isna()
note(f"Enrollments with invalid dates removed: {int(bad_dates.sum())}")
enrollments = enrollments[~bad_dates].drop_duplicates("enrollment_id")

before = len(df)
df = df.drop_duplicates()
note(f"Duplicate progress rows removed       : {before - len(df)}")


df["completion"] = (df["completion"].astype("string")
                    .str.replace("%", "", regex=False)
                    .pipe(pd.to_numeric, errors="coerce"))

note(f"Missing completion values set to 0    : {int(df['completion'].isna().sum())}")
df["completion"] = df["completion"].fillna(0)


out_of_range = int(((df["completion"] < 0) | (df["completion"] > 100)).sum())
note(f"Out-of-range values clipped to 0-100  : {out_of_range}")
df["completion"] = np.clip(df["completion"], 0, 100)


df["last_updated"] = pd.to_datetime(df["last_updated"], errors="coerce")
bad_upd = df["last_updated"].isna()
note(f"Rows with invalid last_updated removed: {int(bad_upd.sum())}")
df = df[~bad_upd]

enrollments = enrollments[enrollments["student_id"].isin(students["student_id"])
                          & enrollments["course_id"].isin(courses["course_id"])]
df = df[df["enrollment_id"].isin(enrollments["enrollment_id"])]
note(f"Clean rows -> students={len(students)}, enrollments={len(enrollments)}, progress={len(df)}")


note("\n=== 3. NUMPY AVERAGE PROGRESS ===")
avg_progress = np.mean(df["completion"].to_numpy())
note(f"Overall average progress : {avg_progress:.2f}%")
note(f"Median progress          : {np.median(df['completion'].to_numpy()):.2f}%")
note(f"Std deviation            : {np.std(df['completion'].to_numpy()):.2f}")

note("\n4. PANDAS COURSE-LEVEL AVERAGES")
summary = df.groupby("course_id")["completion"].mean()          
print(summary, "\n")

report = (summary.round(2).rename("avg_completion_pct").reset_index()
          .merge(courses[["course_id", "course_name"]], on="course_id")
          .sort_values("avg_completion_pct", ascending=False)
          [["course_id", "course_name", "avg_completion_pct"]])
note(report.to_string(index=False))


students.to_csv(OUTPUT / "students_clean.csv", index=False)
courses.to_csv(OUTPUT / "courses.csv", index=False)
enrollments.to_csv(OUTPUT / "enrollments_clean.csv", index=False)
df.to_csv(OUTPUT / "progress_clean.csv", index=False)
report.to_csv(OUTPUT / "course_level_averages.csv", index=False)
(OUTPUT / "cleaning_report.txt").write_text("\n".join(log), encoding="utf-8")
note(f"\nSaved all files to: {OUTPUT}")
