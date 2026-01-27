from review_app.serializers import ListProductSerializer, ProductDetailSerializer
from django.shortcuts import get_object_or_404
from openai import OpenAI
from django.conf import settings

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from datetime import timedelta

from review_app.models import Product



# The following is a dummy API key for tutorial purposes only.
# Replace with your actual OpenAI API key.
client = openai = OpenAI(api_key="sk-test-1234567890abcdefTESTKEYnotreal9876543210")

# When you get your real API key, place the key in a .env file, access it in your settings.py, and use the line below instead:
# client = OpenAI(api_key=settings.OPENAI_API_KEY)


def summarize_reviews(product_name, reviews):
    reviews_text = "\n".join(
        [f"- {r.rating}/5: {r.comment}" for r in reviews]
    )
    # 4/5 awesome product, really loved it!   
    # 2/5 poor product, really loved it!   

    prompt_input = f"""
You are an assistant that summarizes customer reviews.

Product: {product_name}

Reviews:
{reviews_text}

Provide:
- Overall sentiment
- Common pros
- Common cons
- Short final summary
"""

    response = client.responses.create(
        model="gpt-5.1",
        input=prompt_input,
        temperature=0.4,
        max_output_tokens=600,
    )

    answer = response.output_text

    return answer




@api_view(['POST'])
def generate_reviews_summary(request, slug):
    product = get_object_or_404(Product, slug=slug)

    # 1️⃣ Enforce 7-day interval
    if product.summary_updated_at:
        next_allowed_time = product.summary_updated_at + timedelta(days=7)

        if timezone.now() < next_allowed_time:
            time_left = next_allowed_time - timezone.now()
            days_left = time_left.days + (1 if time_left.seconds > 0 else 0)

            return Response(
                {
                    "detail": "Summary was recently generated",
                    "summary": product.review_summary,
                    "days_left": days_left,
                    "next_allowed_at": next_allowed_time,
                    "generated_at": product.summary_updated_at,
                    "newly_created": False,
                },
                status=status.HTTP_200_OK
            )

    # 2️⃣ Fetch latest reviews
    reviews = product.reviews.order_by("-created_at")[:10]
    if not reviews.exists():
        return Response(
            {"error": "No reviews available."},
            status=status.HTTP_400_BAD_REQUEST
        )

    # 3️⃣ Generate new summary
    summary = summarize_reviews(product.name, reviews)

    product.review_summary = summary
    product.summary_updated_at = timezone.now()
    product.save(update_fields=["review_summary", "summary_updated_at"])

    return Response(
        {
            "product": product.name,
            "summary": summary,
            "generated_at": product.summary_updated_at,
            "days_left": 7,
            "newly_created": True,
        },
        status=status.HTTP_201_CREATED
    )


@api_view(['GET'])
def list_products(request):
    products = Product.objects.all().order_by('-id')
    serializer = ListProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    serializer = ProductDetailSerializer(product)
    return Response(serializer.data)



