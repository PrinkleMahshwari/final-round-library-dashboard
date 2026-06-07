CREATE TABLE categories (
  category_id SERIAL PRIMARY KEY,
  category_name VARCHAR(50) NOT NULL
);

CREATE TABLE books (
  book_id SERIAL PRIMARY KEY,
  title VARCHAR(255) NOT NULL,
  author VARCHAR(50) NOT NULL,
  total_copies INT NOT NULL CHECK(total_copies >= 0),
  available_copies INT NOT NULL CHECK(available_copies >= 0)
  CHECK(available_copies <= total_copies),
  category_id int REFERENCES categories(category_id) NOT NULL
);

CREATE TABLE students (
  student_id SERIAL PRIMARY KEY,
  student_name VARCHAR(50) NOT NULL,
  department VARCHAR(50) NOT NULL,
  email VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE issue (
  issue_id SERIAL PRIMARY KEY,
  issue_date DATE NOT NULL,
  return_date DATE NOT NULL,
  status VARCHAR(15) NOT NULL CHECK(status IN ('ISSUED', 'RETURNED', 'LATE')),
  student_id INT REFERENCES students(student_id) NOT NULL,
  book_id INT REFERENCES books(book_id) NOT NULL
);
