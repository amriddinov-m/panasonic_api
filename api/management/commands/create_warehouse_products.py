from django.core.management.base import BaseCommand
from api.models import Product, WarehouseProduct

class Command(BaseCommand):
    help = 'Создать WarehouseProduct для всех продуктов с количеством 0, если еще не создано'

    def handle(self, *args, **options):
        products = Product.objects.all()
        created_count = 0
        for product in products:
            obj, created = WarehouseProduct.objects.get_or_create(
                product=product,
                defaults={'count': 100, 'warehouse_id': 1, 'price': product.price}
            )
            if created:
                created_count += 1
        self.stdout.write(self.style.SUCCESS(f'Создано новых WarehouseProduct: {created_count}'))