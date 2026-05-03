from django.core.management.base import BaseCommand

from core.models import (
    Brand,
    Category,
    Product,
    Size,
    User,
)


class Command(BaseCommand):
    help = "Тестовые пользователи, справочники, товары."

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Очистить данные приложения core перед заполнением",
        )

    def handle(self, *args, **options):
        if options["clear"]:
            Product.objects.all().delete()
            User.objects.all().delete()
            Category.objects.all().delete()
            Brand.objects.all().delete()
            Size.objects.all().delete()

        categories = [
            Category.objects.get_or_create(name=n)[0]
            for n in ("Футболки", "Джинсы", "Обувь", "Куртки", "Аксессуары")
        ]
        brands = [
            Brand.objects.get_or_create(name=n)[0]
            for n in ("Nike", "Adidas", "Zara", "Uniqlo", "Reserved")
        ]
        sizes = [
            Size.objects.get_or_create(name=n)[0]
            for n in ("XS", "S", "M", "L", "XL", "42")
        ]

        for name, email, password in (
            ("Анна Иванова", "anna@test.local", "test123"),
            ("Пётр Сидоров", "petr@test.local", "test123"),
            ("Мария Козлова", "maria@test.local", "test123"),
        ):
            User.objects.get_or_create(
                email=email,
                defaults={"name": name, "password": password},
            )

        # размер idx | категория idx | индекс одного бренда (FK)
        specs = [
            ("Базовая футболка белая", "Хлопок 100%.", 1299.0, 2, 0, 0),
            ("Джинсы slim fit", "Деним с эластикой.", 3490.0, 3, 1, 1),
            ("Кроссовки running", "Лёгкая подошва.", 5990.0, 5, 2, 2),
            ("Куртка ветрозащитная", "Водоотталкивающая.", 7490.0, 4, 3, 3),
            ("Рюкзак городской", 'Под ноутбук 15".', 2190.0, 2, 4, 4),
            ("Худи оверсайз", "Флис.", 4590.0, 4, 0, 0),
            ("Кеды canvas", "Классика.", 1990.0, 5, 2, 1),
            ("Поло трикотажное", "Офис/выходные.", 2490.0, 2, 0, 2),
        ]

        for name, desc, price, zi, ci, bi in specs:
            Product.objects.update_or_create(
                name=name,
                defaults={
                    "description": desc,
                    "price": price,
                    "brand": brands[bi],
                    "size": sizes[zi],
                    "category": categories[ci],
                },
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"Ок: товаров {Product.objects.count()}, брендов {Brand.objects.count()}."
            )
        )
