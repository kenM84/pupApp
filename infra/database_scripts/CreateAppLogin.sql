--create server login
CREATE LOGIN pupApp 
	WITH PASSWORD = 'Cal.exico123!' 
GO

--create app login
USE sqlPupDev-EASTUS2;
CREATE USER pupApp FOR LOGIN pupApp;

--create schema and give pupApp perms
CREATE SCHEMA pupApp;
GRANT CREATE TABLE TO pupApp;
GRANT CONTROL ON SCHEMA:: pupApp TO pupApp;
GRANT ALTER ON SCHEMA::pupApp TO pupApp;