
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI(title="Employee Management API")


class Employee(BaseModel):
    id: int
    name: str
    department: str
    designation: str
    salary: float
    city: str


employees: list[Employee] = []


@app.get("/")
def home():
    return {"message": "Employee Management API is running"}


@app.post("/employees", response_model=Employee, status_code=status.HTTP_201_CREATED)
def add_employee(employee: Employee):
    for emp in employees:
        if emp.id == employee.id:
            raise HTTPException(
                status_code=400,
                detail=f"Employee with id {employee.id} already exists"
            )

    employees.append(employee)
    return employee


@app.get("/employees", response_model=list[Employee])
def get_all_employees():
    return employees


@app.get("/employees/{employee_id}", response_model=Employee)
def get_employee(employee_id: int):
    for emp in employees:
        if emp.id == employee_id:
            return emp

    raise HTTPException(status_code=404, detail="Employee not found")


@app.put("/employees/{employee_id}", response_model=Employee)
def update_employee(employee_id: int, updated: Employee):
    for index, emp in enumerate(employees):
        if emp.id == employee_id:
            employees[index] = updated.model_copy(update={"id": employee_id})
            return employees[index]

    raise HTTPException(status_code=404, detail="Employee not found")


@app.delete("/employees/{employee_id}")
def delete_employee(employee_id: int):
    for index, emp in enumerate(employees):
        if emp.id == employee_id:
            employees.pop(index)
            return {"message": f"Employee {employee_id} deleted successfully"}

    raise HTTPException(status_code=404, detail="Employee not found")
