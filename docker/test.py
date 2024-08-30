# import psycopg2

# def insert_employee(name, age, department, salary):
#     try:
#         connection = psycopg2.connect(
#             user="postgres",
#             password="xyz",
#             host="localhost",
#             port="15432",
#             database="postgres"
#         )
#         cursor = connection.cursor()
        
#         insert_query = '''
#         INSERT INTO employees (name, age, department, salary)
#         VALUES (%s, %s, %s, %s)
#         '''
#         cursor.execute(insert_query, (name, age, department, salary))
        
#         connection.commit()
#         print("Employee inserted successfully")
    
#     except (Exception, psycopg2.Error) as error:
#         print("Error while inserting data", error)
    
#     finally:
#         if cursor is not None:
#             cursor.close()
#         if connection is not None:
#             connection.close()

# def read_employees():
#     try:
#         connection = psycopg2.connect(
#             user="postgres",
#             password="xyz",
#             host="localhost",
#             port="15432",
#             database="postgres"
#         )
#         cursor = connection.cursor()
        
#         select_query = "SELECT * FROM employees"
#         cursor.execute(select_query)
        
#         employees = cursor.fetchall()
#         for emp in employees:
#             print(f"ID: {emp[0]}, Name: {emp[1]}, Age: {emp[2]}, Department: {emp[3]}, Salary: {emp[4]}")
    
#     except (Exception, psycopg2.Error) as error:
#         print("Error while reading data", error)
    
#     finally:
#         if cursor is not None:
#             cursor.close()
#         if connection is not None:
#             connection.close()

# def query_employees_by_department(department):
#     try:
#         connection = psycopg2.connect(
#             user="postgres",
#             password="xyz",
#             host="localhost",
#             port="15432",
#             database="postgres"
#         )
#         cursor = connection.cursor()
        
#         query = '''
#         SELECT * FROM employees WHERE department = %s
#         '''
#         cursor.execute(query, (department,))
        
#         employees = cursor.fetchall()
#         for emp in employees:
#             print(f"ID: {emp[0]}, Name: {emp[1]}, Age: {emp[2]}, Department: {emp[3]}, Salary: {emp[4]}")
    
#     except (Exception, psycopg2.Error) as error:
#         print("Error while querying data", error)
    
#     finally:
#         if cursor is not None:
#             cursor.close()
#         if connection is not None:
#             connection.close()

# def update_employee_salary(employee_id, new_salary):
#     try:
#         connection = psycopg2.connect(
#             user="postgres",
#             password="xyz",
#             host="localhost",
#             port="15432",
#             database="postgres"
#         )
#         cursor = connection.cursor()
        
#         update_query = '''
#         UPDATE employees SET salary = %s WHERE id = %s
#         '''
#         cursor.execute(update_query, (new_salary, employee_id))
        
#         connection.commit()
#         print(f"Employee ID {employee_id} salary updated to {new_salary}")
    
#     except (Exception, psycopg2.Error) as error:
#         print("Error while updating data", error)
    
#     finally:
#         if cursor is not None:
#             cursor.close()
#         if connection is not None:
#             connection.close()

# def delete_employee(employee_id):
#     try:
#         connection = psycopg2.connect(
#             user="postgres",
#             password="xyz",
#             host="localhost",
#             port="15432",
#             database="postgres"
#         )
#         cursor = connection.cursor()
        
#         delete_query = '''
#         DELETE FROM employees WHERE id = %s
#         '''
#         cursor.execute(delete_query, (employee_id,))
        
#         connection.commit()
#         print(f"Employee ID {employee_id} deleted successfully")
    
#     except (Exception, psycopg2.Error) as error:
#         print("Error while deleting data", error)
    
#     finally:
#         if cursor is not None:
#             cursor.close()
#         if connection is not None:
#             connection.close()

# insert_employee("John Doe", 30, "Robotics Engineering", 750000)
# insert_employee("Peter Doe", 31, "Software Engineering", 750000)
# insert_employee("Sally Doe", 32, "Engineering", 750000)
# read_employees()
# query_employees_by_department("Engineering")
# update_employee_salary(1, 80000)
# delete_employee(1)