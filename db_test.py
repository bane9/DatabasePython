import sys
sys.path.append('DataManager')

from DataDistributor import DataDistributor

data = DataDistributor()

#data.new("sequential")
data.connect_to_sql("127.0.0.1", "root", "pass")

metadata = {
    "database_names" : [
        "students",
        "failed_subjects",
        "passed_subjects"
    ],
    "database_column_names" : [
        ["index_no", "name"],
        ["index_no", "name", "silabus", "grade"],
        ["index_no", "name", "silabus", "failed_amount"]
    ],
    "search_combine_columns" : [
		[0],
		[0, 1],
		[0, 1]
	],
    "schema_name" : "uni_proj"
}


data.set_metadata(metadata)

data.db.schema_init()

student_tpl = [["222555666", "John Doe"]]
passed_subject_tpl = [["222555666", "passed_subject_1", "silabus1", "10"], ["222555666", "passed_subject_2", "silabus1", "7"]]
failed_subject_tpl = [["222555666", "failed_subject_01", "silabus01", "2"], ["222555666", "failed_subject_02", "silabus02", "2"]]  

for x in student_tpl:
    data.db.add(x, 0)

for x in passed_subject_tpl:
    data.db.add(x, 1)

for x in failed_subject_tpl:
    data.db.add(x, 2)

data.db.save("", "asd")

target = 1

print(data.db.get(target, index_no="222555666"))

data.db.delete(target, index_no="222555666", name="passed_subject_2")

print(data.db.get(target, index_no="222555666"))

data.db.modify(target, ["222555666", "passed_subject_1", "silabus3", "30"], index_no="222555666", name="passed_subject_1")

print(data.db.get(target, index_no="222555666"))

data.db.load("asd_metadata.json")
