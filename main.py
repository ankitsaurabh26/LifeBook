from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException

import models, schemas
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)  # creates the table

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Habit tracker is running"}

@app.post("/habits", response_model=schemas.HabitOut)
def create_habit(habit: schemas.HabitCreate, db: Session = Depends(get_db)): 

    # API needs to communicate with MySQL. To do that, it needs a database session.
    # FastAPI provides a feature called Dependency Injection - db: Session = Depends(get_db)
    # Depends(get_db) automatically provides your API with a database session, so you don't have to create and close it manually in every endpoint.

    new_habit = models.Habit(name=habit.name, description=habit.description)

    db.add(new_habit) # I want to insert this object into the database when I commit the transaction
    # add() does not immediately save the record in MySQL. It adds the object to the current database session

    db.commit() # Save the transaction in MySQL

    db.refresh(new_habit) # When you insert a record, MySQL may automatically generate certain values. For example: id → Automatically generated primary key. SQLAlchemy reloads the object's database values so that generated or database-updated fields are available on the object

    # refresh() fetches the latest values of that particular record from MySQL and updates your Python object

    return new_habit

@app.get("/habits/{habit_id}", response_model=schemas.HabitOut)
def get_habit(habit_id: int, db: Session = Depends(get_db)):
    habit = db.query(models.Habit).filter(models.Habit.id == habit_id).first()
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    return habit


@app.patch("/habits/{habit_id}", response_model=schemas.HabitOut)
def update_habit(habit_id: int, data: schemas.HabitUpdate, db: Session = Depends(get_db)):
    habit = db.query(models.Habit).filter(models.Habit.id == habit_id).first()
    # .filter(models.Habit.id == habit_id) - Find the record where the database ID matches the ID received from the URL.
    # .first() - Returns the first matching record, If no matching record exists, it returns None

    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")

    for field, value in data.model_dump(exclude_unset=True).items():
        # model_dump() converts that Pydantic object into a normal Python dictionary
        # exclude_unset=True means include only the fields that the frontend actually provided
        # .items() retrieves the dictionary's key-value pairs

        setattr(habit, field, value)
        # setattr() - dynamically changes an object's attribute
        # setattr(habit, "description", "Read 20 pages daily") exactly equivalent to writing: habit.description = "Read 20 pages daily"


    db.commit()
    db.refresh(habit)
    return habit

# Example of getattr:

# class Habit:
#     def __init__(self):
#         self.name = "Reading"
#         self.description = "Read 10 pages daily"

# habit = Habit()

# name = getattr(habit, "name")

# print(name)

@app.delete("/habits/{habit_id}")
def delete_habit(habit_id: int, db: Session = Depends(get_db)):
    habit = db.query(models.Habit).filter(models.Habit.id == habit_id).first()
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")

    db.delete(habit)
    db.commit()
    return {"message": "Habit deleted"}