"""
Pydantic schemas for Employee entity
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class EmployeeCreate(BaseModel):
    """Schema for creating a new employee"""
    name: str = Field(..., min_length=1, max_length=255, description="Employee name")
    email: EmailStr = Field(..., max_length=255, description="Employee email (unique)")
    department: str = Field(..., min_length=1, max_length=100, description="Department name")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "田中太郎",
                "email": "taro@example.com",
                "department": "営業部"
            }
        }


class EmployeeRead(BaseModel):
    """Schema for reading employee data (response)"""
    id: int
    name: str
    email: str
    department: str
    is_deleted: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "田中太郎",
                "email": "taro@example.com",
                "department": "営業部",
                "is_deleted": False,
                "created_at": "2026-04-03T10:00:00Z",
                "updated_at": "2026-04-03T10:00:00Z"
            }
        }


class EmployeeUpdateFull(BaseModel):
    """Schema for full update (PUT) of employee"""
    name: str = Field(..., min_length=1, max_length=255)
    email: EmailStr = Field(..., max_length=255)
    department: str = Field(..., min_length=1, max_length=100)

    class Config:
        json_schema_extra = {
            "example": {
                "name": "田中太郎",
                "email": "taro@example.com",
                "department": "営業部"
            }
        }


class EmployeeUpdatePartial(BaseModel):
    """Schema for partial update (PATCH) of employee"""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    email: Optional[EmailStr] = Field(None, max_length=255)
    department: Optional[str] = Field(None, min_length=1, max_length=100)

    class Config:
        json_schema_extra = {
            "example": {
                "department": "企画部"
            }
        }
