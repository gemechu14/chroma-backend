"""
Seed script — populates the database with two demo salons plus a shared
product catalog.

Usage (from the project root):
    python -m src.seed.seed_data
"""
import sys
import os

# Allow running as a script from project root
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from src.database import SessionLocal, engine, Base
import src.models  # noqa: F401 — register all ORM models

from src.models.tenant import Tenant, Location
from src.models.user import User
from src.models.customer import Customer
from src.models.product import Brand, ProductLine, Product
from src.models.tenant_product import TenantProduct
from src.models.inventory import InventoryItem
from src.utils.security import hash_password


def seed() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        _seed_all(db)
        print("[OK] Seed complete.")
    except Exception as exc:
        db.rollback()
        print(f"[ERROR] Seed failed: {exc}")
        raise
    finally:
        db.close()


def _seed_all(db) -> None:

    # ------------------------------------------------------------------
    # Global product catalog
    # ------------------------------------------------------------------

    redken = _get_or_create(db, Brand, name="Redken", defaults={
        "website_url": "https://www.redken.com",
    })
    wella = _get_or_create(db, Brand, name="Wella", defaults={
        "website_url": "https://www.wella.com",
    })
    db.flush()

    shades_eq = _get_or_create(db, ProductLine, name="Shades EQ", defaults={
        "brand_id": redken.id,
        "category": "COLOR",
    })
    color_touch = _get_or_create(db, ProductLine, name="Color Touch", defaults={
        "brand_id": wella.id,
        "category": "COLOR",
    })
    redken_dev = _get_or_create(db, ProductLine, name="Shades EQ Processing Solution", defaults={
        "brand_id": redken.id,
        "category": "DEVELOPER",
    })
    db.flush()

    # Redken Shades EQ shades
    shades = [
        ("09N", "Shades EQ 09N — Platinum", "N"),
        ("07N", "Shades EQ 07N — Dark Blonde", "N"),
        ("07A", "Shades EQ 07A — Dark Blonde Ash", "A"),
        ("06RB", "Shades EQ 06RB — Red Reflect Brown", "RB"),
        ("05VV", "Shades EQ 05VV — Violet Blaze", "VV"),
    ]
    redken_products: dict[str, Product] = {}
    for code, name, tone in shades:
        p = _get_or_create(db, Product, code=code, product_line_id=shades_eq.id, defaults={
            "name": name,
            "tone_family": tone,
            "pack_size_value": 60,
            "pack_size_unit": "G",
            "is_active": True,
        })
        redken_products[code] = p

    # Wella Color Touch shades
    wella_shades = [
        ("7/0", "Color Touch 7/0 — Medium Blonde", "N"),
        ("6/7", "Color Touch 6/7 — Dark Blonde Brown", "B"),
    ]
    wella_products: dict[str, Product] = {}
    for code, name, tone in wella_shades:
        p = _get_or_create(db, Product, code=code, product_line_id=color_touch.id, defaults={
            "name": name,
            "tone_family": tone,
            "pack_size_value": 60,
            "pack_size_unit": "G",
            "is_active": True,
        })
        wella_products[code] = p

    # Developer
    developer = _get_or_create(
        db, Product,
        code="DEV-10",
        product_line_id=redken_dev.id,
        defaults={
            "name": "Shades EQ Processing Solution 10 Vol",
            "pack_size_value": 950,
            "pack_size_unit": "ML",
            "is_active": True,
        },
    )
    db.flush()

    # ------------------------------------------------------------------
    # Tenant 1 — Salon One (Premium)
    # ------------------------------------------------------------------

    salon_one = _get_or_create(db, Tenant, name="Salon One", defaults={
        "plan": "premium",
        "status": "active",
    })
    db.flush()

    loc_one = _get_or_create(
        db, Location, tenant_id=salon_one.id, name="Salon One — Main Branch", defaults={
            "address": "123 Main Street, New York, NY 10001",
            "timezone": "America/New_York",
        },
    )
    db.flush()

    admin_one = _get_or_create(
        db, User, email="admin@salonone.com", tenant_id=salon_one.id, defaults={
            "full_name": "Alice Admin",
            "password_hash": hash_password("password123"),
            "role": "ADMIN",
            "is_active": True,
            "default_location_id": loc_one.id,
        },
    )
    stylist_one = _get_or_create(
        db, User, email="mike@salonone.com", tenant_id=salon_one.id, defaults={
            "full_name": "Mike Stylist",
            "password_hash": hash_password("password123"),
            "role": "EMPLOYEE",
            "is_active": True,
            "default_location_id": loc_one.id,
        },
    )
    db.flush()

    # Sample customer for Salon One
    sarah = _get_or_create(
        db, Customer, full_name="Sarah Johnson", tenant_id=salon_one.id, defaults={
            "phone": "+1-555-0101",
            "email": "sarah@example.com",
            "home_location_id": loc_one.id,
        },
    )
    db.flush()

    # Tenant products for Salon One
    tp_09n = _get_or_create(
        db, TenantProduct,
        tenant_id=salon_one.id,
        product_id=redken_products["09N"].id,
        defaults={
            "is_enabled": True,
            "tracking_unit": "G",
            "default_unit_cost": 0.35,
            "currency": "USD",
        },
    )
    tp_07n = _get_or_create(
        db, TenantProduct,
        tenant_id=salon_one.id,
        product_id=redken_products["07N"].id,
        defaults={
            "is_enabled": True,
            "tracking_unit": "G",
            "default_unit_cost": 0.35,
            "currency": "USD",
        },
    )
    tp_07a = _get_or_create(
        db, TenantProduct,
        tenant_id=salon_one.id,
        product_id=redken_products["07A"].id,
        defaults={
            "is_enabled": True,
            "tracking_unit": "G",
            "default_unit_cost": 0.35,
            "currency": "USD",
        },
    )
    tp_dev = _get_or_create(
        db, TenantProduct,
        tenant_id=salon_one.id,
        product_id=developer.id,
        defaults={
            "is_enabled": True,
            "tracking_unit": "ML",
            "default_unit_cost": 0.02,
            "currency": "USD",
        },
    )
    db.flush()

    # Inventory items at Salon One main branch
    for tp, qty in [(tp_09n, 360.0), (tp_07n, 360.0), (tp_07a, 180.0), (tp_dev, 950.0)]:
        _get_or_create(
            db, InventoryItem,
            location_id=loc_one.id,
            tenant_product_id=tp.id,
            defaults={
                "tenant_id": salon_one.id,
                "on_hand_qty": qty,
                "reorder_level_qty": 60.0,
            },
        )
    db.flush()

    # ------------------------------------------------------------------
    # Tenant 2 — Salon Two (Basic)
    # ------------------------------------------------------------------

    salon_two = _get_or_create(db, Tenant, name="Salon Two", defaults={
        "plan": "basic",
        "status": "active",
    })
    db.flush()

    loc_two = _get_or_create(
        db, Location, tenant_id=salon_two.id, name="Salon Two — Downtown", defaults={
            "address": "456 Oak Avenue, Los Angeles, CA 90001",
            "timezone": "America/Los_Angeles",
        },
    )
    db.flush()

    _get_or_create(
        db, User, email="admin@salontwo.com", tenant_id=salon_two.id, defaults={
            "full_name": "Bob Owner",
            "password_hash": hash_password("password123"),
            "role": "ADMIN",
            "is_active": True,
            "default_location_id": loc_two.id,
        },
    )
    db.flush()

    # Tenant products for Salon Two (Wella)
    for product in wella_products.values():
        tp = _get_or_create(
            db, TenantProduct,
            tenant_id=salon_two.id,
            product_id=product.id,
            defaults={
                "is_enabled": True,
                "tracking_unit": "G",
                "default_unit_cost": 0.30,
                "currency": "USD",
            },
        )
        db.flush()
        _get_or_create(
            db, InventoryItem,
            location_id=loc_two.id,
            tenant_product_id=tp.id,
            defaults={
                "tenant_id": salon_two.id,
                "on_hand_qty": 300.0,
                "reorder_level_qty": 60.0,
            },
        )

    db.commit()
    print("  Tenants  : Salon One (premium), Salon Two (basic)")
    print("  Users    : admin@salonone.com / mike@salonone.com / admin@salontwo.com  [password123]")
    print("  Products : Redken Shades EQ (5 shades + developer), Wella Color Touch (2 shades)")


# ---------------------------------------------------------------------------
# Helper: get-or-create by unique lookup fields
# ---------------------------------------------------------------------------

def _get_or_create(db, model, defaults: dict | None = None, **lookup):
    instance = db.query(model).filter_by(**lookup).first()
    if instance:
        return instance
    params = {**lookup, **(defaults or {})}
    instance = model(**params)
    db.add(instance)
    return instance


if __name__ == "__main__":
    seed()

