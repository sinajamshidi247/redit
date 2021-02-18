from django.shortcuts import render
from rest_framework import generics , permissions , mixins ,status
from .models import Post , Vote
from .serializers import PostSerializer , VoteSerializer
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import api_view
from rest_framework.response import Response



class PostList(generics.ListCreateAPIView):
    queryset=Post.objects.all()
    serializer_class = PostSerializer
    permissions_classes = [permissions.IsAuthenticatedOrReadOnly] # if not authenticated just allow to get posts not post 

    def perform_create(self, serializer):

        serializer.save(poster=self.request.user.id)


class PostDelete(generics.RetrieveDestroyAPIView):
    queryset=Post.objects.all()
    serializer_class = PostSerializer
    permissions_classes = [permissions.IsAuthenticatedOrReadOnly] # if not authenticated just allow to get posts not post 

    def delete(self,request,*args,**kwargs):
        post= Post.objects.filter(pk=kwargs['pk'],poster=self.request.user.id)
        if post.exists():
            return self.destroy(request,*args,**kwargs)
        else:
            raise ValidationError  ('this isnt your post')


class VoteCreate(generics.CreateAPIView,mixins.DestroyModelMixin):
    
    serializer_class = VoteSerializer
    permissions_classes = [permissions.IsAuthenticated] #just authenticated person can vote 
        
    def get_queryset(self):
        user = self.request.user
        post = Post.objects.get(pk=self.kwargs['pk'])
        return Vote.objects.filter(voter=user,post=post)

        
    def perform_create(self, serializer):
        if self.get_queryset().exists():
            raise ValidationError('you have already voted for this post')
        else:
            serializer.save(voter=self.request.user.id,post=Post.objects.get(pk=self.kwargs['pk']))

    def delete(self,request,*args,**kwargs):
        if self.get_queryset().exists():
            self.get_queryset().delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            raise ValidationError('you never voted for this post loser')




