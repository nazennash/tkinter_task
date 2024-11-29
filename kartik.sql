-- check if the database exists, if there delete (resets to prevent conflicts).
DROP DATABASE kartik;

-- Create a new database named 'kartik'
CREATE DATABASE kartik;

-- specify 'kartik' as database to be used
USE kartik;

-- Create ProductCategory and Product Table
CREATE TABLE ProductCategory (
    ProductCategoryID INT AUTO_INCREMENT PRIMARY KEY,
    ProductCategoryName VARCHAR(255) NOT NULL
);

CREATE TABLE Product (
    ProductID INT AUTO_INCREMENT PRIMARY KEY,
    ProductCategoryID INT,
    ProductName VARCHAR(255),
    Weight DECIMAL(10, 2),
    StandardCost DECIMAL(10, 2),
    Size VARCHAR(50),
    FOREIGN KEY (ProductCategoryID) REFERENCES ProductCategory(ProductCategoryID)
);

-- Have sample test data in ProductCategory and Product
INSERT INTO ProductCategory (ProductCategoryName) VALUES
('Electronics'),
('Furniture'),
('Clothing');

INSERT INTO Product (ProductCategoryID, ProductName, Weight, StandardCost, Size) VALUES
(1, 'Smartphone', 0.5, 700.00, 'Small'),
(1, 'Laptop', 2.5, 1500.00, 'Medium'),
(2, 'Table', 25.0, 300.00, 'Large'),
(2, 'Chair', 10.0, 150.00, 'Medium'),
(3, 'T-shirt', 0.3, 20.00, 'Small'),
(3, 'Jeans', 0.8, 50.00, 'Medium');

-- View for Unique ProductCategories (ProductCategoryID and names)
CREATE VIEW ProductCategoryView AS
SELECT DISTINCT ProductCategoryID, ProductCategoryName
FROM ProductCategory;

-- Stored Procedure to Update records of Product
DELIMITER //

CREATE PROCEDURE UpdateProductDetails(
    IN inputProductCategoryID INT,
    IN percentageChange DECIMAL(5, 2)
)
BEGIN
    -- Update Weight
    UPDATE Product
    SET Weight = Weight + (Weight * percentageChange / 100)
    WHERE ProductCategoryID = inputProductCategoryID;

    -- Update StandardCost
    UPDATE Product
    SET StandardCost = StandardCost + (StandardCost * percentageChange / 100)
    WHERE ProductCategoryID = inputProductCategoryID;

    -- Update Size (Example: Append a suffix for tracking size updates)
    UPDATE Product
    SET Size = CONCAT(Size, ' (u)')
    WHERE ProductCategoryID = inputProductCategoryID;
END //

DELIMITER ;

-- Test the Stored Procedure
CALL UpdateProductDetails(1, 10);

-- Verify the updates - the views (products check and productCategory check)
SELECT * FROM Product;
SELECT DISTINCT ProductCategoryID, ProductCategoryName
FROM ProductCategory;

