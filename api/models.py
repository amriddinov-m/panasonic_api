from django.db import models


class Status(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    _type = models.CharField(max_length=255, verbose_name='Тип')
    status = models.BooleanField(default=True, verbose_name='Статус')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, verbose_name='Пользователь',
                             related_name='status_user')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'


class UnitType(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    status = models.CharField(max_length=255, verbose_name='Статус', null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, verbose_name='Пользователь')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Ед. измерение'
        verbose_name_plural = 'Ед. измерения'


class ProductCategory(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    status = models.CharField(max_length=255, verbose_name='Статус', null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, verbose_name='Пользователь', null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория продуктов'
        verbose_name_plural = 'Категории продуктов'


class Product(models.Model):
    class UnitType(models.TextChoices):
        pcs = 'pcs', 'Шт.'
        kg = 'kg', 'Кг.'

    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, verbose_name='Категория')
    code = models.CharField(max_length=255, verbose_name='Код продукта', null=True)
    name = models.CharField(max_length=255, verbose_name='Название')
    unit_type = models.CharField(max_length=255, verbose_name='Ед. изм', choices=UnitType.choices, default=UnitType.pcs)
    price = models.DecimalField(decimal_places=2, max_digits=15, default=0, verbose_name='Цена')
    status = models.CharField(max_length=255, verbose_name='Статус', null=True)
    comment = models.TextField(verbose_name='Коммент', null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, verbose_name='Пользователь', null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class Warehouse(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    responsible = models.ForeignKey('user.User', on_delete=models.CASCADE, verbose_name='Ответственный',
                                    related_name='responsible_warehouses', null=True)
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, verbose_name='Пользователь')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Склад'
        verbose_name_plural = 'Склады'


class WarehouseProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, verbose_name='Склад', null=True)
    count = models.IntegerField(verbose_name='Кол-во')
    status = models.CharField(max_length=255, verbose_name='Статус', null=True)
    price = models.DecimalField(decimal_places=2, max_digits=15, verbose_name='Цена', default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, verbose_name='Пользователь', null=True)

    def __str__(self):
        return f'{self.product.name} - {self.count}'

    class Meta:
        verbose_name = 'Продукт в складе'
        verbose_name_plural = 'Продукты в складе'


class Income(models.Model):
    class Status(models.TextChoices):
        pending = 'pending', 'В ожидании'
        active = 'active', 'Активный'
        finished = 'finished', 'Закончен'
        cancelled = 'cancelled', 'Отменен'

    client = models.ForeignKey('user.User', on_delete=models.CASCADE, verbose_name='Клиент',
                               related_name='income_client')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, verbose_name='Пользователь',
                             related_name='income_user')
    comment = models.TextField(verbose_name='Коммент')
    status = models.CharField(max_length=255, verbose_name='Статус',
                              choices=Status.choices, default=Status.pending, null=True)
    total_amount = models.IntegerField(default=0, verbose_name='Общая сумма')
    warehouse = models.ForeignKey('Warehouse', on_delete=models.CASCADE, verbose_name='Склад', null=True)

    def __str__(self):
        return f'{self.id}'

    class Meta:
        verbose_name = 'Приход'
        verbose_name_plural = 'Приходы'


class IncomeItem(models.Model):
    income = models.ForeignKey(Income, on_delete=models.CASCADE, verbose_name='Приход')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')
    count = models.IntegerField(verbose_name='Кол-во')
    price = models.DecimalField(decimal_places=2, max_digits=15, verbose_name='Цена')
    comment = models.TextField(verbose_name='Коммент', null=True)
    status = models.CharField(max_length=255, verbose_name='Статус', null=True)
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, verbose_name='Пользователь', null=True)

    def __str__(self):
        return f'{self.id}'

    class Meta:
        verbose_name = 'Элемент прихода'
        verbose_name_plural = 'Элементы прихода'


class Outcome(models.Model):
    class Status(models.TextChoices):
        pending = 'pending', 'В ожидании'
        active = 'active', 'Активный'
        finished = 'finished', 'Закончен'
        cancelled = 'cancelled', 'Отменен'

    client = models.ForeignKey('user.User', on_delete=models.CASCADE, verbose_name='Клиент',
                               related_name='outcome_client')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=255, verbose_name='Статус',
                              choices=Status.choices, default=Status.pending, null=True)
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, verbose_name='Пользователь',
                             related_name='outcome_user')
    comment = models.TextField(verbose_name='Коммент')
    total_amount = models.IntegerField(default=0, verbose_name='Общая сумма')
    warehouse = models.ForeignKey('Warehouse', on_delete=models.CASCADE, verbose_name='Склад', null=True)
    reason = models.TextField(verbose_name='Причина', null=True)

    def __str__(self):
        return f'{self.id}'

    class Meta:
        verbose_name = 'Расход'
        verbose_name_plural = 'Расходы'


class OutcomeItem(models.Model):
    outcome = models.ForeignKey(Outcome, on_delete=models.CASCADE, verbose_name='Расход', related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')
    count = models.IntegerField(verbose_name='Кол-во')
    status = models.CharField(max_length=255, verbose_name='Статус', null=True)
    price = models.DecimalField(decimal_places=2, max_digits=15, verbose_name='Цена')
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, verbose_name='Пользователь')

    def __str__(self):
        return f'{self.id}'

    class Meta:
        verbose_name = 'Элемент расходы'
        verbose_name_plural = 'Элементы расхода'


class Movement(models.Model):
    class Status(models.TextChoices):
        pending = 'pending', 'В ожидании'
        collected = 'collected', 'Собрано'
        sent = 'sent', 'Отправлено'
        received = 'received', 'Получено'
        finished = 'finished', 'Закончено'
        cancelled = 'cancelled', 'Отменено'
        confirmed_cancel = 'confirmed_cancel', 'Отмена подтверждена'

    warehouse_from = models.ForeignKey('Warehouse', on_delete=models.CASCADE, verbose_name='С какого склада',
                                       related_name='warehouse_from')
    warehouse_to = models.ForeignKey('Warehouse', on_delete=models.CASCADE, verbose_name='На какой склад',
                                     related_name='warehouse_to')
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, verbose_name='Пользователь')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=255, verbose_name='Статус', choices=Status.choices, default=Status.pending)
    comment = models.TextField(verbose_name='Коммент')

    def __str__(self):
        return f'{self.id}'

    class Meta:
        verbose_name = 'Пермещение'
        verbose_name_plural = 'Перемещения'


class MovementItem(models.Model):
    movement = models.ForeignKey(Movement, on_delete=models.CASCADE, verbose_name='Перемещение', related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')
    count = models.IntegerField(verbose_name='Кол-во', default=0)
    comment = models.TextField(verbose_name='Коммент')
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, verbose_name='Пользователь')

    def __str__(self):
        return f'{self.id}'

    class Meta:
        verbose_name = 'Элемент перемещения'
        verbose_name_plural = 'Элементы перемещения'


class Order(models.Model):
    class Status(models.TextChoices):
        pending = 'pending', 'В ожидании'
        collected = 'collected', 'Собрано'
        delivering = 'delivering', 'Доставляется'
        delivered = 'delivered', 'Доставлено'
        sent = 'sent', 'Отправлено'
        cancelled = 'cancelled', 'Отменено'

    client = models.ForeignKey('user.User', on_delete=models.CASCADE, verbose_name='Клиент',
                               related_name='order_client')
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, verbose_name='Пользователь')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    comment = models.TextField(verbose_name='Комментарии', null=True)
    total_amount = models.DecimalField(decimal_places=2, max_digits=10, default=0, verbose_name='Общая сумма')
    status = models.CharField(max_length=255, verbose_name='Статус', choices=Status.choices, default=Status.pending)

    def __str__(self):
        return f'{self.id}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class OrderItem(models.Model):
    class Status(models.TextChoices):
        pending = 'pending', 'В ожидании'
        ready = 'ready', 'Готово'
        cancelled = 'cancelled', 'Отменено'

    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Заказ', related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')
    count = models.IntegerField(verbose_name='Кол-во', default=0)
    comment = models.TextField(verbose_name='Коммент', null=True)
    price = models.DecimalField(decimal_places=2, max_digits=15, verbose_name='Цена')
    status = models.CharField(max_length=255, verbose_name='Статус', choices=Status.choices, default=Status.pending)

    def __str__(self):
        return f'{self.id}'

    class Meta:
        verbose_name = 'Элемент заказа'
        verbose_name_plural = 'Элементы заказа'


class Report(models.Model):
    class Status(models.TextChoices):
        pending = 'pending', 'В ожидании'
        confirmed = 'confirmed', 'Подтверждено'
        cancelled = 'cancelled', 'Отменено'
    client = models.ForeignKey('user.User', on_delete=models.CASCADE, verbose_name='Клиент')
    created = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(verbose_name='Коммент', null=True)
    status = models.CharField(max_length=255, verbose_name='Статус', choices=Status.choices, default=Status.pending)
    period = models.IntegerField(verbose_name='Период(месяц)', default=0)

    def __str__(self):
        return f'{self.id}'

    class Meta:
        verbose_name = 'Отчёт'
        verbose_name_plural = 'Отчёты'


class ReportItem(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE, verbose_name='Отчёт', related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')
    count = models.IntegerField(verbose_name='Кол-во', default=0)

    def __str__(self):
        return f'{self.id}'

    class Meta:
        verbose_name = 'Элемент отчета'
        verbose_name_plural = 'Элементы отчета'

