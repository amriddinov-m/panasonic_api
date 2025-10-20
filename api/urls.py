from django.urls import path
from rest_framework import routers
from api.views import StatusViewSet, UnitTypeViewSet, ProductCategoryViewSet, ProductViewSet, WarehouseViewSet, \
    WarehouseProductViewSet, IncomeViewSet, IncomeItemViewSet, OutcomeViewSet, OutcomeItemViewSet, MovementViewSet, \
    MovementItemViewSet, OrderViewSet, OrderItemViewSet, SalesVolumeView, SalesVolumeCompareView, TopProductsView, \
    LeastPopularProductsView, DealersSalesView, DealersCompareView, DealerAvgCheckView, OrdersAndReturnsView, \
    SalesGeographyView, TopCategoriesView, AssortmentStructureView, CentralStockView, StocksByWarehouseDealerView, \
    ForecastShortagesView, PlanVsActualView, PlanAchievementView, OrdersCountView, AverageOrderAmountView, \
    MostOrderedProductsView, OrderImportView, IncomeImportView, BannerViewSet, CatalogViewSet

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
router.register(r'orders', OrderViewSet)
router.register(r'order-items', OrderItemViewSet)
router.register(r'banners', BannerViewSet)
router.register(r'catalogs', CatalogViewSet)


urlpatterns = [
    path("reports/sales-volume/", SalesVolumeView.as_view(), name="report-sales-volume"),
    path("reports/sales-volume/compare/", SalesVolumeCompareView.as_view(),
         name="report-sales-volume-compare"),
    path("reports/top-products/", TopProductsView.as_view(), name="report-top-products"),
    path("reports/least-popular-products/", LeastPopularProductsView.as_view(),
         name="report-least-popular-products"),
    path("reports/dealers-sales/", DealersSalesView.as_view(), name="report-dealers-sales"),
    path("reports/dealers-compare/", DealersCompareView.as_view(), name="report-dealers-compare"),
    path("reports/dealer-avg-check/", DealerAvgCheckView.as_view(), name="report-dealer-avg-check"),
    path("reports/orders-and-returns/", OrdersAndReturnsView.as_view(), name="report-orders-and-returns"),
    path("reports/sales-geography/", SalesGeographyView.as_view(),
         name="report-sales-geography"),
    path("reports/top-categories/", TopCategoriesView.as_view(),
         name="report-top-categories"),
    path("reports/assortment-structure/", AssortmentStructureView.as_view(),
         name="report-assortment-structure"),
    path("reports/central-stock/", CentralStockView.as_view(), name="report-central-stock"),
    path("reports/stocks-by-warehouse-dealer/", StocksByWarehouseDealerView.as_view(),
         name="report-stocks-by-warehouse-dealer"),
    path("reports/forecast-shortages/", ForecastShortagesView.as_view(),
         name="report-forecast-shortages"),
    path("reports/plan-vs-actual/", PlanVsActualView.as_view(), name="report-plan-vs-actual"),
    path("reports/plan-achievement/", PlanAchievementView.as_view(),
         name="report-plan-achievement"),
    path("reports/orders-count/", OrdersCountView.as_view(), name="report-orders-count"),
    path("reports/average-order-amount/", AverageOrderAmountView.as_view(),
         name="report-average-order-amount"),
    path("reports/most-ordered-products/", MostOrderedProductsView.as_view(),
         name="report-most-ordered-products"),
    path('orders/import/', OrderImportView.as_view(), name='order_import'),
    path('incomes/import/', IncomeImportView.as_view(), name='income_import'),
]
