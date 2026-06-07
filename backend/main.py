import os
import psycopg2
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# load environment variable first
load_dotenv()

app = FastAPI(title="Library Dashboard API")

# enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# fetch conection string from .env
DATABASE_URL = os.getenv("DATABASE_URL")

try:
    # Pass the full URL directly to psycopg2
    connection = psycopg2.connect(DATABASE_URL)
except Exception as e:
    print(f"Database Connection Error: {e}")
    connection = None


@app.get("/api")
def api_home():
    return {"message": "Library Dashboard API is running"}


@app.get("/api/books")
def get_books():
    if not connection:
        raise HTTPException(status_code=500, detail="Database connection is unavailable")
    
    try:    
        # Using 'with' statements automatically closes the cursor safely
        with connection.cursor() as curs:
            curs.execute("""
                SELECT 
                    b.book_id,
                    b.title,
                    b.author,
                    c.category_name,
                    b.total_copies,
                    b.available_copies
                FROM books b
                JOIN categories c ON b.category_id = c.category_id
                ORDER BY b.book_id;
            """)
            rows = curs.fetchall()
            columns = [column[0] for column in curs.description]
            bookData = [dict(zip(columns, row)) for row in rows]
            return bookData
            
    except Exception as e:
        print(f"Query Error: {e}")
        # Always rollback the transaction if a query fails to prevent frozen connections
        if connection:
            connection.rollback()
        raise HTTPException(status_code=500, detail="Failed to fetch book data")


@app.get("/api/issues")
def get_issues():
    if not connection:
        raise HTTPException(status_code=500, detail="Database connection is unavailable")
    
    try:    
        # Using 'with' statements automatically closes the cursor safely
        with connection.cursor() as curs:
            curs.execute("""
                SELECT 
                    i.issue_id,
                    s.student_name,
                    s.department,
                    b.title,
                    c.category_name,
                    i.issue_date,
                    i.return_date,
                    i.status
                FROM issue i
                JOIN students s ON i.student_id = s.student_id
                JOIN books b ON i.book_id = b.book_id
                JOIN categories c ON b.category_id = c.category_id
                ORDER BY i.issue_date DESC;
            """)
            rows = curs.fetchall()
            columns = [column[0] for column in curs.description]
            issueData = [dict(zip(columns, row)) for row in rows]
            return issueData
            
    except Exception as e:
        print(f"Query Error: {e}")
        # Always rollback the transaction if a query fails to prevent frozen connections
        if connection:
            connection.rollback()
        raise HTTPException(status_code=500, detail="Failed to fetch issue data")


@app.get("/api/reports/books-by-category")
def books_by_category():
    if not connection:
        raise HTTPException(status_code=500, detail="Database connection is unavailable")
    
    try:    
        # Using 'with' statements automatically closes the cursor safely
        with connection.cursor() as curs:
            curs.execute("""
                SELECT 
                    c.category_name,
                    COUNT(b.book_id) AS total_books
                FROM categories c
                LEFT JOIN books b ON c.category_id = b.category_id
                GROUP BY c.category_name
                ORDER BY total_books DESC;
            """)
            rows = curs.fetchall()
            columns = [column[0] for column in curs.description]
            categoryData = [dict(zip(columns, row)) for row in rows]
            return categoryData
            
    except Exception as e:
        print(f"Query Error: {e}")
        # Always rollback the transaction if a query fails to prevent frozen connections
        if connection:
            connection.rollback()
        raise HTTPException(status_code=500, detail="Failed to fetch category data")


@app.get("/api/reports/issue-status")
def issue_status():
    if not connection:
        raise HTTPException(status_code=500, detail="Database connection is unavailable")
    
    try:    
        # Using 'with' statements automatically closes the cursor safely
        with connection.cursor() as curs:
            curs.execute("""
                SELECT 
                    status,
                    COUNT(*) AS total
                FROM issue
                GROUP BY status
                ORDER BY total DESC;
            """)
            rows = curs.fetchall()
            columns = [column[0] for column in curs.description]
            statusData = [dict(zip(columns, row)) for row in rows]
            return statusData
            
    except Exception as e:
        print(f"Query Error: {e}")
        # Always rollback the transaction if a query fails to prevent frozen connections
        if connection:
            connection.rollback()
        raise HTTPException(status_code=500, detail="Failed to fetch issue status data")


@app.get("/api/reports/top-students")
def top_students():
    if not connection:
        raise HTTPException(status_code=500, detail="Database connection is unavailable")
    
    try:    
        # Using 'with' statements automatically closes the cursor safely
        with connection.cursor() as curs:
            curs.execute("""
                SELECT 
                    s.student_name,
                    COUNT(i.issue_id) AS total_issued
                FROM students s
                JOIN issue i ON s.student_id = i.student_id
                GROUP BY s.student_name
                ORDER BY total_issued DESC
                LIMIT 5;
            """)
            rows = curs.fetchall()
            columns = [column[0] for column in curs.description]
            studentData = [dict(zip(columns, row)) for row in rows]
            return studentData
            
    except Exception as e:
        print(f"Query Error: {e}")
        # Always rollback the transaction if a query fails to prevent frozen connections
        if connection:
            connection.rollback()
        raise HTTPException(status_code=500, detail="Failed to fetch top students data")


@app.get("/api/reports/available-copies")
def available_copies():
    if not connection:
        raise HTTPException(status_code=500, detail="Database connection is unavailable")
    
    try:    
        # Using 'with' statements automatically closes the cursor safely
        with connection.cursor() as curs:
            curs.execute("""
                SELECT 
                    b.title,
                    c.category_name,
                    b.total_copies,
                    b.available_copies,
                    (b.total_copies - b.available_copies) AS issued_copies
                FROM books b
                JOIN categories c ON b.category_id = c.category_id
                ORDER BY issued_copies DESC;
            """)
            rows = curs.fetchall()
            columns = [column[0] for column in curs.description]
            copiesData = [dict(zip(columns, row)) for row in rows]
            return copiesData
            
    except Exception as e:
        print(f"Query Error: {e}")
        # Always rollback the transaction if a query fails to prevent frozen connections
        if connection:
            connection.rollback()
        raise HTTPException(status_code=500, detail="Failed to fetch available copies data")

@app.get("/api/dashboard/stats")
def get_dashboard_stats():
    if not connection:
        raise HTTPException(status_code=500, detail="Database connection is unavailable")
    
    try:    
        with connection.cursor() as curs:
            curs.execute("""
                SELECT 
                    (SELECT COUNT(*) FROM students) AS total_students,
                    (SELECT COUNT(*) FROM categories) AS total_categories,
                    (SELECT COALESCE(SUM(total_copies), 0) FROM books) AS total_books,
                    (SELECT COUNT(*) FROM issue) AS total_issued_records,
                    (SELECT COUNT(*) FROM issue WHERE status = 'Returned') AS returned_books,
                    (SELECT COUNT(*) FROM issue WHERE status = 'Returned' AND return_date > issue_date + INTERVAL '14 day') AS returned_late_books
                FROM (VALUES (1)) AS dummy;
            """)
            row = curs.fetchone()
            columns = [column[0] for column in curs.description]
            return dict(zip(columns, row))
            
    except Exception as e:
        print(f"Query Error: {e}")
        if connection:
            connection.rollback()
        raise HTTPException(status_code=500, detail="Failed to fetch dashboard statistics")


@app.get("/api/dashboard/details-table")
def get_dashboard_details_table():
    if not connection:
        raise HTTPException(status_code=500, detail="Database connection is unavailable")
    
    try:    
        with connection.cursor() as curs:
            curs.execute("""
                SELECT 
                    s.student_name,
                    s.department,
                    s.email,
                    b.title AS book_title,
                    c.category_name,
                    i.issue_date,
                    i.return_date,
                    i.status
                FROM issue i
                JOIN students s ON i.student_id = s.student_id
                JOIN books b ON i.book_id = b.book_id
                JOIN categories c ON b.category_id = c.category_id
                ORDER BY i.issue_date DESC;
            """)
            rows = curs.fetchall()
            columns = [column[0] for column in curs.description]
            return [dict(zip(columns, row)) for row in rows]
            
    except Exception as e:
        print(f"Query Error: {e}")
        if connection:
            connection.rollback()
        raise HTTPException(status_code=500, detail="Failed to fetch dashboard detailed table data")


# mount the static frontend files
app.mount("/", StaticFiles(directory="./frontend", html=True), name="frontend")
