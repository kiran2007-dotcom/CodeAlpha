from django.core.management.base import BaseCommand
from django.utils.text import slugify
from store.models import Product

SAMPLE_PRODUCTS = [
    ("Studio Wireless Headphones", "Comfortable over-ear headphones with clear sound and long battery life.", "2499.00", 18, "https://images.unsplash.com/photo-1509966756634-9c23dd6e6815"),
    ("Everyday Backpack", "A durable everyday backpack with a padded laptop compartment.", "1899.00", 24, "https://images.unsplash.com/photo-1553062407-98eeb64c6a62"),
    ("Minimal Desk Lamp", "A clean desk lamp designed for focused work and warm ambient light.", "1299.00", 12, "https://images.unsplash.com/photo-1507473885765-e6ed057f782c"),
    ("Classic Wrist Watch", "A versatile everyday watch with a minimal dial and comfortable strap.", "3299.00", 9, "https://images.unsplash.com/photo-1523275335684-37898b6baf30"),
    ("Ceramic Coffee Mug", "A simple ceramic mug for your daily coffee or tea.", "399.00", 40, "https://images.unsplash.com/photo-1514228742587-6b1558fcca3d"),
    ("Running Sneakers", "Lightweight sneakers built for daily walks and active days.", "2799.00", 15, "https://images.unsplash.com/photo-1542291026-7eec264c27ff"),
]

class Command(BaseCommand):
    help = "Create sample products for the store"

    def handle(self, *args, **options):
        for name, description, price, stock, image_url in SAMPLE_PRODUCTS:
            slug = slugify(name)
            Product.objects.update_or_create(
                slug=slug,
                defaults={"name": name, "description": description, "price": price,
                          "stock": stock, "image_url": image_url, "is_active": True},
            )
        self.stdout.write(self.style.SUCCESS("Sample products are ready."))
