-- ============================================
-- CREATE VIDEO GAME ANALYSIS TABLES
-- ============================================

USE VideoGameAnalysis;
GO

PRINT '';
PRINT '========================================';
PRINT 'CREATING TABLES';
PRINT '========================================';
PRINT '';

-- ============================================
-- Drop existing tables (clean start)
-- ============================================

IF OBJECT_ID('GameAnalysis', 'U') IS NOT NULL 
BEGIN
    DROP TABLE GameAnalysis;
    PRINT 'Dropped old GameAnalysis table';
END

IF OBJECT_ID('Sales', 'U') IS NOT NULL 
BEGIN
    DROP TABLE Sales;
    PRINT 'Dropped old Sales table';
END

IF OBJECT_ID('Games', 'U') IS NOT NULL 
BEGIN
    DROP TABLE Games;
    PRINT 'Dropped old Games table';
END

PRINT '';
GO

-- ============================================
-- TABLE 1: Games
-- ============================================

PRINT 'Creating Games table...';

CREATE TABLE Games (
    GameID INT PRIMARY KEY IDENTITY(1,1),
    Title NVARCHAR(500) NOT NULL,
    Rating DECIMAL(3,2) NULL,
    Genres NVARCHAR(255) NULL,
    Plays INT DEFAULT 0,
    Backlogs INT DEFAULT 0,
    Wishlist INT DEFAULT 0,
    ReleaseDate DATE NULL,
    ReleaseYear INT NULL,
    Platform NVARCHAR(50) NULL,
    Developer NVARCHAR(255) NULL,
    CreatedDate DATETIME DEFAULT GETDATE()
);

PRINT '✅ Games table created';
PRINT '';
GO

-- ============================================
-- TABLE 2: Sales
-- ============================================

PRINT 'Creating Sales table...';

CREATE TABLE Sales (
    SaleID INT PRIMARY KEY IDENTITY(1,1),
    GameName NVARCHAR(500) NOT NULL,
    Platform NVARCHAR(50) NULL,
    ReleaseYear INT NULL,
    Genre NVARCHAR(100) NULL,
    Publisher NVARCHAR(255) NULL,
    NA_Sales DECIMAL(10,2) DEFAULT 0,
    EU_Sales DECIMAL(10,2) DEFAULT 0,
    JP_Sales DECIMAL(10,2) DEFAULT 0,
    Other_Sales DECIMAL(10,2) DEFAULT 0,
    Global_Sales DECIMAL(10,2) DEFAULT 0,
    CreatedDate DATETIME DEFAULT GETDATE()
);

PRINT '✅ Sales table created';
PRINT '';
GO

-- ============================================
-- TABLE 3: GameAnalysis (Merged)
-- ============================================

PRINT 'Creating GameAnalysis table...';

CREATE TABLE GameAnalysis (
    AnalysisID INT PRIMARY KEY IDENTITY(1,1),
    Title NVARCHAR(500) NOT NULL,
    Rating DECIMAL(3,2) NULL,
    Genre NVARCHAR(100) NULL,
    Platform NVARCHAR(50) NULL,
    Developer NVARCHAR(255) NULL,
    Publisher NVARCHAR(255) NULL,
    ReleaseYear INT NULL,
    Plays INT DEFAULT 0,
    Wishlist INT DEFAULT 0,
    Backlogs INT DEFAULT 0,
    NA_Sales DECIMAL(10,2) DEFAULT 0,
    EU_Sales DECIMAL(10,2) DEFAULT 0,
    JP_Sales DECIMAL(10,2) DEFAULT 0,
    Other_Sales DECIMAL(10,2) DEFAULT 0,
    Global_Sales DECIMAL(10,2) DEFAULT 0,
    CreatedDate DATETIME DEFAULT GETDATE()
);

PRINT '✅ GameAnalysis table created';
PRINT '';
GO

-- ============================================
-- Create Indexes
-- ============================================

PRINT 'Creating indexes for better performance...';

CREATE INDEX IX_Games_Title ON Games(Title);
CREATE INDEX IX_Games_Platform ON Games(Platform);
CREATE INDEX IX_Sales_GameName ON Sales(GameName);
CREATE INDEX IX_Sales_Platform ON Sales(Platform);
CREATE INDEX IX_Analysis_Title ON GameAnalysis(Title);
CREATE INDEX IX_Analysis_Genre ON GameAnalysis(Genre);
CREATE INDEX IX_Analysis_Platform ON GameAnalysis(Platform);

PRINT '✅ Indexes created';
PRINT '';
GO

-- ============================================
-- Verify Tables
-- ============================================

PRINT '========================================';
PRINT 'TABLE CREATION COMPLETE';
PRINT '========================================';
PRINT '';
PRINT 'Tables created:';

SELECT 
    TABLE_NAME AS [Table Name],
    (SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS 
     WHERE TABLE_NAME = t.TABLE_NAME) AS [Columns]
FROM INFORMATION_SCHEMA.TABLES t
WHERE TABLE_TYPE = 'BASE TABLE'
ORDER BY TABLE_NAME;

PRINT '';
PRINT '✅ Ready to load data!';
GO
