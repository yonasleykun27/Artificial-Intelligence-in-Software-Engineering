# Custom Exceptions for Product validation
class InvalidPriceError(ValueError):
    """Exception raised when a product price is invalid (must be a positive number > 0)."""
    pass


class InvalidQuantityError(ValueError):
    """Exception raised when a product quantity is invalid (must be a non-negative integer >= 0)."""
    pass


class Product:
    """Represents a product with a name, price, and quantity."""

    def __init__(self, name: str, price: float, quantity: int):
        self.name = name
        # Assigning through self.price and self.quantity invokes property setters,
        # ensuring validation occurs during initialization as well as on reassignment.
        self.price = price
        self.quantity = quantity

    @property
    def price(self) -> float:
        """Gets the unit price of the product."""
        return self._price

    @price.setter
    def price(self, value: float):
        """Sets the unit price, validating that it is a positive number (> 0)."""
        if isinstance(value, bool) or not isinstance(value, (int, float)) or value <= 0:
            raise InvalidPriceError(
                f"Invalid price '{value}'. Price must be a positive number (> 0)."
            )
        self._price = float(value)

    @property
    def quantity(self) -> int:
        """Gets the available stock quantity of the product."""
        return self._quantity

    @quantity.setter
    def quantity(self, value: int):
        """Sets the stock quantity, validating that it is a non-negative integer (>= 0)."""
        if isinstance(value, bool) or not isinstance(value, int) or value < 0:
            raise InvalidQuantityError(
                f"Invalid quantity '{value}'. Quantity must be a non-negative integer (>= 0)."
            )
        self._quantity = value


class InventoryManager:
    """Manages the collection of products and provides inventory operations."""

    def __init__(self, inventory=None):
        self.inventory = inventory if inventory is not None else []

    def add_product(self, product: Product):
        """Adds a product object to the inventory list."""
        self.inventory.append(product)

    def update_quantity(self, name: str, new_quantity: int):
        """Updates the quantity of a product by name."""
        for product in self.inventory:
            if product.name == name:
                product.quantity = new_quantity
                break

    def calculate_total_value(self) -> float:
        """Calculates the total monetary value of all inventory."""
        total = 0.0
        for product in self.inventory:
            total += product.price * product.quantity
        return total

    def display_inventory(self):
        """Prints the current inventory list."""
        for product in self.inventory:
            print(f"{product.name} - ${product.price:.2f} x {product.quantity}")


if __name__ == "__main__":
    # Demo usage
    manager = InventoryManager()
    manager.add_product(Product("Laptop", 1200.00, 5))
    manager.add_product(Product("Mouse", 25.00, 20))
    manager.update_quantity("Mouse", 18)

    print("Current Inventory:")
    manager.display_inventory()
    print(f"\nTotal Inventory Value: ${manager.calculate_total_value():.2f}\n")

    # Demonstration of error handling and validation
    print("--- Demonstrating Validation & Custom Exceptions ---")
    
    # 1. Invalid price on initialization
    try:
        Product("Invalid Item", -10.0, 5)
    except InvalidPriceError as e:
        print(f"Caught expected error on initialization (negative price): {e}")

    # 2. Zero price on initialization
    try:
        Product("Free Item", 0, 5)
    except InvalidPriceError as e:
        print(f"Caught expected error on initialization (zero price): {e}")

    # 3. Invalid quantity on initialization
    try:
        Product("Invalid Item", 50.0, -3)
    except InvalidQuantityError as e:
        print(f"Caught expected error on initialization (negative quantity): {e}")

    # 4. Non-integer quantity on initialization
    try:
        Product("Invalid Item", 50.0, 3.5)
    except InvalidQuantityError as e:
        print(f"Caught expected error on initialization (fractional quantity): {e}")

    # 5. Invalid price reassignment on existing object
    try:
        laptop = Product("Laptop", 1200.00, 5)
        laptop.price = -500.00
    except InvalidPriceError as e:
        print(f"Caught expected error on direct attribute reassignment: {e}")

    # 6. Invalid quantity update via InventoryManager
    try:
        manager.update_quantity("Mouse", -10)
    except InvalidQuantityError as e:
        print(f"Caught expected error via update_quantity: {e}")
