import psycopg2
from psycopg2 import sql
from json import loads

# Replace these values with your actual database credentials
dbname = "prof_rec_sample_data"
user = "anirudhnukala"
password = "sample_data"
host = "localhost"
port = "5432"

# Replace these values with your actual table and column names
table_name = "my_table"
column_name = "course"

# Establish a connection to the database


def get_course_info(user_input):
    
    connection = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )
    
    search_value = f"{user_input['dept']} {user_input['number']}"
    # Create a cursor object to execute SQL queries
    cursor = connection.cursor()

    # Build the SQL query to select data based on the column
    query = sql.SQL("SELECT * FROM {} WHERE {} = %s;").format(
        sql.Identifier(table_name),
        sql.Identifier(column_name)
    )

    # Execute the query with the specified search value
    cursor.execute(query, (search_value,))

    # Fetch all the results
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    
    courses = []
    for row in results:
        dict = {
   	        "GPA": {
            },
 	        "GradesPercentage": {
      	        "A": float(row[9]),
                "B": float(row[10]),
                "C": float(row[11]),
  	            "D": float(row[12]),
                "F": float(row[13])
 	        },
            "Professor": {
                "Course": row[2],
                "Difficulty": float(row[15]),
                "Name": row[1],
     	        "Num_Ratings": float(row[17]),
                "Rating": float(row[14]),
  	            "Would Take Again": float(row[16])
      	    }
	    }
    
        if row[4] is not None:
            dict["GPA"][row[3]] = float(row[4])
        if row[6] is not None:
            dict["GPA"][row[5]] = float(row[6])
        if row[8] is not None:
            dict["GPA"][row[7]] = float(row[8])
    
        courses.append(dict)
    
    return courses


def get_prof_info(user_input):
    
    connection = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )
    
    search_course = f"{user_input['dept']} {user_input['number']}"
    print(search_course)
    search_prof = user_input['professor']
    print(search_prof)
    # Create a cursor object to execute SQL queries
    cursor = connection.cursor()

    # Build the SQL query to select data based on the column
    query = sql.SQL("SELECT * FROM {} WHERE {} = %s AND {} = %s;").format(
        sql.Identifier(table_name),
        sql.Identifier("course"),
        sql.Identifier("professor")
    )

    # Execute the query with the specified search value
    cursor.execute(query, (search_course, search_prof))

    # Fetch all the results
    row = cursor.fetchone()
    cursor.close()
    connection.close()
    
    print(row)
    
    dict = {
        "GPA": {
        },
        "GradesPercentage": {
            "A": float(row[9]),
            "B": float(row[10]),
            "C": float(row[11]),
            "D": float(row[12]),
            "F": float(row[13])
 	    },
        "Professor": {
            "Course": row[2],
            "Difficulty": float(row[15]),
            "Name": row[1],
     	    "Num_Ratings": float(row[17]),
            "Rating": float(row[14]),
  	        "Would Take Again": float(row[16])
        }
	}
    
    if row[4] is not None:
        dict["GPA"][row[3]] = float(row[4])
    if row[6] is not None:
        dict["GPA"][row[5]] = float(row[6])
    if row[8] is not None:
        dict["GPA"][row[7]] = float(row[8])

    print(dict)
    return dict
    

def check_data(data):
    
    user_input = loads(data)

    if(user_input['dept'] == ""):
        return 'invalid department'
    elif(user_input['number'] == ""):
        return 'invalid number'
    
    if(user_input['professor'] == ""):
        # return 'getting course info'
        return get_course_info(user_input)
    else:
        # return 'getting prof info'
        print(user_input)
        return get_prof_info(user_input)





