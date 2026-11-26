
import csv


# Read employee data
with open("data/employees.csv", "r") as file:
    employees = list(csv.DictReader(file))


# 1. Bonus function using *args and **kwargs
def bonus(salary, rate=0.1, *extras, **options):
    result = salary * rate + sum(extras)

    if "cap" in options:
        result = min(result, options["cap"])

    return result


print("Bonus:", bonus(50000, 0.1, 1000, 500, cap=6000))


# 2. Custom exception
class InvalidSalaryError(Exception):
    pass


# 3. Employee class
class Employee:
    def __init__(self, name, salary):
        if salary < 0:
            raise InvalidSalaryError(f"Invalid salary: {salary}")

        self.name = name
        self.salary = salary

    def annual_salary(self):
        return self.salary * 12

    def get_details(self):
        return f"Name: {self.name}, Salary: {self.salary}"


# 4. Manager inheritance
class Manager(Employee):
    def __init__(self, name, salary, team_size):
        super().__init__(name, salary)
        self.team_size = team_size

    def get_details(self):
        return (
            f"Name: {self.name}, Salary: {self.salary}, "
            f"Team Size: {self.team_size}"
        )


# 5. Test Employee and Manager
emp = Employee("Arun", 30000)
print("Annual Salary:", emp.annual_salary())

manager = Manager("Priya", 60000, 5)
print("Manager Details:", manager.get_details())


# 6. Exception handling
try:
    employee = Employee("Test", -500)
except InvalidSalaryError as error:
    print("Error:", error)
finally:
    print("Transaction finished")


# 7. List comprehension
high_salary = [
    emp["name"]
    for emp in employees
    if int(emp["salary"]) > 50000
]

print("Above 50000:", high_salary)


# 8. Map and lambda - 10% salary raise
updated_salaries = list(
    map(lambda emp: round(int(emp["salary"]) * 1.10, 2), employees)
)

print("Updated Salaries:", updated_salaries)


# 9. Filter Chennai employees
chennai_employees = list(
    filter(lambda emp: emp["city"] == "Chennai", employees)
)

print("Chennai:", [emp["name"] for emp in chennai_employees])


# 10. Continue and break
print("Loop demonstration:")

for emp in employees:
    salary = int(emp["salary"])

    if salary == 0:
        continue

    if salary > 85000:
        print("First salary above 85000:", emp["name"])
        break

    print(emp["name"], salary)
