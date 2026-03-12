# Import all models so SQLAlchemy can register them and create tables
from src.models.tenant import Tenant, Location  # noqa: F401
from src.models.user import User  # noqa: F401
from src.models.customer import Customer  # noqa: F401
from src.models.product import Brand, ProductLine, Product  # noqa: F401
from src.models.tenant_product import TenantProduct  # noqa: F401
from src.models.inventory import InventoryItem, InventoryTxn  # noqa: F401
from src.models.formula import Formula, FormulaItem  # noqa: F401


