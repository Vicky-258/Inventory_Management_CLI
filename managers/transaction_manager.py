from models import Transaction, Item
from db import get_db

class TransactionManager:
    def _log_transaction(self, user_id: int, item_id: int, action: str, quantity: int, unit_price: float):
        total_price = round(unit_price * quantity, 2)
        with get_db() as db:
            transaction = Transaction(
                user_id=user_id,
                item_id=item_id,
                action=action,
                quantity=quantity,
                total_price=total_price
            )
            db.add(transaction)
            db.commit()
        print(f"✅ Logged {action} of {quantity} unit(s), ₹{total_price} total.")

    def buy_item(self, user_id: int, item_name: str, quantity: int):
        with get_db() as db:
            item = db.query(Item).filter(Item.name.ilike(f"%{item_name}%")).first()
            if not item:
                raise ValueError("Item not found.")
            item.quantity += quantity
            db.commit()
            self._log_transaction(user_id, item.id, "buy", quantity, item.price)
            return item

    def sell_item(self, user_id: int, item_name: str, quantity: int):
        with get_db() as db:
            item = db.query(Item).filter(Item.name.ilike(f"%{item_name}%")).first()
            if not item:
                raise ValueError("Item not found.")
            if item.quantity < quantity:
                raise ValueError("Not enough stock.")
            item.quantity -= quantity
            db.commit()
            self._log_transaction(user_id, item.id, "sell", quantity, item.price)
            return item
