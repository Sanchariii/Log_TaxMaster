CREATE LOGIN Sanchari WITH PASSWORD = 'RA_project';
CREATE USER SanR FOR LOGIN Sanchari;

USE TaxMaster;
ALTER ROLE db_datareader ADD MEMBER Sanchari;
ALTER ROLE db_datawriter ADD MEMBER SanR;