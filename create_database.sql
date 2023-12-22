DROP TABLE Products;

CREATE TABLE IF NOT EXISTS Products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price INTEGER NOT NULL,
    is_sale BOOLEAN NOT NULL DEFAULT 0,
    inventory INTEGER NOT NULL DEFAULT 0,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP 
);

INSERT into Products (
        name,
        price,
        is_sale,
        created_at,
        inventory
    )
    VALUES (
        "Computer Mouse",
        9.99,
        1,
        '2023-01-01 12:00:00',
        5
    );

INSERT into Products (name, price, is_sale)
    VALUES
      ("TV", 9.99, 1),
      ("DVD Player", 8950438430.545, true),
      ("Blue Ray Player", 9.99, 1),
      ("Car", 4534859, 1),
      ("Pencil", 9.99, false)
      ;
