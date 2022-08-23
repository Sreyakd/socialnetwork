from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from socialapp.models import UserProfile,Posts,Comments
from socialapp.serializer import UserSerializer,UserProfileSerializer,PostSerializer,CommentSerializer
from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework.decorators import action


class UserRegistrationView(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

class UserProfileView(ModelViewSet):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    def create(self,request,*args,**kwargs):
        serializer = UserProfileSerializer(data=request.data,context={"user":request.user})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

    @action(methods=["post"], detail=True)
    def add_following(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        user=User.objects.get(id=id)
        profile=UserProfile.objects.get(user=request.user)
        profile.following.add(user)
        return Response({"msg":"ok"})

    @action(methods=["get"],detail=False)
    def my_following(self,request,*args,**kwargs):
        user=request.user
        user_profile=UserProfile.objects.get(user=user)
        followings=user_profile.following.all()
        serializer=UserSerializer(followings,many=True)
        return Response(data=serializer.data)

    # @action(methods=["get"], detail=True)
    # def get_following(self, request, *args, **kwargs):
    #     id = kwargs.get("pk")
    #     user = User.objects.get(id=id)
    #     follows = user.UserProfile.all()
    #     serializer = UserProfileSerializer(follows,many=True)
    #     return Response(serializer.data)

class PostView(ModelViewSet):
    serializer_class = PostSerializer
    queryset = Posts.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self,serializer):
        serializer.save(author=self.request.user)

    @action(methods=["post"],detail=True)
    def add_comment(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        post=Posts.objects.get(id=id)
        user=request.user
        serializer=CommentSerializer(data=request.data,context={"post":post,"user":user})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

    @action(methods=["get"], detail=True)
    def get_comments(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        post=Posts.objects.get(id=id)
        comment=post.Comments_set.all()
        serializer=CommentSerializer(comment,many=True)
        return Response(serializer.data)

    @action(methods=["post"], detail=True)
    def add_like(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        post=Posts.objects.get(id=id)
        post.liked_by.add(request.user)
        return Response({"msg":"ok"})






