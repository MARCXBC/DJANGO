from rest_framework import serializers
from .models import Blog,BlogImage

class BlogImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = BlogImage
        fields = "__all__"

class BlogSerializer(serializers.ModelSerializer):

    images = BlogImageSerializer(many=True, read_only=True)

    class Meta:
        model = Blog
        fields = "__all__"  
        read_only_fields = ["author"]        


