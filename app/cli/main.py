"""Command-line interface for pharmacy system.

This is a thin wrapper around the core pharmacy logic.
No business logic here - just orchestration.
"""

import sys
from pathlib import Path

# Add src to path so we can import pharmacy modules
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from pharmacy.models import ShoppingCart, CartItem
from pharmacy.business import PricingEngine, QuantityValidator
from pharmacy.database import PharmacyDatabase


def main():
    """Simple CLI demo of the pharmacy system."""
    print("=" * 50)
    print("Pharmacy System - CLI Demo")
    print("=" * 50)
    print()
    
    # 1. Initialize database
    db_path = Path("pharmacy.db")
    print(f"📁 Database: {db_path.absolute()}")
    
    with PharmacyDatabase(db_path) as db:
        db.init_tables()
        db.load_csv_data(Path("src/pharmacy/data"))
        print("✅ Database initialized")
        print()
        
        # 2. Show all products
        print("📦 Products in stock:")
        print("-" * 40)
        products = db.get_all_products()
        for p in products[:5]:  # Show first 5
            print(f"   {p.id}. {p.name} - {p.price} руб. (stock: {p.quantity_in_stock})")
        print(f"   ... and {len(products) - 5} more")
        print()
        
        # 3. Demo shopping cart
        print("🛒 Demo: Customer buys 2 items")
        print("-" * 40)
        
        cart = ShoppingCart()
        
        # Add first product
        product1 = products[0]
        cart.add_item(CartItem(
            product_id=product1.id,
            product_name=product1.name,
            quantity=2,
            price=product1.price
        ))
        print(f"   Added: {product1.name} x 2 = {product1.price * 2} руб.")
        
        # Add second product
        product2 = products[1]
        cart.add_item(CartItem(
            product_id=product2.id,
            product_name=product2.name,
            quantity=1,
            price=product2.price
        ))
        print(f"   Added: {product2.name} x 1 = {product2.price} руб.")
        
        print()
        print(f"   Subtotal: {cart.total} руб.")
        
        # 4. Apply discounts
        final_price, discounts = PricingEngine.calculate_final_price(
            subtotal=cart.total,
            total_quantity=cart.item_count,
            promo_code="STUDENT10"
        )
        
        if discounts:
            for d in discounts:
                print(f"   Discount {d.percent}%: -{d.amount} руб. ({d.reason})")
            print(f"   Final price: {final_price} руб.")
        
        print()
        print("=" * 50)
        print("✅ Demo completed successfully!")
        print("=" * 50)


if __name__ == "__main__":
    main()
