# Restaurant API Service

Restaurant API Service is a Django-based RESTful API for managing restaurants and menus. It provides endpoints for creating, updating, and retrieving restaurant-related data, as well as user registration and menu management.

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Endpoints](#endpoints)
- [Presentation](#presentation)

## Introduction

Restaurant API Service is designed to streamline the management of restaurant-related data.

### Features:
- Rating system for menus
- Getting menu for current day
- Uploading menu

## Installation

1. Clone the repository:

   ```
   git clone https://github.com/volodymyr-komarnyckyi/restaurant-test
   ```
2. Create .env file and define environmental variables following .env.example:
   ```
   POSTGRES_HOST= your db host
   POSTGRES_DB= name of your db
   POSTGRES_USER= username of your db user
   POSTGRES_PASSWORD= your db password
   SECRET_key=" your django secret key "
   ```
3. Run command:
   ```
   docker-compose up --build
   ```
4. App will be available at: ```127.0.0.1:8000```
5. Login using next credentials:
   ```
   admin@admin.com
   Volodymyr8204
   ```
## Endpoints
   ```
   "restaurant" : 
                "http://127.0.0.1:8000/api/theatre/genres/"
                "http://127.0.0.1:8000/api/theatre/actors/"
                "http://127.0.0.1:8000/api/theatre/plays/"
                "http://127.0.0.1:8000/api/theatre/theatre_halls/"
                "http://127.0.0.1:8000/api/theatre/performances/"
                "http://127.0.0.1:8000/api/theatre/reservations/"
   "employee" : 
                   "http://127.0.0.1:8000/api/user/register/"
                   "http://127.0.0.1:8000/api/user/me/"
                   "http://127.0.0.1:8000/api/user/token/"
                   "http://127.0.0.1:8000/api/user/token/refresh/"
   "documentation": 
                   "http://127.0.0.1:8000/api/doc/"
                   "http://127.0.0.1:8000/api/swagger/"
                   "http://127.0.0.1:8000/api/redoc/"
   ```

## Schema
![db_schema.png](rest_db.png)

## Presentation
![swagger.png](swagger.png)
![trip_list.png](play_list.png)
![api_root.png](api_root.png)