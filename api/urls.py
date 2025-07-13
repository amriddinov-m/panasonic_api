from rest_framework import routers
from api.views import StatusViewSet, UnitTypeViewSet, ProductCategoryViewSet, ProductViewSet, WarehouseViewSet, \
    WarehouseProductViewSet, IncomeViewSet, IncomeItemViewSet, OutcomeViewSet, OutcomeItemViewSet, MovementViewSet, \
    MovementItemViewSet

router = routers.SimpleRouter()
router.register(r'statuses', StatusViewSet)
router.register(r'unit-types', UnitTypeViewSet)
router.register(r'product-categories', ProductCategoryViewSet)
router.register(r'products', ProductViewSet)
router.register(r'warehouses', WarehouseViewSet)
router.register(r'warehouse-products', WarehouseProductViewSet)
router.register(r'incomes', IncomeViewSet)
router.register(r'income-items', IncomeItemViewSet)
router.register(r'outcomes', OutcomeViewSet)
router.register(r'outcome-items', OutcomeItemViewSet)
router.register(r'movements', MovementViewSet)
router.register(r'movement-items', MovementItemViewSet)
