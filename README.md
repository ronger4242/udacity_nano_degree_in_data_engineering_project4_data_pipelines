# Project4: Data Pipelines with Airflow
## Project Introduction
A music streaming company, Sparkify, has decided that it is time to introduce more automation and monitoring to their data warehouse ETL pipelines and come to the conclusion that the best tool to achieve this is Apache Airflow.

They have decided to bring you into the project and expect you to create high grade data pipelines that are dynamic and built from reusable tasks, can be monitored, and allow easy backfills. They have also noted that the data quality plays a big part when analyses are executed on top the data warehouse and want to run tests against their datasets after the ETL steps have been executed to catch any discrepancies in the datasets.

The source data resides in S3 and needs to be processed in Sparkify's data warehouse in Amazon Redshift. The source datasets consist of JSON logs that tell about user activity in the application and JSON metadata about the songs the users listen to.

## Datasets
* Log data:s3://udacity-dend/log_data
* Song data:s3://udacity-dend/song_data

## Airflow Data Pipeline
* Create a project S3 bucket using the AWS Cloudshell

  aws s3 mb s3://nancy-zhao/
  
* Copy the data from the udacity bucket to the home cloudshell directory:

  aws s3 cp s3://udacity-dend/log-data/ ~/log-data/ --recursive
  aws s3 cp s3://udacity-dend/song-data/A/A/A ~/song-data/ --recursive

* Copy the data from the udacity bucket to the home cloudshell directory:

  aws s3 cp ~/log-data/ s3://nancy-zhao/log-data/ --recursive
  aws s3 cp ~/song-data/ s3://nancy-zhao/song-data/ --recursive

## Airflow DAGS:
### 1.create_tables DAG overview
![image (8)](https://github.com/ronger4242/udacity_nano_degree_in_data_engineering_project4_data_pipelines/assets/53929071/233d960c-28d0-49e0-8d25-c7312bb54672)
* Begin_execution & Stop_execution are dummy operators representing DAG start and end point.
* Create_tables: create tables in Redshift

### 2. final_project DAG overview

![image (6)](https://github.com/ronger4242/udacity_nano_degree_in_data_engineering_project4_data_pipelines/assets/53929071/9cab1803-3792-4a20-a480-f48054e447c1)
* Stage_Events & Stage_songs: extract and load data from S3 to Redshift
* Load_songplays_fact_table & Load_*_dim_tables: load and transform data from staging to fact and dimension tables
* Run_data_quality_checks: run data quality checks to ensure no empty tables

## Execution
* Set up AWS and Airflow configurations
* Create S3 bucket and copy data from udacity-dend bucket
* Run create_tables DAG to create tables in redshift
* Run final_project DAG to triger the ETL data pipeline

![image (5)](https://github.com/ronger4242/udacity_nano_degree_in_data_engineering_project4_data_pipelines/assets/53929071/d11a1ac3-72c8-494d-ac17-30168f1bf7f6)
![image (7)](https://github.com/ronger4242/udacity_nano_degree_in_data_engineering_project4_data_pipelines/assets/53929071/6d6a7619-ae56-436a-95c2-0b665ec79c32)
