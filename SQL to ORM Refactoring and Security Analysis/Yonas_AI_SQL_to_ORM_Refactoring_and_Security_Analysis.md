# Yonas_AI: SQL to ORM Refactoring and Security Analysis

**Author**: Yonas Leykun  
**Institution**: Frontier Institute of Technology  
**Course**: SE 203: High-Level Programming & Artificial Intelligence in Software Engineering  
**Module**: Week 5 | SQL to ORM Refactoring and Security Analysis  
**AI Assistant Used**: Antigravity AI / Google Gemini  

---

## 1. Prompt Formulation

To initiate the refactoring process and extract a comprehensive, production-grade architectural translation from procedural SQL to modern ORM, the following single, comprehensive prompt was formulated and submitted to the AI assistant:

```text
Act as a Senior Python and Database Architect. I have an existing procedural Python database script using mysql.connector and raw SQL queries (with functions like get_connection, create_user, get_user_by_username, update_user_email, delete_user, list_users).

Please refactor this into a professional, modern, and object-oriented solution using SQLAlchemy ORM.

Specifically, your response must:
1. Define the User class as a SQLAlchemy declarative model with appropriate table mapping, primary key, column types, and constraints (nullable, unique).
2. Show how to create the table, instantiate the database engine, add a new user to the database, and query for that user using an ORM Session (including transactional commit and rollback handling).
3. Explain in detail why the SQLAlchemy ORM version is a significantly more professional and secure solution than using raw SQL with string formatting, specifically detailing SQL injection immunity, type safety, connection pooling, and long-term code maintainability.
```

---

## 2. Execution Screenshot

Below is the single, uncropped screenshot of the AI assistant's complete execution response. It displays the refactored SQLAlchemy declarative model definition, table synchronization and CRUD session workflow, and the detailed comparative security and professional architectural analysis:

![AI Interaction and Refactoring Complete Execution Screenshot](./screenshots/ai_response_screenshot.png)

*Figure 1: Full AI assistant interaction showing the User declarative model definition, session management workflow, and comparative analysis of security and professional maintainability advantages.*

---

## 3. Verification and Reflection

### Abstraction and Maintainability
Transitioning from procedural SQL string manipulation to an object-centric Object-Relational Mapping (ORM) architecture fundamentally elevates software reliability by bridging the impedance mismatch between relational database tables and object-oriented domain logic. In procedural SQL codebases, database tables are addressed through raw text strings scattered across multiple service functions, and queried rows are returned as untyped tuples or generic dictionaries. This paradigm introduces severe cognitive overhead and architectural fragility: simple schema evolutions—such as renaming a column or altering a primary key type—fail to trigger static compile-time errors or IDE warnings, inevitably resulting in silent runtime defects and regressions. Conversely, SQLAlchemy’s declarative system establishes a single source of truth where tables, constraints, types, and relationships are codified as native Python classes. Developers interact with strongly typed attributes (`user.email`) rather than fragile array indices (`row[2]`), unlocking rich IDE autocompletion, static type validation via tools like MyPy, and automated schema migration pipelines with Alembic.

Furthermore, the abstraction provided by SQLAlchemy's `Session` implements Martin Fowler’s Unit of Work and Identity Map patterns, isolating application business logic from transactional mechanics and low-level connection lifecycles. Instead of manually coordinating cursor instances, tracking open connection pools, and choreographing error-prone `BEGIN`, `COMMIT`, and `ROLLBACK` branches across deeply nested functions, the ORM session maintains a deterministic registry of modified, inserted, and deleted objects. It batches state synchronizations inside transactional scopes and guarantees rollbacks upon exception encounters. Additionally, because the ORM compiles domain queries through an internal Abstract Syntax Tree (AST) into target-specific SQL dialects, engineering teams achieve genuine database engine portability. Development and CI/CD test suites can execute in-memory against SQLite for sub-second feedback loops, while staging and production environments seamlessly target clustered MySQL or PostgreSQL instances without requiring a single line of application code to be rewritten.

---

## 4. GitHub Repository Update

All task assets, including the initial procedural script, the refactored SQLAlchemy ORM implementation, full markdown documentation, and the execution screenshot, have been organized and committed to the course repository:

* **GitHub Repository Link**: [https://github.com/yonasleykun27/Artificial-Intelligence-in-Software-Engineering](https://github.com/yonasleykun27/Artificial-Intelligence-in-Software-Engineering)
* **Specific Task Folder Link**: [https://github.com/yonasleykun27/Artificial-Intelligence-in-Software-Engineering/tree/main/SQL%20to%20ORM%20Refactoring%20and%20Security%20Analysis](https://github.com/yonasleykun27/Artificial-Intelligence-in-Software-Engineering/tree/main/SQL%20to%20ORM%20Refactoring%20and%20Security%20Analysis)
