#churn database
CREATE DATABASE data;

CREATE TABLE data.churn (
id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
customerID VARCHAR(12),
`date` date,
gender VARCHAR(12),
SeniorCitizen INT,
Partner	VARCHAR(6),
Dependents	VARCHAR(6),
tenure	INT,
PhoneService VARCHAR(6),
MultipleLines text,
InternetService	varchar(64),
OnlineSecurity	 VARCHAR(24),
OnlineBackup VARCHAR(24),	
DeviceProtection  VARCHAR(24),	
TechSupport	 VARCHAR(24),
StreamingTV	 VARCHAR(24),
StreamingMovies	 VARCHAR(24),
Contract text,
PaperlessBilling  VARCHAR(6),
PaymentMethod	text,
MonthlyCharges float,
TotalCharges float,
Churn VARCHAR(6),
created date,
updated date,
UNIQUE KEY `u_k_1`(customerID, date) ,
KEY `k_1`(churn),
KEY `k_2`(date),
KEY `k_3`(customerID))
 AUTO_INCREMENT = 0;


LOAD DATA INFILE '/var/lib/mysql-files/churn_data.csv' IGNORE
INTO TABLE data.churn
           FIELDS TERMINATED BY ',' 
           LINES TERMINATED BY '\n'
           IGNORE 1 LINES
           (customerID,	gender,	SeniorCitizen,
Partner, Dependents, tenure,	PhoneService,	MultipleLines,	InternetService,
	OnlineSecurity,	OnlineBackup,	DeviceProtection,	TechSupport,	StreamingTV,
	StreamingMovies,	Contract,	PaperlessBilling,	PaymentMethod,	MonthlyCharges,
	TotalCharges,	Churn
)
set 
customerID = customerID,
gender=gender,
SeniorCitizen= SeniorCitizen,
Partner=Partner, 
Dependents=Dependents, 
tenure=tenure,
PhoneService=PhoneService,	
MultipleLines=MultipleLines,	
InternetService=InternetService,
OnlineSecurity=OnlineSecurity,
OnlineBackup=OnlineBackup,	
DeviceProtection=DeviceProtection,	
TechSupport=TechSupport,	
StreamingTV=StreamingTV,
StreamingMovies=StreamingMovies,	
Contract=Contract,	
PaperlessBilling=PaperlessBilling,	
PaymentMethod=PaymentMethod,	
MonthlyCharges=IF(MonthlyCharges='',0,MonthlyCharges),
TotalCharges=IF(TotalCharges='',0,TotalCharges),	
Churn=Churn
;

UPDATE data.churn 
SET `date`= "2020-9-20"
,`created`="2020-9-20"
,`updated`="2020-9-20"
WHERE id>0;