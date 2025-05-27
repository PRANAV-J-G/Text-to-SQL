import sqlite3

# connections 
connection = sqlite3.connect("student.db")

# cursor connection to execute queries 
cursor = connection.cursor()

# create table 
table = '''
Create table STUDENT(NAME VARCHAR (25),CLASS VARCHAR(25),SECTION VARCHAR(25),MARKS INT);
'''
cursor.execute(table)

# List of student records to insert
students = [
    ("Alice Johnson", "10", "A", 89),
    ("Bob Smith", "10", "A", 76),
    ("Charlie Brown", "10", "B", 92),
    ("Diana Prince", "10", "B", 84),
    ("Ethan Hunt", "9", "A", 88),
    ("Fiona Gallagher", "9", "B", 91),
    ("George Wilson", "8", "C", 73),
    ("Hannah Lee", "8", "C", 95),
    ("Ian Somerhalder", "11", "A", 90),
    ("Julia Roberts", "11", "B", 85),
    ("Kevin Hart", "12", "C", 78),
    ("Laura Palmer", "12", "C", 82),
    ("Mike Tyson", "9", "A", 68),
    ("Nina Dobrev", "9", "B", 93),
    ("Oscar Isaac", "10", "C", 80),
    ("Pam Beesly", "10", "A", 86),
    ("Quentin Tarantino", "12", "B", 89),
    ("Rachel Green", "11", "A", 94),
    ("Steve Rogers", "12", "A", 96),
    ("Tina Fey", "11", "C", 87),
    ("Uma Thurman", "8", "A", 77),
    ("Victor Stone", "9", "C", 74),
    ("Wanda Maximoff", "10", "B", 91),
    ("Xander Cage", "11", "B", 79),
    ("Yara Shahidi", "12", "C", 83),
    ("Zayn Malik", "8", "B", 66),
    ("Amy Santiago", "10", "A", 88),
    ("Ben Wyatt", "10", "B", 92),
    ("Carla Espinosa", "9", "C", 81),
    ("Dexter Morgan", "9", "B", 90),
    ("Ellie Goulding", "12", "A", 87),
    ("Finn Wolfhard", "11", "C", 84),
    ("Ginny Weasley", "8", "A", 75),
    ("Harry Potter", "10", "C", 97),
    ("Isla Fisher", "12", "B", 89),
    ("Jack Sparrow", "11", "A", 65),
    ("Kendall Jenner", "9", "A", 90),
    ("Liam Hemsworth", "9", "C", 77),
    ("Monica Geller", "10", "B", 94),
    ("Noah Centineo", "11", "B", 86),
    ("Olivia Wilde", "12", "C", 88),
    ("Pablo Escobar", "10", "A", 69),
    ("Queen Latifah", "9", "B", 91),
    ("Ron Weasley", "10", "C", 85),
    ("Sansa Stark", "11", "C", 78),
    ("Tony Stark", "12", "A", 98),
    ("Ursula Buffay", "8", "B", 73),
    ("Violet Baudelaire", "9", "C", 92),
    ("Walter White", "10", "B", 89),
    ("Xena Warrior", "11", "A", 80),
    ("Yosemite Sam", "8", "C", 60),
    ("Zelda Fitzgerald", "12", "B", 83)
]

# Insert records
for student in students:
    cursor.execute("INSERT INTO STUDENT (NAME, CLASS, SECTION, MARKS) VALUES (?, ?, ?, ?)", student)

# Commit changes
connection.commit()

# Close connection
connection.close()
