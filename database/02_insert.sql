INSERT INTO categories (category_name) VALUES 
  ('Thriller'),
  ('RomCom'),
  ('SciFi'),
  ('Academic'),
  ('Biography'),
  ('History'),
  ('Current Affair'),
  ('Adventure');

INSERT INTO books (title, author, total_copies, available_copies, category_id) VALUES
  ('The Silent Patient', 'Alex Michalides', 10, 7, 1),
  ('Gone Girl', 'Gillian Flynn', 8, 4, 1),
  ('The Hating Game', 'Sally Throne', 6, 5, 2),
  ('Book Lovers', 'Emily Henry', 7, 3, 2),
  ('Dune', 'Frank Herbert', 15, 11, 3),
  ('Project Hail Mary', 'Andy Weir', 12, 9, 3),
  ('Introudction to Algorithms', 'Thomas H. Cormen', 5, 2, 4),
  ('A Brief History of Time', 'Stephen Hawking', 8, 6, 4),
  ('Steve Jobs', 'Walter Isaacson', 6, 4, 5),
  ('I know Why the Caged Bird sings', 'Maya Angelou', 5, 5, 5),
  ('Sapies: A Brief History of HumanKind', 'Yuval Noah Harai', 14, 10, 6),
  ('The Guns of August', 'Barbara W. Tuchman', 4, 1, 6),
  ('The Room Where It Happened', 'John Bolton', 5, 3, 7),
  ('Fear: Trump in the White House', 'Bob Woodward', 6, 2, 7),
  ('The Hobbit', 'J.R.R. Tolkien', 20, 16, 8),
  ('Into the Wild', 'Jon Krakauer', 9, 6, 8);

INSERT INTO students(student_name, department, email) VALUES
  ('Abdul Wasiq', 'BSSE', 'bsse2480185@szabist.pk'),
  ('Prinkle Maheshwari', 'BSSE', 'bsse2480218@szabist.pk'),
  ('Yasir', 'BSSE', 'bsse2480224@szabist.pk'),
  ('Rohan Kumar', 'BSCS', 'bscs241240@szabist.pk'),
  ('Bhunesh Kumar', 'BSSE', 'bsse2480190@szabist.pk');

INSERT INTO issue (issue_date, return_date, status, student_id, book_id) VALUES
  ('2026-05-01', '2026-05-15', 'RETURNED', 1, 7),
  ('2026-06-01', '2026-06-15', 'ISSUED', 2, 4),
  ('2026-04-10', '2026-04-24', 'LATE', 3, 5),
  ('2026-05-10', '2026-05-24', 'RETURNED', 4, 11),
  ('2026-06-03', '2026-06-17', 'ISSUED', 5, 14);

-- correct spelling 
UPDATE books SET title = 'Introduction to Algorithms' WHERE book_id = 7;
UPDATE books SET title = 'Sapiens: A Breif History of HumanKind' WHERE book_id = 11;

-- Create index for optimization
CREATE INDEX idx_books_category_id ON books(category_id);
CREATE INDEX idx_issue_student_id ON issue(student_id);
CREATE INDEX idx_issue_book_id ON issue(book_id);
CREATE INDEX idx_issue_status ON issue(status);
