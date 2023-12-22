DROP TABLE Posts;

CREATE TABLE IF NOT EXISTS Posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    published BOOLEAN NOT NULL DEFAULT true,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP 
);

INSERT into Posts (title, content, published)
    VALUES
      ("Alice in Wonderland", 'A book by Lewis Carrol', true),
      ("The Cat in the Hat", 'A book by Ronald Dahl', true)
      ;
