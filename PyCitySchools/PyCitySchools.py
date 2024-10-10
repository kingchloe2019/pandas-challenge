#Dependencies and Setup
from pathlib import Path
import pandas as pd

#Load in Dataset of Schools
district_data_load = Path('/workspaces/PyCitySchools/schools_complete.csv')
district_data = pd.read_csv(district_data_load)

#Load in Dataset of Students
student_data_load = Path('/workspaces/PyCitySchools/students_complete.csv')
student_data = pd.read_csv(student_data_load)

#Combine datasets into one
complete_data = pd.merge(student_data, district_data, how = 'left', on = 'school_name')

# ------------------------------------------------------------------------------------------------------------------- #

#District Summary

#Total number of unique schools
schools_total = district_data['school_name'].count()
print('Total number of unique schools:', schools_total)
    
#Total students
students_total = district_data['size'].sum()
print('Total number of students:', students_total)

#Total Budget
budget_total = district_data['budget'].sum()
print('Total budget: $', budget_total)

#Average Math Score
avg_math_score = complete_data['math_score'].mean()
print('Average Math Score:', avg_math_score)

#Average Reading Score
avg_reading_score = complete_data['reading_score'].mean()
print('Average Reading Score:', avg_reading_score)

#% passing math
passing_math_count = complete_data[(complete_data["math_score"] >= 70)].count()["student_name"]
percent_passing_math = passing_math_count / float(students_total) * 100
print('Percent Passing Math: %', percent_passing_math)

#% passing reading
passing_reading_count = complete_data[(complete_data['reading_score'] >= 70)].count()['student_name']
percent_passing_reading = passing_reading_count / float(students_total) * 100
print('Percent Passing Reading: %', percent_passing_reading)

#% passing overall
passing_math_reading_count = complete_data[
    (complete_data["math_score"] >= 70) & (complete_data["reading_score"] >= 70)
].count()["student_name"]
overall_passing_rate = passing_math_reading_count /  float(students_total) * 100
print('Overall Passing Rate: %', overall_passing_rate)

#District Summary as a DataFrame
district_summary = pd.DataFrame({
    "Total Unique Schools": schools_total,
    "Total Students": students_total, 
    "Total Budget": budget_total,
    "Average Math Score": avg_math_score,
    "Average Reading Score": avg_reading_score,
    "% Passing Math": percent_passing_math,
    "% Passing Reading": percent_passing_reading,
    "% Overall Passing": overall_passing_rate
}, index = [0])

#Formatting
district_summary["Total Students"] = district_summary["Total Students"].map("{:,}".format)
district_summary["Total Budget"] = district_summary["Total Budget"].map("${:,.2f}".format)

#Display dataframe
display(district_summary)

# ------------------------------------------------------------------------------------------------------------------- #
#School Summary of Each School

#School types
school_types = district_data.set_index(["school_name"])["type"]

#List of School names
school_name_list = []

for name in complete_data['school_name']:
    if name not in school_name_list:
        school_name_list.append(name)

#Total Students Per School
students_per_school = district_data.set_index('school_name')['size']

#Total budget per school
budget_per_school = district_data.set_index('school_name')['budget']

#Per Student Budget
per_student_budget = budget_per_school/students_per_school

#Average Math Score per school
per_school_math = complete_data.groupby('school_name')['math_score'].mean()

#Average Reading Score per school
per_school_reading = complete_data.groupby('school_name')['reading_score'].mean()

# students with a passing reading score
students_passing_reading = complete_data[complete_data["reading_score"] >= 70]  # Filter for students passing reading

# Now per school
school_students_passing_reading = students_passing_reading.groupby(["school_name"])['student_name'].count()  # Group by school name and count

#students with a passing math score
students_passing_math = complete_data[complete_data["math_score"] >= 70]  # Filter for students passing reading

# Now per school
school_students_passing_math = students_passing_math.groupby(["school_name"])['student_name'].count()  # Group by school name and count

# Use the provided code to calculate the number of students per school that passed both math and reading with scores of 70 or higher
students_passing_math_and_reading = complete_data[
    (complete_data["reading_score"] >= 70) & (complete_data["math_score"] >= 70)]

school_students_passing_math_and_reading = students_passing_math_and_reading.groupby(["school_name"])['student_name'].count()

#percent passing math, per school
school_percent_passing_math = (school_students_passing_math / students_per_school) * 100

#percent passing reading, per school
school_percent_passing_reading = (school_students_passing_reading / students_per_school) * 100

#percent passing overall, per school
school_percent_passing_overall = (school_students_passing_math_and_reading / students_per_school) * 100

#store all of this in a dataframe
per_school_summary = pd.DataFrame({
'school_type': school_types,
'total_students': students_per_school,
'total_budget': budget_per_school,
'budget_per_student': per_student_budget, 
'avg_math_score': per_school_math,
'avg_reading_score': per_school_reading,
'percent_passing_math': school_percent_passing_math,
'percent_passing_reading': school_percent_passing_reading,
'percent_passing_overall': school_percent_passing_overall,

})

#nice formatting
per_school_summary["total_budget"] = per_school_summary["total_budget"].map("${:,.2f}".format)
per_school_summary["budget_per_student"] = per_school_summary["budget_per_student"].map("${:,.2f}".format)

#display the dataframe
display(per_school_summary)

# ------------------------------------------------------------------------------------------------------------------- #

#Highest Performing Schools by % overall passing
top_schools_by_passing = school_percent_passing_overall.sort_values(ascending = False).head(5)

#Saving into a df
top_schools = top_schools_by_passing.reset_index()
top_schools.columns = ['school_name', 'percent_passing_overall']
display(top_schools)


# ------------------------------------------------------------------------------------------------------------------- #

#Lowest Performing schools by % overall passing 

lowest_schools_by_passing = school_percent_passing_overall.sort_values(ascending = True).head(5)

bottom_schools = lowest_schools_by_passing.reset_index()
bottom_schools.columns = ['school_name', 'percent_passing_overall']
display(bottom_schools)

# ------------------------------------------------------------------------------------------------------------------- #
# Math Scores by Grade

#Separating Data by Grade
ninth_grade = complete_data[complete_data['grade'] == '9th']
tenth_grade = complete_data[complete_data['grade'] == '10th']
eleventh_grade = complete_data[complete_data['grade'] == '11th']
eleventh_grade = complete_data[complete_data['grade'] == '12th'] 

#calculate the mean math score for every grade, in each school
ninth_grade_math_avg = ninth_grade.groupby('school_name')['math_score'].mean().reset_index()
ninth_grade_math_avg['grade'] = '9th'

tenth_grade_math_avg = tenth_grade.groupby('school_name')['math_score'].mean().reset_index()
tenth_grade_math_avg['grade'] = '10th'

eleventh_grade_math_avg = eleventh_grade.groupby('school_name')['math_score'].mean().reset_index()
eleventh_grade_math_avg['grade'] = '11th'

twelfth_grade_math_avg = twelfth_grade.groupby('school_name')['math_score'].mean().reset_index()
twelfth_grade_math_avg['grade'] = '12th'

#Combine into a single df
math_scores_by_grade = pd.concat([ninth_grade_math_avg, tenth_grade_math_avg, eleventh_grade_math_avg, twelfth_grade_math_avg])

display(math_scores_by_grade)

# ------------------------------------------------------------------------------------------------------------------- #

#Reading Scores by grade

#calculate the mean score of reading for every school
ninth_grade_reading_avg = ninth_grade.groupby('school_name')['reading_score'].mean().reset_index()
ninth_grade_reading_avg['grade'] = '9th'

tenth_grade_reading_avg = tenth_grade.groupby('school_name')['reading_score'].mean().reset_index()
tenth_grade_reading_avg['grade'] = '10th'

eleventh_grade_reading_avg = eleventh_grade.groupby('school_name')['reading_score'].mean().reset_index()
eleventh_grade_reading_avg['grade'] = '11th'

twelfth_grade_reading_avg = twelfth_grade.groupby('school_name')['reading_score'].mean().reset_index()
twelfth_grade_reading_avg['grade'] = '12th'

#combine to a single df
reading_scores_by_grade = pd.concat([ninth_grade_reading_avg, tenth_grade_reading_avg, eleventh_grade_reading_avg, twelfth_grade_reading_avg])

display(reading_scores_by_grade)

# ------------------------------------------------------------------------------------------------------------------- #

#Scores by School Spending

#make a copy of school spending for later
school_spending_df = per_school_summary.copy()

#Spending Bins
spending_bins = [0, 585, 630, 645, 680]
labels = ["<$585", "$585-630", "$630-645", "$645-680"]

#divide budget by size
school_spending_df['spending_ranges_per_student'] = pd.cut(x = per_student_budget, bins = spending_bins, labels = labels)

# Convert Spending Ranges (Per Student) to a string
school_spending_df["spending_ranges_per_student"] = school_spending_df["spending_ranges_per_student"].astype(str)

#Calculate mean scores per spending range
spending_math_scores = school_spending_df.groupby(["spending_ranges_per_student"])["avg_math_score"].mean()
spending_reading_scores = school_spending_df.groupby(["spending_ranges_per_student"])["avg_reading_score"].mean()
spending_passing_math = school_spending_df.groupby(["spending_ranges_per_student"])["percent_passing_math"].mean()
spending_passing_reading = school_spending_df.groupby(["spending_ranges_per_student"])["percent_passing_reading"].mean()
overall_passing_spending = school_spending_df.groupby(["spending_ranges_per_student"])["percent_passing_overall"].mean()

#make a dataframe out of the above variables

spending_summary = pd.DataFrame({
'avg_math_score': spending_math_scores,
'avg_reading_score': spending_reading_scores,
'percent_passing_math': spending_passing_math,
'percent_passing_reading': spending_passing_reading,
'percent_passing_overall': overall_passing_spending
})

display(spending_summary)

# ------------------------------------------------------------------------------------------------------------------- #
#Scores by School Size

#Establish the bins
size_bins = [0, 1000, 2000, 5000]
size_labels = ["Small (<1000)", "Medium (1000-2000)", "Large (2000-5000)"]

## Create a copy of the school summary for later aggregations
school_size_df = per_school_summary.copy()

# Use `pd.cut` on the per_school_counts Series from earlier to categorize school size based on the bins.
school_size_df["school_size"] = pd.cut(x = students_per_school, bins = size_bins, labels = size_labels)

# Convert School Size to a string
school_size_df["school_size"] = school_size_df["school_size"].astype(str)
school_size_df

# Calculate averages for the desired columns.
size_math_scores = school_size_df.groupby(["school_size"])["avg_math_score"].mean()
size_reading_scores = school_size_df.groupby(["school_size"])["avg_reading_score"].mean()
size_passing_math = school_size_df.groupby(["school_size"])["percent_passing_math"].mean()
size_passing_reading = school_size_df.groupby(["school_size"])["percent_passing_reading"].mean()
size_overall_passing = school_size_df.groupby(["school_size"])["percent_passing_overall"].mean()

#Summary of size in a dataframe

size_summary = pd.DataFrame({
'avg_math_score': size_math_scores,
'avg_reading_score': size_reading_scores,
'percent_passing_math': size_passing_math,
'percent_passing_reading': size_passing_reading,
'percent_passing_overall': size_overall_passing
})

display(size_summary)

# ------------------------------------------------------------------------------------------------------------------- #

#Data based on School Types 

# Group the per_school_summary DataFrame by "School Type" and average the results.
average_math_score_by_type = per_school_summary.groupby(['school_type'])["avg_math_score"].mean()
average_reading_score_by_type = per_school_summary.groupby(['school_type'])["avg_reading_score"].mean()
average_percent_passing_math_by_type = per_school_summary.groupby(['school_type'])["percent_passing_math"].mean()
average_percent_passing_reading_by_type = per_school_summary.groupby(['school_type'])["percent_passing_reading"].mean()
average_percent_overall_passing_by_type = per_school_summary.groupby(['school_type'])["percent_passing_overall"].mean()

type_summary = pd.DataFrame({
"avg_math_score": average_math_score_by_type,
"avg_reading_score": average_reading_score_by_type,
"percent_passing_math": average_percent_passing_math_by_type,
"percent_passing_reading": average_percent_passing_reading_by_type,
"percent_passing_overall": average_percent_overall_passing_by_type
})

display(type_summary)

# ------------------------------------------------------------------------------------------------------------------- #

