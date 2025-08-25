from datetime import timedelta

from dateutil.relativedelta import relativedelta
from django.db.models import ExpressionWrapper, F, DecimalField, Sum, Count, Value
from django.db.models.functions import TruncDay, TruncWeek, TruncMonth, Coalesce
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .filters import WarehouseProductFilter
from .serializers import *


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class StatusViewSet(viewsets.ModelViewSet):
    queryset = Status.objects.order_by('-id')
    serializer_class = StatusSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'status', '_type', 'created', 'user']


class UnitTypeViewSet(viewsets.ModelViewSet):
    queryset = UnitType.objects.order_by('-id')
    serializer_class = UnitTypeSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'status', 'created', 'user']


class ProductCategoryViewSet(viewsets.ModelViewSet):
    queryset = ProductCategory.objects.order_by('-id')
    serializer_class = ProductCategorySerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'status', 'created', 'user']


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.order_by('-id')
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'category', 'unit_type', 'status', 'created', 'user']


class WarehouseViewSet(viewsets.ModelViewSet):
    queryset = Warehouse.objects.order_by('-id')
    serializer_class = WarehouseSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'created', 'user']


class WarehouseProductViewSet(viewsets.ModelViewSet):
    queryset = WarehouseProduct.objects.order_by('-id')
    serializer_class = WarehouseProductSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = WarehouseProductFilter


class IncomeViewSet(viewsets.ModelViewSet):
    queryset = Income.objects.order_by('-id')
    serializer_class = IncomeSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['client', 'created', 'user', 'status']


class IncomeItemViewSet(viewsets.ModelViewSet):
    queryset = IncomeItem.objects.order_by('-id')
    serializer_class = IncomeItemSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['income', 'product', 'status', 'user']


class OutcomeViewSet(viewsets.ModelViewSet):
    queryset = Outcome.objects.order_by('-id')
    serializer_class = OutcomeSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['client', 'created', 'user', 'status']


class OutcomeItemViewSet(viewsets.ModelViewSet):
    queryset = OutcomeItem.objects.order_by('-id')
    serializer_class = OutcomeItemSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['outcome', 'product', 'status', 'user']



class MovementViewSet(viewsets.ModelViewSet):
    queryset = Movement.objects.order_by('-id')
    serializer_class = MovementSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['warehouse_from', 'warehouse_to', 'user', 'created', 'status']


class MovementItemViewSet(viewsets.ModelViewSet):
    queryset = MovementItem.objects.order_by('-id')
    serializer_class = MovementItemSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['movement', 'product', 'user']


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.order_by('-id')
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['client', 'user', 'status', 'created']


class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.order_by('-id')
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['order', 'product', 'status']


class SalesVolumeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        group_by = request.query_params.get("group_by", "day")  # day|week|month
        date_from = request.query_params.get("date_from")
        date_to = request.query_params.get("date_to")
        warehouse_id = request.query_params.get("warehouse")
        client_id = request.query_params.get("client")
        product_id = request.query_params.get("product")
        status = request.query_params.get("status", Outcome.Status.finished)

        trunc = {"day": TruncDay, "week": TruncWeek, "month": TruncMonth}.get(group_by, TruncDay)

        qs = OutcomeItem.objects.select_related("outcome", "product")
        if status:
            qs = qs.filter(outcome__status=status)
        if date_from:
            qs = qs.filter(outcome__created__date__gte=date_from)
        if date_to:
            qs = qs.filter(outcome__created__date__lte=date_to)
        if warehouse_id:
            qs = qs.filter(outcome__warehouse_id=warehouse_id)
        if client_id:
            qs = qs.filter(outcome__client_id=client_id)
        if product_id:
            qs = qs.filter(product_id=product_id)

        amount_expr = ExpressionWrapper(
            F("count") * F("price"),
            output_field=DecimalField(max_digits=20, decimal_places=2)
        )

        zero_dec = Value(0, output_field=DecimalField(max_digits=20, decimal_places=2))

        agg = (
            qs.annotate(period=trunc("outcome__created"))
              .values("period")
              .annotate(
                  total_qty=Coalesce(Sum("count"), 0),                # Int OK
                  total_amount=Coalesce(Sum(amount_expr), zero_dec),  # <-- Decimal OK
                  orders=Count("outcome_id", distinct=True),
              )
              .order_by("period")
        )

        data = [
            {
                "period": item["period"].date().isoformat() if hasattr(item["period"], "date") else item["period"],
                "total_qty": item["total_qty"],
                "total_amount": item["total_amount"],
                "orders": item["orders"],
            }
            for item in agg
        ]
        return Response({"group_by": group_by, "results": data})


class SalesVolumeCompareView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        group_by = request.query_params.get("group_by", "day")   # day|week|month
        mode = request.query_params.get("mode", "prev")          # prev|yoy
        status = request.query_params.get("status", Outcome.Status.finished)

        date_from = request.query_params.get("date_from")
        date_to = request.query_params.get("date_to")

        # --- Определяем период по умолчанию (последние 30 дней)
        if not date_to or not date_from:
            now = timezone.now().date()
            date_to = date_to or now.isoformat()
            date_from = date_from or (now - timedelta(days=30)).isoformat()

        # Текущий диапазон
        cur_start = date_from
        cur_end = date_to

        # Сравнительный диапазон
        if mode == "yoy":
            # Тот же период год назад
            prev_start = (timezone.datetime.fromisoformat(cur_start) - relativedelta(years=1)).date().isoformat()
            prev_end = (timezone.datetime.fromisoformat(cur_end) - relativedelta(years=1)).date().isoformat()
        else:
            # Непосредственно предыдущий равный по длине период
            cur_len_days = (timezone.datetime.fromisoformat(cur_end).date()
                            - timezone.datetime.fromisoformat(cur_start).date()).days or 0
            prev_end_date = timezone.datetime.fromisoformat(cur_start).date() - timedelta(days=1)
            prev_start_date = prev_end_date - timedelta(days=cur_len_days)
            prev_start, prev_end = prev_start_date.isoformat(), prev_end_date.isoformat()

        trunc = {"day": TruncDay, "week": TruncWeek, "month": TruncMonth}.get(group_by, TruncDay)

        # Базовый QS + фильтры
        def base_qs():
            qs = OutcomeItem.objects.select_related("outcome", "product")
            if status:
                qs = qs.filter(outcome__status=status)
            warehouse = request.query_params.get("warehouse")
            client = request.query_params.get("client")
            product = request.query_params.get("product")
            if warehouse:
                qs = qs.filter(outcome__warehouse_id=warehouse)
            if client:
                qs = qs.filter(outcome__client_id=client)
            if product:
                qs = qs.filter(product_id=product)
            return qs

        amount_expr = ExpressionWrapper(
            F("count") * F("price"),
            output_field=DecimalField(max_digits=20, decimal_places=2)
        )
        zero_dec = Value(0, output_field=DecimalField(max_digits=20, decimal_places=2))

        def aggregate_range(start_date: str, end_date: str):
            qs = base_qs().filter(
                outcome__created__date__gte=start_date,
                outcome__created__date__lte=end_date
            )
            # Итоги
            totals = qs.aggregate(
                total_qty=Coalesce(Sum("count"), 0),
                total_amount=Coalesce(Sum(amount_expr), zero_dec),
                orders=Count("outcome_id", distinct=True),
            )
            # По корзинам
            buckets = (
                qs.annotate(period=trunc("outcome__created"))
                  .values("period")
                  .annotate(
                      total_qty=Coalesce(Sum("count"), 0),
                      total_amount=Coalesce(Sum(amount_expr), zero_dec),
                      orders=Count("outcome_id", distinct=True),
                  )
                  .order_by("period")
            )
            # нормализуем ключ периода в iso
            by_period = []
            for b in buckets:
                p = b["period"]
                key = p.date().isoformat() if hasattr(p, "date") else p
                by_period.append({
                    "period": key,
                    "total_qty": b["total_qty"],
                    "total_amount": b["total_amount"],
                    "orders": b["orders"],
                })
            return totals, by_period

        cur_totals, cur_periods = aggregate_range(cur_start, cur_end)
        prev_totals, prev_periods = aggregate_range(prev_start, prev_end)

        # Вычисляем дельты/проценты
        def diff(cur, prev):
            def pct(c, p):
                return float(c - p) / float(p) * 100.0 if p not in (0, None) else None
            return {
                "qty": {
                    "current": cur["total_qty"],
                    "previous": prev["total_qty"],
                    "delta": cur["total_qty"] - prev["total_qty"],
                    "pct": pct(cur["total_qty"], prev["total_qty"]),
                },
                "amount": {
                    "current": cur["total_amount"],
                    "previous": prev["total_amount"],
                    "delta": cur["total_amount"] - prev["total_amount"],
                    "pct": pct(cur["total_amount"], prev["total_amount"]),
                },
                "orders": {
                    "current": cur["orders"],
                    "previous": prev["orders"],
                    "delta": cur["orders"] - prev["orders"],
                    "pct": pct(cur["orders"], prev["orders"]),
                }
            }

        # Сшиваем корзины по ключу периода
        prev_map = {b["period"]: b for b in prev_periods}
        by_period = []
        for b in cur_periods:
            pkey = b["period"]
            prev_b = prev_map.get(pkey, {"total_qty": 0, "total_amount": 0, "orders": 0})
            def pct(c, p):
                return float(c - p) / float(p) * 100.0 if p not in (0, None) else None
            by_period.append({
                "period": pkey,
                "qty": {
                    "current": b["total_qty"],
                    "previous": prev_b["total_qty"],
                    "delta": b["total_qty"] - prev_b["total_qty"],
                    "pct": pct(b["total_qty"], prev_b["total_qty"]),
                },
                "amount": {
                    "current": b["total_amount"],
                    "previous": prev_b["total_amount"],
                    "delta": b["total_amount"] - prev_b["total_amount"],
                    "pct": pct(b["total_amount"], prev_b["total_amount"]),
                },
                "orders": {
                    "current": b["orders"],
                    "previous": prev_b["orders"],
                    "delta": b["orders"] - prev_b["orders"],
                    "pct": pct(b["orders"], prev_b["orders"]),
                },
            })

        result = {
            "group_by": group_by,
            "mode": mode,
            "current": {"date_from": cur_start, "date_to": cur_end},
            "previous": {"date_from": prev_start, "date_to": prev_end},
            "summary": diff(cur_totals, prev_totals),
            "by_period": by_period,
        }
        return Response(result)


class TopProductsView(APIView):
    """
    GET /api/reports/top-products/
        ?metric=amount|qty
        &limit=20
        &date_from=YYYY-MM-DD
        &date_to=YYYY-MM-DD
        &warehouse=ID
        &client=ID
        &status=finished|active|...
        &category=ID
        &product=ID   (можно передавать несколько: ?product=560&product=561)

    Возвращает топ товаров с полями:
    - product_id, product_name, unit_type, category_id, category_name
    - total_qty, total_amount, orders
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        metric = request.query_params.get("metric", "amount")   # amount|qty
        try:
            limit = int(request.query_params.get("limit", 20))
        except ValueError:
            limit = 20
        limit = max(1, min(limit, 500))  # ограничим разумно

        date_from = request.query_params.get("date_from")
        date_to = request.query_params.get("date_to")
        warehouse_id = request.query_params.get("warehouse")
        client_id = request.query_params.get("client")
        category_id = request.query_params.get("category")
        status = request.query_params.get("status", Outcome.Status.finished)

        qs = OutcomeItem.objects.select_related("outcome", "product", "product__category")

        # Фильтры
        if status:
            qs = qs.filter(outcome__status=status)
        if date_from:
            qs = qs.filter(outcome__created__date__gte=date_from)
        if date_to:
            qs = qs.filter(outcome__created__date__lte=date_to)
        if warehouse_id:
            qs = qs.filter(outcome__warehouse_id=warehouse_id)
        if client_id:
            qs = qs.filter(outcome__client_id=client_id)
        if category_id:
            qs = qs.filter(product__category_id=category_id)

        # фильтр по нескольким product (повторяющийся параметр в query string)
        product_ids = request.query_params.getlist("product")
        if product_ids:
            qs = qs.filter(product_id__in=product_ids)

        # Агрегации
        amount_expr = ExpressionWrapper(
            F("count") * F("price"),
            output_field=DecimalField(max_digits=20, decimal_places=2),
        )
        zero_dec = Value(0, output_field=DecimalField(max_digits=20, decimal_places=2))

        grouped = (
            qs.values(
                "product_id",
                "product__name",
                "product__unit_type",
                "product__category_id",
                "product__category__name",
            )
            .annotate(
                total_qty=Coalesce(Sum("count"), 0),
                total_amount=Coalesce(Sum(amount_expr), zero_dec),
                orders=Count("outcome_id", distinct=True),
            )
        )

        if metric == "qty":
            grouped = grouped.order_by("-total_qty", "product__name")
        else:  # amount
            grouped = grouped.order_by("-total_amount", "product__name")

        data = [
            {
                "product_id": r["product_id"],
                "product_name": r["product__name"],
                "unit_type": r["product__unit_type"],
                "category_id": r["product__category_id"],
                "category_name": r["product__category__name"],
                "total_qty": r["total_qty"],
                "total_amount": r["total_amount"],
                "orders": r["orders"],
            }
            for r in grouped[:limit]
        ]

        # опционально — добавить номер в рейтинге
        for i, item in enumerate(data, start=1):
            item["rank"] = i

        return Response({
            "metric": metric,
            "limit": limit,
            "count": len(data),
            "results": data
        })


class LeastPopularProductsView(APIView):
    """
    GET /api/reports/least-popular-products/
        ?metric=amount|qty
        &limit=20
        &date_from=YYYY-MM-DD
        &date_to=YYYY-MM-DD
        &warehouse=ID
        &client=ID
        &status=finished|active|...
        &category=ID
        &product=ID

    Возвращает наименее популярные товары:
    - product_id, product_name, unit_type, category_id, category_name
    - total_qty, total_amount, orders
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        metric = request.query_params.get("metric", "amount")
        try:
            limit = int(request.query_params.get("limit", 20))
        except ValueError:
            limit = 20
        limit = max(1, min(limit, 500))

        date_from = request.query_params.get("date_from")
        date_to = request.query_params.get("date_to")
        warehouse_id = request.query_params.get("warehouse")
        client_id = request.query_params.get("client")
        category_id = request.query_params.get("category")
        status = request.query_params.get("status", Outcome.Status.finished)

        qs = OutcomeItem.objects.select_related("outcome", "product", "product__category")

        # Фильтры
        if status:
            qs = qs.filter(outcome__status=status)
        if date_from:
            qs = qs.filter(outcome__created__date__gte=date_from)
        if date_to:
            qs = qs.filter(outcome__created__date__lte=date_to)
        if warehouse_id:
            qs = qs.filter(outcome__warehouse_id=warehouse_id)
        if client_id:
            qs = qs.filter(outcome__client_id=client_id)
        if category_id:
            qs = qs.filter(product__category_id=category_id)
        product_ids = request.query_params.getlist("product")
        if product_ids:
            qs = qs.filter(product_id__in=product_ids)

        # Агрегации
        amount_expr = ExpressionWrapper(
            F("count") * F("price"),
            output_field=DecimalField(max_digits=20, decimal_places=2),
        )
        zero_dec = Value(0, output_field=DecimalField(max_digits=20, decimal_places=2))

        grouped = (
            qs.values(
                "product_id",
                "product__name",
                "product__unit_type",
                "product__category_id",
                "product__category__name",
            )
            .annotate(
                total_qty=Coalesce(Sum("count"), 0),
                total_amount=Coalesce(Sum(amount_expr), zero_dec),
                orders=Count("outcome_id", distinct=True),
            )
        )

        # Сортировка: наоборот (от наименьшего к большему)
        if metric == "qty":
            grouped = grouped.order_by("total_qty", "product__name")
        else:
            grouped = grouped.order_by("total_amount", "product__name")

        data = []
        for i, r in enumerate(grouped[:limit], start=1):
            data.append({
                "rank": i,
                "product_id": r["product_id"],
                "product_name": r["product__name"],
                "unit_type": r["product__unit_type"],
                "category_id": r["product__category_id"],
                "category_name": r["product__category__name"],
                "total_qty": r["total_qty"],
                "total_amount": r["total_amount"],
                "orders": r["orders"],
            })

        return Response({
            "metric": metric,
            "limit": limit,
            "count": len(data),
            "results": data
        })
