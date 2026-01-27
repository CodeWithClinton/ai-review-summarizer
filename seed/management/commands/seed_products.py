
from django.core.management.base import BaseCommand
from django.utils.text import slugify
import random
from review_app.models import Product, Review


class Command(BaseCommand):
    help = "Seed database with 10 products and realistic reviews"

    def handle(self, *args, **kwargs):
        products_data = [
            {
                "name": "Wireless Bluetooth Headphones",
                "description": "Premium over-ear wireless headphones designed for immersive sound, deep bass, and all-day comfort. Ideal for work calls, music, and commuting.",
                "image_url": "https://images.unsplash.com/photo-1518443886634-0c17b9cbe65d",
                "price": 89.99,
                "reviews": [
                    "The sound quality is rich and well balanced with deep bass and clear vocals. I use these daily for work calls and music, and the battery easily lasts multiple days.",
                    "Very comfortable even during long listening sessions. Pairing was instant and the connection is stable throughout the day.",
                    "Excellent value for money. The build quality feels premium and the noise isolation is impressive for the price.",
                    "Great headphones for commuting. They block out most background noise and calls sound very natural.",
                    "Battery life exceeded my expectations and charging is fast. I would easily recommend this to others."
                ]
            },
            {
                "name": "Smart Fitness Watch",
                "description": "A sleek fitness smartwatch with heart rate tracking, step counting, sleep analysis, and workout monitoring to help you stay healthy and active.",
                "image_url": "https://images.unsplash.com/photo-1517433456452-f9633a875f6f",
                "price": 129.50,
                "reviews": [
                    "This watch keeps me motivated to stay active. Step tracking, heart rate monitoring, and sleep data are all very useful.",
                    "Lightweight and comfortable for daily wear. The screen is bright and easy to read outdoors.",
                    "Battery lasts several days and syncing with my phone is smooth and reliable.",
                    "Great fitness features at this price point. The app is intuitive and easy to navigate.",
                    "I love how accurate the workout tracking is. It has become part of my daily routine."
                ]
            },
            {
                "name": "Mechanical Gaming Keyboard",
                "description": "High-performance mechanical keyboard built for gamers and professionals who value speed, durability, and tactile feedback.",
                "image_url": "https://images.unsplash.com/photo-1517336714731-489689fd1ca8",
                "price": 74.00,
                "reviews": [
                    "Typing feels incredibly satisfying with these switches. Great for both work and gaming.",
                    "Solid build quality and responsive keys. It improved my typing speed noticeably.",
                    "Perfect keyboard for long gaming sessions. The keys feel durable and consistent.",
                    "The tactile feedback is excellent, though it can be loud in quiet environments.",
                    "Fantastic value mechanical keyboard with premium feel."
                ]
            },
            {
                "name": "4K Ultra HD Monitor",
                "description": "A stunning 4K monitor offering crisp visuals, vibrant colors, and a large screen size for productivity, gaming, and creative work.",
                "image_url": "https://images.unsplash.com/photo-1527443224154-c4a3942d3acf",
                "price": 399.99,
                "reviews": [
                    "The display is incredibly sharp and vibrant. Perfect for productivity and media consumption.",
                    "Color accuracy is excellent and the screen size makes multitasking easier.",
                    "Watching movies and editing photos feels immersive on this monitor.",
                    "High quality panel with great brightness. Setup was quick and easy.",
                    "Worth every penny if you value screen clarity and detail."
                ]
            },
            {
                "name": "Noise Cancelling Earbuds",
                "description": "Compact wireless earbuds with active noise cancellation, clear sound, and a comfortable fit for daily use and workouts.",
                "image_url": "https://images.unsplash.com/photo-1590658268037-6bf12165a8df",
                "price": 59.99,
                "reviews": [
                    "Noise cancellation works surprisingly well and the sound quality is clear.",
                    "Very comfortable fit and great for workouts and commuting.",
                    "Battery life is solid and the charging case feels durable.",
                    "Easy to pair and stable connection throughout use.",
                    "Excellent earbuds considering the price."
                ]
            },
            {
                "name": "Portable Power Bank 20000mAh",
                "description": "High-capacity portable power bank designed to keep your devices charged on the go, perfect for travel and emergencies.",
                "image_url": "https://images.unsplash.com/photo-1609091839311-d5365f9ff1c5",
                "price": 45.25,
                "reviews": [
                    "This power bank is extremely reliable during travel. It charges my phone multiple times on a single charge.",
                    "Fast charging and solid build quality. Slightly heavy but expected for the capacity.",
                    "Perfect for long trips and emergencies. Never failed me so far.",
                    "Very dependable and holds charge for a long time.",
                    "Excellent power bank for everyday use."
                ]
            },
            {
                "name": "DSLR Camera Backpack",
                "description": "Durable and well-padded camera backpack designed to safely carry DSLR cameras, lenses, and accessories.",
                "image_url": "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee",
                "price": 68.90,
                "reviews": [
                    "The padding is excellent and keeps my camera gear well protected.",
                    "Comfortable to wear even with heavy equipment.",
                    "Lots of compartments and very well organized.",
                    "Feels durable and perfect for outdoor photography.",
                    "Great backpack for professional and hobby photographers."
                ]
            },
            {
                "name": "Ergonomic Office Chair",
                "description": "Ergonomically designed office chair with lumbar support and adjustable features to improve posture and comfort during long work hours.",
                "image_url": "https://images.unsplash.com/photo-1586023492125-27b2c045efd7",
                "price": 249.99,
                "reviews": [
                    "This chair greatly improved my posture and comfort during long work hours.",
                    "Excellent lumbar support and cushioning.",
                    "Very sturdy and easy to assemble.",
                    "Comfortable for all-day sitting without back pain.",
                    "Worth every cent for remote workers."
                ]
            },
            {
                "name": "USB-C Hub Adapter",
                "description": "A compact USB-C hub that expands your laptop connectivity with multiple ports including HDMI, USB, and card readers.",
                "image_url": "https://images.unsplash.com/photo-1587825140708-dfaf72ae4b04",
                "price": 34.75,
                "reviews": [
                    "Works flawlessly with my laptop and connects all my devices.",
                    "Compact design and very convenient for travel.",
                    "Good selection of ports and stable performance.",
                    "Plug and play with no setup required.",
                    "Reliable hub for everyday use."
                ]
            },
            {
                "name": "Smart Home Wi-Fi Router",
                "description": "High-speed smart Wi-Fi router designed to provide strong, stable internet coverage for modern smart homes and multiple devices.",
                "image_url": "https://images.unsplash.com/photo-1603791440384-56cd371ee9a7",
                "price": 179.00,
                "reviews": [
                    "Wi-Fi coverage improved significantly across my home.",
                    "Fast speeds and very stable connection.",
                    "Easy setup and user-friendly interface.",
                    "Handles multiple devices without issues.",
                    "Excellent router for modern smart homes."
                ]
            }
        ]

        authors = [
            "Daniel A.", "Grace T.", "Michael O.", "Sarah K.", "John P.",
            "Amaka R.", "Samuel I.", "Blessing N.", "Victor L.", "Peace D."
        ]

        for product_data in products_data:
            product, created = Product.objects.get_or_create(
                name=product_data["name"],
                defaults={
                    "description": product_data["description"],
                    "image_url": product_data["image_url"],
                    "price": product_data["price"],
                    "slug": slugify(product_data["name"])
                }
            )

            if not created:
                continue

            negative_reviews = [
                "I was honestly disappointed with this product. It did not perform as well as I expected and some features felt poorly implemented.",
                "The idea is good but execution is lacking. I ran into issues during regular use and it did not feel worth the price.",
            ]

            neutral_reviews = [
                "This product is average. It works, but there are noticeable drawbacks that prevent it from being great.",
            ]

            positive_reviews = product_data["reviews"]

            all_reviews = (
                [(text, random.randint(4, 5)) for text in positive_reviews] +
                [(text, random.randint(1, 2)) for text in negative_reviews] +
                [(text, 3) for text in neutral_reviews]
            )

            random.shuffle(all_reviews)

            for review_text, rating in all_reviews[:5]:
                Review.objects.create(
                    product=product,
                    rating=rating,
                    comment=review_text,
                    author=random.choice(authors)
                )

            self.stdout.write(self.style.SUCCESS(f"Seeded {product.name}"))

        self.stdout.write(self.style.SUCCESS("🎉 10 products with descriptions, images, and reviews successfully seeded"))
