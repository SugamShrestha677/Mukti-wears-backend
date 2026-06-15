from django.core.management.base import BaseCommand
from products.models import Product


PRODUCTS = [
    {
        "name": "Patan Canvas Hoodie",
        "slug": "patan-canvas-hoodie",
        "price": 145.00,
        "category": "men",
        "series": "Heritage Series",
        "image": "https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=800&q=80",
        "sizes": ["XS", "S", "M", "L", "XL"],
        "colours": ["Bone", "Ink"],
        "description": "Heavyweight 500gsm loop-back cotton with woven Newari geometric panels at the sleeves. Boxed silhouette, dropped shoulder.",
        "story": "Inspired by the lattice work of Patan's hidden courtyards — geometry that has weathered a thousand monsoons.",
        "care": "Wash cold, inside out. Hang dry. Do not bleach.",
        "stock": 25,
    },
    {
        "name": "Loomed Artisan Shell",
        "slug": "loomed-artisan-shell",
        "price": 180.00,
        "category": "men",
        "series": "Heritage Series",
        "image": "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=800&q=80",
        "sizes": ["XS", "S", "M", "L", "XL"],
        "colours": ["Sand", "Stone"],
        "description": "Hand-loomed Nepali cotton coach jacket with discreet peacock-feather embroidery at the chest. Lined, full-zip.",
        "story": "Cut and stitched in a small atelier in Bhaktapur. Each shell carries the maker's mark.",
        "care": "Dry clean preferred. Do not iron embroidery.",
        "stock": 15,
    },
    {
        "name": "Scripted Heritage Tee",
        "slug": "scripted-heritage-tee",
        "price": 75.00,
        "category": "men",
        "series": "Core",
        "image": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=800&q=80",
        "sizes": ["XS", "S", "M", "L", "XL"],
        "colours": ["Ink"],
        "description": "Heavyweight cotton tee with hand-stitched Ranjana-script pocket. Garment-washed for vintage hand.",
        "story": 'The pocket script is a Ranjana benediction — "may the road remember you."',
        "care": "Wash cold, tumble low.",
        "stock": 40,
    },
    {
        "name": "Dhaka Cargo Trousers",
        "slug": "dhaka-cargo-trousers",
        "price": 120.00,
        "category": "men",
        "series": "Heritage Series",
        "image": "https://images.unsplash.com/photo-1624378439575-d8705ad7ae80?w=800&q=80",
        "sizes": ["XS", "S", "M", "L", "XL"],
        "colours": ["Stone", "Ink"],
        "description": "Relaxed cargo cut with hand-loomed Dhaka fabric pocket inserts. Concealed elastic waist, ankle drawcord.",
        "story": "Dhaka cloth has clothed Nepali royalty and farmers alike. Here it lives on streetwear.",
        "care": "Wash cold. Reshape while damp.",
        "stock": 30,
    },
    {
        "name": "Peacock Window Scarf",
        "slug": "peacock-window-scarf",
        "price": 95.00,
        "category": "accessories",
        "series": "Atelier",
        "image": "https://images.unsplash.com/photo-1601924994987-69e26d50dc26?w=800&q=80",
        "sizes": ["One Size"],
        "colours": ["Cream"],
        "description": "Brushed wool scarf with hand-embroidered peacock-window motif. Fringed ends, generous drape.",
        "story": "After the Pujari Math window in Bhaktapur — carved in the 15th century, still standing.",
        "care": "Dry clean only.",
        "stock": 20,
    },
    {
        "name": "Indigo Weave Bucket Hat",
        "slug": "indigo-weave-bucket",
        "price": 65.00,
        "category": "accessories",
        "series": "Core",
        "image": "https://images.unsplash.com/photo-1588850561407-ed78c334e67a?w=800&q=80",
        "sizes": ["One Size"],
        "colours": ["Indigo"],
        "description": "Garment-dyed cotton bucket with woven Nepali band at the brim. Soft crown, unstructured.",
        "story": "Indigo dye vats still bubble in the alleys of Asan. We carry that pigment forward.",
        "care": "Spot clean. Air dry.",
        "stock": 35,
    },
]


class Command(BaseCommand):
    help = "Seed the database with Nepal-inspired products (idempotent)"

    def handle(self, *args, **options):
        created_count = 0
        for data in PRODUCTS:
            _, created = Product.objects.update_or_create(
                slug=data["slug"],
                defaults=data,
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f"  Created: {data['name']}"))
            else:
                self.stdout.write(f"  Updated: {data['name']}")

        self.stdout.write(
            self.style.SUCCESS(
                f"\nDone. {created_count} new, {len(PRODUCTS) - created_count} updated."
            )
        )
