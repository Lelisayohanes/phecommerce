from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Product, ProductImage, Category
from .serializers import ProductSerializer, ProductImageSerializer,CategorySerializer
import logging

logger = logging.getLogger(__name__)

class ProductViewSet(viewsets.ModelViewSet):  # Changed from APIView to ModelViewSet
    queryset = Product.objects.all()  # Added queryset
    serializer_class = ProductSerializer

    def create(self, request, *args, **kwargs):
        product_data = {
            'name': request.data.get('name'),
            'description': request.data.get('description'),
            'price': request.data.get('price'),
            'discount': request.data.get('discount'),
            'category': request.data.get('category'),  # Get the category ID

        }
        
        product_serializer = self.get_serializer(data=product_data)
        if product_serializer.is_valid():
            product = product_serializer.save()

            # Process image uploads
            image_types = request.data.getlist('image_type')
            images = request.FILES.getlist('images')
            for i in range(len(images)):
                if i < len(image_types):  # Ensure there's a corresponding type
                    image = ProductImage(product=product, image_url=images[i], image_type=image_types[i])
                    image.save()

            return Response(product_serializer.data, status=status.HTTP_201_CREATED)
        return Response(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductImageViewSet(viewsets.ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer