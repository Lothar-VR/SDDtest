"""
API Router for Employee endpoints
"""
from fastapi import APIRouter

# Create router
router = APIRouter()


@router.get("/employees")
def list_employees():
    """
    Get all employees (non-deleted)
    """
    return {"items": [], "total": 0}


@router.post("/employees", status_code=201)
def create_employee():
    """
    Create a new employee
    """
    pass


@router.get("/employees/{employee_id}")
def get_employee(employee_id: int):
    """
    Get a specific employee by ID
    """
    pass


@router.put("/employees/{employee_id}")
def update_employee(employee_id: int):
    """
    Update entire employee record
    """
    pass


@router.patch("/employees/{employee_id}")
def partial_update_employee(employee_id: int):
    """
    Partially update employee record
    """
    pass


@router.delete("/employees/{employee_id}", status_code=204)
def delete_employee(employee_id: int):
    """
    Delete (soft delete) an employee
    """
    pass
