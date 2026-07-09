from django.shortcuts import render
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

import cloudinary.uploader
from .models import Blog,BlogImage
from .serializers import BlogSerializer

class CreateBlogView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = BlogSerializer(data=request.data)

        if serializer.is_valid():
           blog= serializer.save(author=request.user)
           images = request.FILES.getlist("images")
           for image in images:
                result= cloudinary.uploader.upload(image)

                BlogImage.objects.create(
                    blog=blog,
                    image=image["secure_url"],
                    )
                return Response({"message": "Blog created successfully"}, status=201)
           return Response(serializer.errors, status=400)  

class BlogListView(APIView):

    def get(self, request):
        search=request.GET.get("search");

        blogs = Blog.objects.all().order_by("-created_at")
        if search:
            blogs = blogs.filter(
                Q(title__icontains=search)  |
                Q(content__icontains=search)
            )

        serializer = BlogSerializer(blogs, many=True)

        return Response(serializer.data, status=200)



class BlogDetailView(APIView):
    def get(self,request, id):
        try:
            blogs=Blog.objects.get(id=id)
            serializer=BlogSerializer(blogs)
            return Response(serializer.data,status=200)
        except Blog.DoesNotExist:
            return Response({"message":"Blog not found"},status=404)
        
class UpdateBlogView(APIView):
    permission_classes=[IsAuthenticated]
    def path(self,request,id):

        try:
            blog=Blog.objects.get(id=id)
            if blog.author!=request.user:
                return Response({"message": "You can only edit your own blog"},status=403)
            serializer=BlogSerializer(
                instance=blog,
                data=request.data,
                partial=True
            )

            if serializer.is_valid():
                serializer.save()

                return Response({"message":"Blog Updated"},status=200)
            return Response(serializer.errors,status=400)
        except Blog.DoesNotExist:
            return Response({"message":"Blog not found"},status=404)
        


class DeleteBlogView(APIView):
    permission_classes=[IsAuthenticated]
    def delete(self,request,id):
        try:
            blog=Blog.objects.get(id=id)
            if(blog.author !=request.user and not request.user.is_staff):
                blog.delete()
                return Response({"message":"Blog Deleted"})
        except Blog.DoesNotExist:

            return Response({"message":"Blog not found"},status=404)
        
class MyBlogView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        blogs = Blog.objects.filter(author=request.user)  # Added 's' to objects and blog
        serializer = BlogSerializer(blogs, many=True)     # Plural variables match
        return Response(serializer.data)


            
        

