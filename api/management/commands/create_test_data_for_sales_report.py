# your_app/management/commands/seed_outcomes.py
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db import transaction
from decimal import Decimal
import random
from datetime import timedelta, datetime, date, time as dtime

from user.models import User
from api.models import Product, Warehouse, Outcome, OutcomeItem


def _rand_dt_in_range(start_date: date, end_date: date) -> timezone.datetime:
    # случайная дата и рандомное время суток; учитываем TZ
    days = (end_date - start_date).days
    rand_day = start_date + timedelta(days=random.randint(0, max(days, 0)))
    rand_time = dtime(hour=random.randint(8, 18), minute=random.randint(0, 59), second=random.randint(0, 59))
    naive = datetime.combine(rand_day, rand_time)
    return timezone.make_aware(naive, timezone.get_current_timezone())


class Command(BaseCommand):
    help = "Создать тестовые расходы (Outcome + OutcomeItem) на существующих продуктах (id 560–800)."

    def add_arguments(self, parser):
        parser.add_argument("--days", type=int, default=None,
                            help="Если date-from/date-to не заданы, раскидать за последние N дней.")
        parser.add_argument("--date-from", type=str, default=None, help="YYYY-MM-DD")
        parser.add_argument("--date-to", type=str, default=None, help="YYYY-MM-DD")
        parser.add_argument("--yoy", action="store_true",
                            help="Дополнительно создать такой же объём данных за аналогичный период год назад.")
        parser.add_argument("--outcomes", type=int, default=100, help="Сколько Outcome создать (на период).")
        parser.add_argument("--min-items", type=int, default=1)
        parser.add_argument("--max-items", type=int, default=5)
        parser.add_argument("--seed", type=int, default=42)

    @transaction.atomic
    def handle(self, *args, **opts):
        random.seed(opts["seed"])

        # user и продукты
        try:
            user = User.objects.get(pk=1)
        except User.DoesNotExist:
            self.stderr.write(self.style.ERROR("Нет пользователя с id=1"))
            return

        products = list(Product.objects.filter(id__gte=560, id__lte=800))
        if not products:
            self.stderr.write(self.style.ERROR("Нет продуктов с id в диапазоне 560–800"))
            return

        # склад
        warehouse = Warehouse.objects.first()
        if not warehouse:
            warehouse = Warehouse.objects.create(name="Тестовый склад", user=user, responsible=user)

        # определить периоды
        date_from_str = opts.get("date-from")
        date_to_str = opts.get("date-to")
        periods = []

        if date_from_str and date_to_str:
            cur_from = date.fromisoformat(date_from_str)
            cur_to = date.fromisoformat(date_to_str)
        else:
            # если даты не заданы — используем последние N дней (по умолчанию 90)
            days = opts["days"] if opts["days"] is not None else 90
            cur_to = timezone.now().date()
            cur_from = cur_to - timedelta(days=days)

        periods.append(("current", cur_from, cur_to))

        if opts["yoy"]:
            prev_from = date(cur_from.year - 1, cur_from.month, cur_from.day)
            prev_to = date(cur_to.year - 1, cur_to.month, cur_to.day)
            periods.append(("yoy", prev_from, prev_to))

        def make_outcomes(period_name: str, start_d: date, end_d: date):
            created = []
            for i in range(opts["outcomes"]):
                created_dt = _rand_dt_in_range(start_d, end_d)
                outcome = Outcome.objects.create(
                    client=user,
                    user=user,
                    warehouse=warehouse,
                    status=Outcome.Status.finished,
                    comment=f"[{period_name}] Тестовый расход #{i+1}",
                    total_amount=Decimal("0.00"),
                    reason="seed"
                )
                # переписываем created/updated
                Outcome.objects.filter(pk=outcome.pk).update(created=created_dt, updated=created_dt)
                created.append(outcome)

            # строки
            for outcome in created:
                items_count = random.randint(opts["min_items"], opts["max_items"])
                total = Decimal("0.00")
                for _ in range(items_count):
                    product = random.choice(products)
                    count = random.randint(1, 20)
                    price = product.price or Decimal("100.00")
                    OutcomeItem.objects.create(
                        outcome=outcome, product=product, count=count,
                        price=price, status="active", user=user
                    )
                    total += price * count
                outcome.total_amount = total
                outcome.save(update_fields=["total_amount"])

            self.stdout.write(self.style.SUCCESS(
                f"{period_name}: создано Outcome {len(created)} ({start_d}..{end_d})"
            ))

        for name, dfrom, dto in periods:
            make_outcomes(name, dfrom, dto)

        self.stdout.write(self.style.SUCCESS("Готово. Теперь проверь отчёты /api/reports/sales-volume и compare."))
