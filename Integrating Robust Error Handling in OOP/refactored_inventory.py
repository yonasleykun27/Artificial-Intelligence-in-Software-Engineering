"""Refactored Object-Oriented Inventory Manager with Robust Error Handling.

Author: Yonas Leykun
Course: SE 202: High Level Programming I
Assignment: W3 AI Lab Assignment - Integrating Robust Error Handling in OOP

Description:
    Enhances the Product class with defensive data validation using Python
    @property getters and setters and a custom InvalidProductDataError
    exception. Enforces strict data integrity and encapsulation to prevent
    inconsistent object states such as negative prices or negative quantities.
"""


class InvalidProductDataError(ValueError):
    """Exception raised when invalid product data is assigned.

    Inherits from ValueError to maintain semantic consistency with Python's
    standard exception hierarchy while offering a distinct type for domain
    validation failures.
    """

    def __init__(self, attribute, value, reason):
        self.attribute = attribute
        self.value = value
        self.reason = reason
        message = (
            f"Invalid value for '{attribute}': {value!r}. {reason}"
        )
        super().__init__(message)


class Product:
    """Represents a product with validated name, price, and quantity."""

    def __init__(self, name, price, quantity):
        """Initialize a new Product instance.

        Delegates attribute assignment directly to property setters to
        ensure validation occurs at instantiation time.
        """
        self.name = name
        self.price = price
        self.quantity = quantity

    @property
    def name(self):
        """Get the product name."""
        return self._name

    @name.setter
    def name(self, value):
        """Set and validate the product name."""
        if not isinstance(value, str) or not value.strip():
            raise InvalidProductDataError(
                "name", value, "Product name must be a non-empty string."
            )
        self._name = value.strip()

    @property
    def price(self):
        """Get the unit price."""
        return self._price

    @price.setter
    def price(self, value):
        """Set and validate unit price. Must be a non-negative float or int."""
        # Reject booleans explicitly (bool is a subclass of int in Python)
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise InvalidProductDataError(
                "price", value, "Price must be a numeric value (int or float)."
            )
        if value < 0:
            raise InvalidProductDataError(
                "price", value, "Price cannot be negative."
            )
        self._price = float(value)

    @property
    def quantity(self):
        """Get current inventory stock quantity."""
        return self._quantity

    @quantity.setter
    def quantity(self, value):
        """Set and validate stock quantity. Must be a non-negative integer."""
        # Reject booleans explicitly
        if isinstance(value, bool) or not isinstance(value, int):
            raise InvalidProductDataError(
                "quantity", value, "Quantity must be an integer."
            )
        if value < 0:
            raise InvalidProductDataError(
                "quantity", value, "Quantity cannot be negative."
            )
        self._quantity = value


class InventoryManager:
    """Manages the collection of products and provides inventory operations."""

    def __init__(self, inventory=None):
        self.inventory = inventory if inventory is not None else []

    def add_product(self, product):
        """Adds a product object to the inventory list."""
        if not isinstance(product, Product):
            raise TypeError(
                "Only Product instances can be added to inventory."
            )
        self.inventory.append(product)

    def update_quantity(self, name, new_quantity):
        """Updates the quantity of a product by name."""
        for product in self.inventory:
            if product.name == name:
                product.quantity = new_quantity
                return True
        return False

    def calculate_total_value(self):
        """Calculates the total monetary value of all inventory."""
        total = 0.0
        for product in self.inventory:
            total += product.price * product.quantity
        return total

    def display_inventory(self):
        """Prints the current inventory list."""
        for product in self.inventory:
            print(
                f"{product.name} - ${product.price:.2f} x {product.quantity}"
            )


if __name__ == "__main__":
    # Standard Demo Usage from Step 1
    print("--- Initializing Inventory Manager ---")
    manager = InventoryManager()
    manager.add_product(Product("Laptop", 1200.00, 5))
    manager.add_product(Product("Mouse", 25.00, 20))
    manager.update_quantity("Mouse", 18)

    print("Current Inventory:")
    manager.display_inventory()
    print(f"\nTotal Inventory Value: ${manager.calculate_total_value():.2f}")

    # Mandatory Test Case from Step 4
    print("\n--- Testing Invalid Input ---")
    try:
        manager.inventory[0].quantity = -5
    except Exception as e:
        print(f"Test result: {e}")

    # Supplementary Defensive Test Cases
    print("\n--- Testing Supplementary Validation Edge Cases ---")

    # Edge Case 1: Negative Price on Existing Product
    try:
        manager.inventory[1].price = -15.50
    except InvalidProductDataError as e:
        print(f"Caught negative price assignment: {e}")

    # Edge Case 2: Negative Quantity at Instantiation Time
    try:
        Product("Keyboard", 45.00, -10)
    except InvalidProductDataError as e:
        print(f"Caught invalid instantiation: {e}")

    # Edge Case 3: Non-numeric Type Assignment
    try:
        manager.inventory[0].price = "cheap"
    except InvalidProductDataError as e:
        print(f"Caught invalid type assignment: {e}")

    # Verify inventory state remained uncorrupted
    print("\nInventory state verification post-exceptions (values unchanged):")
    manager.display_inventory()
    print(f"Total Inventory Value: ${manager.calculate_total_value():.2f}")
