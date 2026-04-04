-- Migration script to add the multimedia column to the services table
-- Purpose: Add multimedia service flag to existing services table
-- Safe to run on production database (idempotent)

USE app_db;

-- Check if column exists before adding it using information_schema
-- This prevents errors if the migration is run multiple times (true idempotent)
SET @dbname = DATABASE();
SET @columnname = 'multimedia';

SELECT COUNT(*) INTO @exists 
FROM information_schema.columns 
WHERE table_schema = @dbname 
  AND table_name = 'services' 
  AND column_name = @columnname;

SET @sql = CONCAT(
    'ALTER TABLE services ADD COLUMN ',
    @columnname, ' BOOLEAN DEFAULT FALSE'
);
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;
