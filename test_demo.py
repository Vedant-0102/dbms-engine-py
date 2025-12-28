"""
Demo script to test the database engine functionality
"""
from engine import DatabaseEngine


def run_demo():
    print("=" * 60)
    print("Mini Database Engine - Demo")
    print("=" * 60)
    
    engine = DatabaseEngine()
    
    commands = [
        ("CREATE TABLE students (id, name, age)", "Creating students table..."),
        ("INSERT INTO students VALUES (1, 'Alice', 20)", "Inserting Alice..."),
        ("INSERT INTO students VALUES (2, 'Bob', 22)", "Inserting Bob..."),
        ("INSERT INTO students VALUES (3, 'Charlie', 19)", "Inserting Charlie..."),
        ("SELECT * FROM students", "Selecting all students..."),
        ("SELECT name, age FROM students", "Selecting name and age..."),
        ("SELECT * FROM students WHERE age = 20", "Selecting students with age 20..."),
        ("UPDATE students SET age = 21 WHERE name = Alice", "Updating Alice's age..."),
        ("SELECT * FROM students", "Viewing updated data..."),
        ("DELETE FROM students WHERE id = 2", "Deleting Bob..."),
        ("SELECT * FROM students", "Final data..."),
    ]
    
    for command, description in commands:
        print(f"\n{description}")
        print(f"SQL> {command}")
        try:
            result = engine.execute(command)
            if result:
                print(result)
        except Exception as e:
            print(f"Error: {e}")
    
    print("\n" + "=" * 60)
    print("Demo completed!")
    print("=" * 60)


if __name__ == "__main__":
    run_demo()
