from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..models import Target
from ..db import get_session

from pydantic import BaseModel

router = APIRouter()

class TargetCreate(BaseModel):
    name: str
    slug: str
    region: str
    population: int = None
    enabled: bool = True

class TargetRead(BaseModel):
    id: int
    name: str
    slug: str
    region: str
    population: int = None
    enabled: bool
    created_at: str

    class Config:
        orm_mode = True

@router.post("/targets", response_model=TargetRead, status_code=status.HTTP_201_CREATED)
def create_target(target: TargetCreate, session: Session = Depends(get_session)):
    db_target = session.query(Target).filter(
        (Target.name == target.name) | (Target.slug == target.slug)
    ).first()
    if db_target:
        raise HTTPException(status_code=400, detail="Target already exists")
    new_target = Target(**target.dict())
    session.add(new_target)
    session.commit()
    session.refresh(new_target)
    return new_target

@router.get("/targets", response_model=List[TargetRead])
def list_targets(session: Session = Depends(get_session)):
    return session.query(Target).all()

@router.get("/targets/{id}", response_model=TargetRead)
def get_target(id: int, session: Session = Depends(get_session)):
    target = session.query(Target).get(id)
    if not target:
        raise HTTPException(status_code=404, detail="Target not found")
    return target

@router.delete("/targets/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_target(id: int, session: Session = Depends(get_session)):
    target = session.query(Target).get(id)
    if not target:
        raise HTTPException(status_code=404, detail="Target not found")
    session.delete(target)
    session.commit()

