import sys
sys.path.append('DataManager')

from DataDistributor import DataDistributor

data = DataDistributor()

data.new("serial")

metadata = {
    "databases" : 3,
    "database_column_names" : [
        ["index_no", "name"],
        ["index_no", "name, silabus, grade"],
        ["index_no", "name, silabus, failed_amount"]
    ],
    "search_combine_columns" : [
		[0],
		[0, 1],
		[0, 1]
	]
}

data.set_metadata(metadata)

student_tpl = [["222555666", "John Doe"]]
passed_subject_tpl = [["0", "passed_subject_1", "silabus1", "10"], ["222555666", "passed_subject_2", "silabus1", "7"]]
failed_subject_tpl = [["0", "failed_subject_01", "silabus01", "2"], ["222555666", "failed_subject_02", "silabus02", "2"]]  

for x in student_tpl:
    data.db.add(x, 0)

for x in passed_subject_tpl:
    data.db.add(x, 1)

for x in failed_subject_tpl:
    data.db.add(x, 2)

data.db.save("", "asd")

print(data.db.get("222555666", 0))

data.db.delete("222555666", 0)

data.db.load("asd_metadata.json")

print(data.db.search_all_keys("222555666"))
