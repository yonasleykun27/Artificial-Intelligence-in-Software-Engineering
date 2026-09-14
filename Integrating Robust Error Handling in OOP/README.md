# W3 AI Lab Assignment: Integrating Robust Error Handling in OOP

**Author:** Yonas Leykun  
**Course:** SE 202: High Level Programming I  
**Institution:** Frontier Institute of Technology  
**Directory:** `Integrating Robust Error Handling in OOP`

---

## 1. Project Overview

In real-world inventory management and enterprise e-commerce systems, data integrity is paramount. Allowing direct, unvalidated mutation of core domain attributes—such as setting a product's price or stock quantity to a negative number—leads to silent state corruption, distorted accounting ledgers, and catastrophic downstream failures.

This project refactors a vulnerable object-oriented product inventory system by incorporating **defensive programming**, **encapsulation**, and **domain-specific exception handling** in Python.

---

## 2. AI Scaffolding Tool & Methodology

- **AI Tool Used:** **Gemini Code Assist** (integrated via VS Code extension).
- **Methodology:** A single comprehensive scaffolding prompt was submitted to Gemini Code Assist instructing it to implement `@property` validation, construct a domain-specific custom exception (`InvalidProductDataError`), route `__init__` constructor assignments through setters, and provide an architectural breakdown of Encapsulation and Precedence under Python's Descriptor Protocol.

---

## 3. Key Architectural Enhancements
 
### A. Defensive Data Validation via `@property` Setters
- **Private Backing Stores:** Attributes `_name`, `_price`, and `_quantity` are shielded from direct external tampering.
- **Strict Precedence:** Utilizing Python's **data descriptor protocol**, `@property` setters intercept every assignment attempt (e.g., `product.quantity = -5`) before the instance dictionary (`__dict__`) can be updated.
- **Instantiation Safety:** The `__init__` constructor routes assignments directly through `self.price = price` and `self.quantity = quantity`, guaranteeing that invalid data is caught immediately upon instantiation, eliminating duplicate validation logic.
- **Type Safety:** Guards against Python's type hierarchy subtleties (specifically ensuring `bool` values, which subclass `int`, are rejected for price and quantity).

### B. Domain-Specific Custom Exception (`InvalidProductDataError`)
- Subclasses standard `ValueError` to preserve semantic compatibility with standard Python exception hierarchies while providing explicit domain context.
- Stores structured metadata: `attribute`, `value`, and `reason`, enabling caller applications and API controllers to generate clear, actionable error responses (e.g., HTTP 422) without crashing.

---

## 4. Repository File Structure

| File | Description |
| :--- | :--- |
| [`initial_inventory.py`](initial_inventory.py) | The unvalidated baseline implementation demonstrating silent failure and state corruption under invalid inputs. |
| [`refactored_inventory.py`](refactored_inventory.py) | The hardened implementation featuring `@property` setters, `InvalidProductDataError`, constructor validation, and an automated test suite. |
| [`README.md`](README.md) | Comprehensive engineering documentation, AI tool methodology, and execution guide. |

---

## 5. Execution & Verification

To run the refactored inventory manager and observe the validation in action:

```bash
python refactored_inventory.py
```

### Verification Output:
```text
--- Initializing Inventory Manager ---
Current Inventory:
Laptop - $1200.00 x 5
Mouse - $25.00 x 18

Total Inventory Value: $6450.00

--- Testing Invalid Input ---
Test result: Invalid value for 'quantity': -5. Quantity cannot be negative.

--- Testing Supplementary Validation Edge Cases ---
Caught negative price assignment: Invalid value for 'price': -15.5. Price cannot be negative.
Caught invalid instantiation: Invalid value for 'quantity': -10. Quantity cannot be negative.
Caught invalid type assignment: Invalid value for 'price': 'cheap'. Price must be a numeric value (int or float).

Inventory state verification post-exceptions (values unchanged):
Laptop - $1200.00 x 5
Mouse - $25.00 x 18
Total Inventory Value: $6450.00
```

### Code Style Compliance:
Both files strictly adhere to PEP 8 standards:
```bash
pycodestyle initial_inventory.py refactored_inventory.py
# 0 errors, 0 warnings
```
