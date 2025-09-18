# <app_name>/management/commands/seed_reports_demo.py
import random
from datetime import datetime, timedelta, date
from decimal import Decimal, ROUND_HALF_UP

from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Min
from django.utils import timezone
from django.contrib.auth import get_user_model

from api.models import (  # 🤚 ЗАМЕНИ "app" на имя твоего приложения с моделями
    Product, ProductCategory,
    Warehouse, WarehouseProduct,
    Order, OrderItem,
    Outcome, OutcomeItem,
    Income, IncomeItem,
    Report, ReportItem,
)

# ------------------------
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# ------------------------

def dec(x) -> Decimal:
    return Decimal(str(x)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

def pick(seq):
    return seq[random.randrange(len(seq))]

def month_range(months_back: int):
    """Список (year, month) от (сегодня - months_back+1) до текущего месяца включительно."""
    today = timezone.now().date().replace(day=1)
    out = []
    for i in range(months_back):
        m = today.month - (months_back - 1 - i)
        y = today.year
        while m <= 0:
            m += 12
            y -= 1
        out.append((y, m))
    return out  # [(2024, 8), (2024, 9), ...]


def ensure_user_minimal(label: str, idx: int):
    """
    Пытаемся создать пользователя с минимальным набором полей.
    Если не получится (например, кастомная модель требует особые поля), вернём существующего id=1.
    """
    User = get_user_model()
    try:
        field_names = {f.name for f in User._meta.get_fields()}
        kwargs = {}
        # Первично — пробуем email/first_name/last_name
        if "email" in field_names:
            kwargs["email"] = f"{label}.{idx}@example.local"
        if "first_name" in field_names:
            kwargs["first_name"] = f"{label.capitalize()}{idx}"
        if "last_name" in field_names:
            kwargs["last_name"] = "Demo"
        if "username" in field_names:
            kwargs["username"] = f"{label}{idx}"

        # Попробуем create (не create_user — чтобы не требовать password)
        u = User.objects.create(**kwargs)
        return u
    except Exception:
        # fallback: пытаемся взять существующего id=1
        try:
            return User.objects.get(pk=1)
        except User.DoesNotExist:
            # ну совсем край — создадим «сырая» запись с минималкой по тому, что есть
            kwargs = {}
            if "email" in field_names:
                kwargs["email"] = f"demo@{label}.local"
            if "first_name" in field_names:
                kwargs["first_name"] = "Demo"
            if "last_name" in field_names:
                kwargs["last_name"] = "User"
            if "username" in field_names:
                kwargs["username"] = f"{label}demo"
            return User.objects.create(**kwargs)


def ensure_warehouses(creator):
    warehouses = list(Warehouse.objects.all()[:3])
    if len(warehouses) >= 3:
        return warehouses
    # создаём 3 склада: Центральный, Восток, Запад
    names = ["Центральный склад", "Склад Восток", "Склад Запад"]
    existing_names = {w.name for w in warehouses}
    to_create = []
    for name in names:
        if name not in existing_names:
            to_create.append(Warehouse(name=name, responsible=creator, user=creator))
    if to_create:
        Warehouse.objects.bulk_create(to_create)
    return list(Warehouse.objects.all()[:3])


def ensure_categories_and_prices(creator, products):
    """
    У товаров может не быть категории/цены. Создадим несколько категорий
    и раздадим товары по категориям и ценам.
    """
    if not products:
        return

    cats = list(ProductCategory.objects.all())
    if not cats:
        cats = [
            ProductCategory(name="Стройматериалы", status="active", user=creator),
            ProductCategory(name="Инструменты", status="active", user=creator),
            ProductCategory(name="Сантехника", status="active", user=creator),
        ]
        ProductCategory.objects.bulk_create(cats)
        cats = list(ProductCategory.objects.all())

    # Установим цену, если 0/None, и категорию, если нет
    updates = []
    for p in products:
        changed = False
        if p.price is None or p.price == 0:
            p.price = dec(random.randint(50, 2500) / (10 if p.unit_type == "kg" else 1))
            changed = True
        if p.category_id is None:
            p.category = pick(cats)
            changed = True
        if changed:
            updates.append(p)
    if updates:
        Product.objects.bulk_update(updates, ["price", "category"])


def ensure_products(creator, min_count=50):
    """
    Гарантируем наличие достаточного количества товаров.
    Если уже есть — используем их. Иначе создаём.
    """
    products = list(Product.objects.all())
    if len(products) >= min_count:
        ensure_categories_and_prices(creator, products)
        return products

    # создадим недостающее
    to_create = []
    for i in range(min_count - len(products)):
        unit = pick(["pcs", "kg"])
        to_create.append(Product(
            name=f"DEMO Товар {i+1}",
            unit_type=unit,
            price=dec(random.randint(100, 5000) / (10 if unit == "kg" else 1)),
            status="active",
            user=creator,
            category=None,  # проставим ниже
        ))
    if to_create:
        Product.objects.bulk_create(to_create)

    products = list(Product.objects.all())
    ensure_categories_and_prices(creator, products)
    return products


def ensure_clients(count, fallback_user):
    """
    Создаём N клиентов (дилеров). При проблемах — возвращаем список из fallback_user * N.
    """
    created = []
    for i in range(count):
        u = ensure_user_minimal("client", i + 1)
        created.append(u)
    # если все одинаковые (fallback), то вернём уникальный список через set?
    # Для отчётов лучше иметь >=2 уникальных. Если вдруг один — просто дублируем id=1.
    return created or [fallback_user]


def dt_random_in_month(y, m):
    # случайный день месяца (1..28, чтобы не париться с длиной)
    d = random.randint(1, 28)
    h = random.randint(9, 18)
    mi = random.randint(0, 59)
    return timezone.make_aware(datetime(y, m, d, h, mi))


# ------------------------
# ОСНОВНАЯ КОМАНДА
# ------------------------

class Command(BaseCommand):
    help = "Создаёт демо-данные для отчётов (планы, заказы, отгрузки, приходы, остатки)."

    def add_arguments(self, parser):
        parser.add_argument("--months", type=int, default=14, help="Сколько месяцев назад генерировать (включая текущий). По умолчанию 14.")
        parser.add_argument("--clients", type=int, default=5, help="Сколько дилеров создать (если можно). По умолчанию 5.")
        parser.add_argument("--orders-per-month", type=int, default=120, help="Примерное кол-во заказов в месяц (на всех дилеров и склады).")
        parser.add_argument("--seed", type=int, default=42, help="Seed для детерминированности.")
        parser.add_argument("--central-stock", type=int, default=1, help="Стартовый запас на центральном складе (множитель).")

    def handle(self, *args, **opts):
        random.seed(opts["seed"])

        months_back = max(2, opts["months"])
        clients_n = max(1, opts["clients"])
        orders_target = max(20, opts["orders_per_month"])
        central_stock_factor = max(1, opts["central_stock"])

        self.stdout.write(self.style.NOTICE(f"Generating demo data: months={months_back}, clients={clients_n}, orders/month≈{orders_target}"))

        # 1) Базовые сущности
        User = get_user_model()
        creator = None
        try:
            creator = User.objects.get(pk=1)
        except User.DoesNotExist:
            creator = ensure_user_minimal("owner", 1)

        warehouses = ensure_warehouses(creator)
        central = warehouses[0]
        products = ensure_products(creator, min_count=80)
        clients = ensure_clients(clients_n, fallback_user=creator)

        # 2) Начальные остатки (WarehouseProduct) — на центральном и немного на остальных
        #    Чтобы «остатки» и «дефициты» работали сразу.
        self._seed_initial_stocks(products, warehouses, creator, central_stock_factor)

        # 3) Планы (Report + ReportItem) — для каждого клиента по месяцам
        #    План = базовый оборот по клиенту, с разбросом по продуктам.
        months = month_range(months_back)
        self._seed_plans(months, clients, products, creator)

        # 4) Заказы (Order + OrderItem) и Отгрузки (Outcome + OutcomeItem)
        #    Итоги в среднем около плана ± случайный шум.
        self._seed_orders_and_outcomes(months, clients, products, warehouses, creator, orders_target)

        # 5) Приходы (Income + IncomeItem): часть pending/active — чтобы «дефициты» учитывали будущие поставки
        self._seed_incomes(months, products, warehouses, creator)

        self.stdout.write(self.style.SUCCESS("Demo data generated successfully."))

    # ------------- GENERATORS -------------

    def _seed_initial_stocks(self, products, warehouses, creator, factor: int):
        """
        Бросаем стартовый запас: на центральном — побольше; на остальных — поменьше.
        """
        existing = WarehouseProduct.objects.count()
        if existing > 0:
            return

        to_create = []
        for w in warehouses:
            for p in random.sample(products, k=max(10, len(products)//2)):
                base = random.randint(5, 40)
                qty = base * (3 if w == warehouses[0] else 1) * factor
                price = p.price or dec(random.randint(100, 5000))
                to_create.append(WarehouseProduct(
                    product=p, warehouse=w, count=qty, price=price, status="in_stock", user=creator
                ))
        WarehouseProduct.objects.bulk_create(to_create)

    def _seed_plans(self, months, clients, products, creator):
        """
        Report(status=confirmed) per client per month.
        ReportItem.count планируется в «штуках» (или кг), деньги считаем по Product.price.
        """
        # не будем дублировать планы, если уже есть confirmed за эти месяцы
        have_any = Report.objects.filter(status=Report.Status.confirmed).exists()
        if have_any:
            return

        for (y, m) in months:
            for client in clients:
                r = Report.objects.create(
                    client=client, comment=f"План на {y}-{m:02d}", status=Report.Status.confirmed, period=m
                )
                # для плана берём подмножество товаров
                items = []
                # 10–20 SKU в плане
                skus = random.sample(products, k=random.randint(10, 20))
                for p in skus:
                    # базовый план в штуках/кг
                    base = random.randint(5, 60)
                    items.append(ReportItem(
                        report=r, product=p, count=base
                    ))
                ReportItem.objects.bulk_create(items)

    def _seed_orders_and_outcomes(self, months, clients, products, warehouses, creator, orders_target):
        """
        На каждый месяц: создаём пачку Order/OrderItem и Outcome/OutcomeItem (фактические).
        Часть заказов отменяем/доставляем; фактические — в статусе finished.
        """
        # не пересоздаём, если уже есть заказы/отгрузки за самый ранний месяц
        if Order.objects.exists() and Outcome.objects.exists():
            return

        for (y, m) in months:
            # сколько заказов в этом месяце: от 70% до 130% цели
            orders_in_month = max(10, int(orders_target * random.uniform(0.7, 1.3)))
            all_orders = []
            all_oitems = []
            all_outcomes = []
            all_out_items = []

            for _ in range(orders_in_month):
                client = pick(clients)
                wh = pick(warehouses)
                created_dt = dt_random_in_month(y, m)

                # Статус заказа
                status = random.choices(
                    population=[
                        Order.Status.pending,
                        Order.Status.collected,
                        Order.Status.delivering,
                        Order.Status.delivered,
                        Order.Status.sent,
                        Order.Status.cancelled,
                    ],
                    weights=[10, 10, 15, 40, 15, 10],
                    k=1
                )[0]

                o = Order(
                    client=client, user=creator, warehouse=wh,
                    comment="DEMO Order", status=status,
                    total_amount=dec(0), created=created_dt, updated=created_dt
                )
                all_orders.append(o)

            Order.objects.bulk_create(all_orders)

            # Привяжем айтемы к заказам
            # каждый заказ: 1–5 SKU по 1–50 шт
            orders = list(Order.objects.filter(created__year=y, created__month=m))
            for o in orders:
                n_items = random.randint(1, 5)
                skus = random.sample(products, k=n_items)
                total = dec(0)
                for p in skus:
                    qty = random.randint(1, 50)
                    price = p.price or dec(random.randint(100, 5000))
                    all_oitems.append(OrderItem(
                        order=o, product=p, count=qty, price=price, status="ok", user=creator
                    ))
                    total += dec(qty) * dec(price)
                o.total_amount = total
            Order.objects.bulk_update(orders, ["total_amount"])

            OrderItem.objects.bulk_create(all_oitems)

            # Фактические отгрузки — создадим для 70–85% заказов (как finished)
            realized_orders = random.sample(orders, k=int(len(orders) * random.uniform(0.7, 0.85)))
            for o in realized_orders:
                # копируем позиции заказа в Outcome
                out = Outcome(
                    client=o.client, status=Outcome.Status.finished, user=creator,
                    comment=f"DEMO Outcome for order {o.id}",
                    total_amount=dec(0), warehouse=o.warehouse,
                    created=o.created + timedelta(hours=1), updated=o.created + timedelta(hours=1)
                )
                all_outcomes.append(out)

            Outcome.objects.bulk_create(all_outcomes)
            outcomes = list(Outcome.objects.filter(created__year=y, created__month=m))

            # сопоставим заказ->отгрузка по времени/клиенту/складу
            # (приблизительно: количество одинаковое)
            o_by_key = {}
            for o in realized_orders:
                key = (o.client_id, o.warehouse_id)
                o_by_key.setdefault(key, []).append(o)

            out_by_key = {}
            for out in outcomes:
                key = (out.client_id, out.warehouse_id)
                out_by_key.setdefault(key, []).append(out)

            # создаём OutcomeItem по тем же SKU, что в заказе, уменьшив/изменив qty +/- 20%
            for key, ords in o_by_key.items():
                outs = out_by_key.get(key, [])
                for idx, order in enumerate(ords):
                    if idx >= len(outs):
                        break
                    out = outs[idx]
                    items = list(OrderItem.objects.filter(order=order))
                    total = dec(0)
                    for it in items:
                        # 80–120% от заказанного
                        qty = max(1, int(it.count * random.uniform(0.8, 1.2)))
                        price = it.price
                        all_out_items.append(OutcomeItem(
                            outcome=out, product=it.product, count=qty, price=price, status="ok", user=creator
                        ))
                        total += dec(qty) * dec(price)
                    out.total_amount = total

            if all_out_items:
                OutcomeItem.objects.bulk_create(all_out_items)
            if outcomes:
                Outcome.objects.bulk_update(outcomes, ["total_amount"])

    def _seed_incomes(self, months, products, warehouses, creator):
        """
        Приходы (часть pending/active), чтобы отчёт по дефицитам мог учитывать ожидаемые приходы.
        """
        # если уже есть какие-то приходы — не плодим
        if Income.objects.exists():
            return

        for (y, m) in months[-6:]:  # последние 6 месяцев — достаточно
            for _ in range(random.randint(5, 12)):
                wh = pick(warehouses)
                created_dt = dt_random_in_month(y, m)
                status = random.choice([Income.Status.pending, Income.Status.active, Income.Status.finished])

                inc = Income(
                    client=creator,  # формально клиент, можно завести отдельного
                    user=creator, comment="DEMO Income", status=status,
                    total_amount=dec(0), warehouse=wh,
                    created=created_dt, updated=created_dt
                )
                inc.save()

                n_items = random.randint(1, 5)
                items = []
                total = dec(0)
                for p in random.sample(products, k=n_items):
                    qty = random.randint(5, 80)
                    price = p.price or dec(random.randint(100, 5000))
                    items.append(IncomeItem(
                        income=inc, product=p, count=qty, price=price, status="ok", user=creator
                    ))
                    total += dec(qty) * dec(price)
                IncomeItem.objects.bulk_create(items)
                inc.total_amount = total
                inc.save()
