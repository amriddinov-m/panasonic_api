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
    status = models.ForeignKey(Status, on_delete=models.CASCADE, verbose_name='Статус')
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
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.ForeignKey(Status, on_delete=models.CASCADE, verbose_name='Статус')
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, verbose_name='Пользователь')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория продуктов'
        verbose_name_plural = 'Категории продуктов'


class Product(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, verbose_name='Категория')
    name = models.CharField(max_length=255, verbose_name='Название')
    unit_type = models.ForeignKey('UnitType', on_delete=models.CASCADE, verbose_name='Ед. Изм')
    status = models.ForeignKey(Status, on_delete=models.CASCADE, verbose_name='Статус')
    comment = models.TextField(verbose_name='Коммент')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, verbose_name='Пользователь')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class Warehouse(models.Model):
    name = models.CharField(max_length=255, verbose_name='<UNK>')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, verbose_name='Пользователь')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Склад'
        verbose_name_plural = 'Склады'


class WarehouseProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, verbose_name='Склад')
    count = models.IntegerField(verbose_name='Кол-во')
    unit_type = models.ForeignKey('UnitType', on_delete=models.CASCADE, verbose_name='Ед. изм')
    status = models.ForeignKey(Status, on_delete=models.CASCADE, verbose_name='Статус')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, verbose_name='Пользователь')

    def __str__(self):
        return f'{self.product.name} - {self.count} {self.unit_type}'

    class Meta:
        verbose_name = 'Продукт в складе'
        verbose_name_plural = 'Продукты в складе'


class Income(models.Model):
    client = models.ForeignKey('user.User', on_delete=models.CASCADE, verbose_name='Клиент',
                               related_name='income_client')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, verbose_name='Пользователь',
                             related_name='income_user')
    comment = models.TextField(verbose_name='Коммент')
    status = models.ForeignKey(Status, on_delete=models.CASCADE, verbose_name='Статус')
    total_amount = models.IntegerField(verbose_name='Общая сумма', default=0)

    def __str__(self):
        return f'{self.id}'

    class Meta:
        verbose_name = 'Приход'
        verbose_name_plural = 'Приходы'


class IncomeItem(models.Model):
    income = models.ForeignKey(Income, on_delete=models.CASCADE, verbose_name='Приход')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')
    count = models.IntegerField(verbose_name='Кол-во')
    unit_type = models.ForeignKey('UnitType', on_delete=models.CASCADE, verbose_name='Ед. изм')
    price = models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Цена')
    comment = models.TextField(verbose_name='Коммент')
    status = models.ForeignKey(Status, on_delete=models.CASCADE, verbose_name='Статус')
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, verbose_name='Пользователь')

    def __str__(self):
        return f'{self.id}'

    class Meta:
        verbose_name = 'Элемент прихода'
        verbose_name_plural = 'Элементы прихода'


class Outcome(models.Model):
    client = models.ForeignKey('user.User', on_delete=models.CASCADE, verbose_name='Клиент',
                               related_name='outcome_client')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.ForeignKey(Status, on_delete=models.CASCADE, verbose_name='Статус')
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, verbose_name='Пользователь',
                             related_name='outcome_user')
    comment = models.TextField(verbose_name='Коммент')
    total_amount = models.IntegerField(verbose_name='Общая сумма', default=0)

    def __str__(self):
        return f'{self.id}'

    class Meta:
        verbose_name = 'Расход'
        verbose_name_plural = 'Расходы'


class OutcomeItem(models.Model):
    outcome = models.ForeignKey(Outcome, on_delete=models.CASCADE, verbose_name='Расход')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')
    count = models.IntegerField(verbose_name='Кол-во')
    unit_type = models.ForeignKey('UnitType', on_delete=models.CASCADE, verbose_name='Ед. изм')
    status = models.ForeignKey(Status, on_delete=models.CASCADE, verbose_name='Статус')
    price = models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Цена')
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, verbose_name='Пользователь')

    def __str__(self):
        return f'{self.id}'

    class Meta:
        verbose_name = 'Элемент расходы'
        verbose_name_plural = 'Элементы расхода'
