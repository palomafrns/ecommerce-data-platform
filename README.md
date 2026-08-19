E-commerce Data Platform

Data engineering pipeline for ingesting, processing, and loading e-commerce (product) data, built in Python with PostgreSQL as the target database.

About the project

This project implements an ETL pipeline that extracts raw product data (JSON format), processes and organizes this information into staging layers, and performs structured loading into a PostgreSQL database using psycopg2.

The goal is to practice and demonstrate data engineering concepts: data modeling, staging, data quality validation, and multi-table ETL.

Raw: raw product data is stored as JSON, with no transformation
Staging: data is separated and organized into intermediate files by domain (dimensions, images, metadata)
Load: staging data is loaded into PostgreSQL through Python scripts using psycopg2, following the mapping between source fields and database columns

Tech stack:

Python — main pipeline language
psycopg2 — connection and data loading into PostgreSQL
PostgreSQL — target relational database
Docker Compose — database environment orchestration
pandas / numpy — data manipulation and transformation