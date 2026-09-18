# IT Retail ERP

Computer hardware, software and IT retail management system for Kuwait.

This repository contains two implementations of the same ERP business requirements:

- `aspnet-core/` — ASP.NET Core MVC, Entity Framework Core, ASP.NET Core Identity, SQL Server
- `django/` — Python Django, SQL Server

Both implementations follow the same business flow and SRS. Development work is done on the `development` branch and promoted to `main` after review.

## Core business flow

Supplier → Purchase → Inventory → Sales / Service → Customer → Payment → Profit / Reports

Quotation flow:

Customer → Quotation → Approval → Sales Invoice → Payment → Stock Update → Customer Ledger

## Database

Microsoft SQL Server 2019 is the initial production database.
