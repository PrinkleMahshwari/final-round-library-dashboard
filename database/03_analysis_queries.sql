-- Books by Category
SELECT
c.category_name,
COUNT(b.book_id) AS total_books
FROM categories c
LEFT JOIN books b ON c.category_id = b.category_id
GROUP BY c.category_name
ORDER BY total_books DESC;

-- Issue Status Count
SELECT 
status,
COUNT(*) AS total
FROM issue
GROUP BY status
ORDER BY total DESC;

-- Top students by Issued Books
SELECT 
s.student_name,
COUNT(i.issue_id) AS total_issued
FROM students s 
JOIN issue i on s.student_id = i.student_id
GROUP BY s.student_name
ORDER BY total_issued DESC
LIMIT 5;

-- Complete issue report
SELECT
i.issue_id,
s.student_name,
s.department,
s.email,
b.title,
c.category_name,
i.issue_date,
i.return_date,
i.status
FROM issue i 
JOIN students s ON s.student_id = i.student_id
JOIN books b ON b.book_id = i.book_id
JOIN categories c on c.category_id = b.category_id
ORDER BY i.issue_date DESC;

-- Available Copies Report
SELECT
b.title,
c.category_name,
b.total_copies,
b.available_copies,
(b.total_copies - b.available_copies) AS issued_copies
FROM books b
JOIN categories c ON b.category_id = c.category_id
ORDER BY issued_copies DESC;

