from django.contrib.auth.models import User
from django.db.models import Q
from itertools import chain
from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib import messages
from blog.models import Post , Comment , UserProfileInfo
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from blog.forms import PostForm , CommentForm , UserUpdateForm , UserForm , UserProfileInfoForm
from django.urls import reverse_lazy , reverse
from django.views.generic import (TemplateView,ListView,
                                   DetailView,CreateView,
                                   UpdateView,DeleteView)

# Create your views here.

class AboutView(TemplateView):
    template_name = 'blog/about.html'

class UserProfileView(DetailView):
    model = User
    template_name = 'blog/User_Profile.html'

    def get_context_data(self,*args,**kwargs):
        request = self.request
        context = super().get_context_data(*args, **kwargs)
        context['u_form'] = UserUpdateForm(instance=request.user)
        context['p_form'] = UserProfileInfoForm(instance=request.user.userprofileinfo)
        context['post_list'] = Post.objects.all().order_by('-published_date')
        return context

    def post(self, request, *args, **kwargs):
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = UserProfileInfoForm(request.POST, instance=request.user.userprofileinfo)
        pk = request.user.pk
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request,'Profile details update successful !')
            return redirect(reverse('profile',kwargs={'pk':pk}))

class HomeView(ListView):
    model = Post
    template_name='blog/post_list.html'
    context_object_name = 'post_list'
    paginate_by = 20
    count = 0

    def get_context_data(self,*args,**kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['count'] = self.count or 0
        context['query'] = self.request.GET.get('q')
        return context

    def get_queryset(self):
        request = self.request
        query = request.GET.get('q', None)

        if query is not None:
            blog_results        = Post.objects.search(query)


            # combine querysets
            queryset_chain = chain(
                    blog_results,
            )
            qs = sorted(queryset_chain,
                        key=lambda instance: instance.pk,
                        reverse=True)
            self.count = len(qs) # since qs is actually a list
            return qs
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')


class PostDetailView(DetailView):
    model = Post

    def like_check(self):
        request = self.request
        is_liked = False
        post = get_object_or_404(Post,pk=self.kwargs['pk'])

        if post.likes.filter(pk=request.user.pk).exists():
            is_liked = True
        return is_liked

    def get_context_data(self,*args,**kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['is_liked'] = self.like_check
        return context

class CreatePostView(CreateView,LoginRequiredMixin):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post

class UpdatePostView(UpdateView,LoginRequiredMixin):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post

class PostDeleteView(DeleteView,LoginRequiredMixin):
    model = Post
    success_url = reverse_lazy('home')

class DraftPostView(ListView,LoginRequiredMixin):
    login_url = '/login/'
    redirect_field_name = 'blog/post_draft_list.html'
    model = Post


    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('create_date')

def register(request):

    registered = False
    register_form = UserForm()
    profile_form = UserProfileInfoForm()

    if request.method == 'POST':
        register_form = UserForm(request.POST)
        profile_form = UserProfileInfoForm(request.POST)

        if register_form.is_valid() and profile_form.is_valid():
            user = register_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()
            registered = True
            html = "<html><head><!-- Latest compiled and minified CSS --><link rel='stylesheet' href='https://stackpath.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css' integrity='sha384-HSMxcRTRxnN+Bdg0JdbxYKrThecOKuH5zCYotlSAcp1+c8xmyTe9GYg1l9a69psu' crossorigin='anonymous'><!-- Optional theme --><link rel='stylesheet' href='https://stackpath.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap-theme.min.css' integrity='sha384-6pzBo3FDv/PJ8r2KRkGHifhEocL+1X2rVCTTkUfGk7/0pbek5mMa1upzvWbrUbOZ' crossorigin='anonymous'><link href='https://fonts.googleapis.com/css2?family=Permanent+Marker&display=swap' rel='stylesheet'><link href='https://fonts.googleapis.com/css2?family=Do+Hyeon&display=swap' rel='stylesheet'></head><body style='background-color: #88d6f2;'><center><h1>THANK YOU!</h1></center><center><h3>Your account has been successfully <strong>created!</strong></center></h3><center><br><center><span class='glyphicon glyphicon-ok-circle' style='font-size:8em;color:green'><span><br><a class='btn btn-primary btn-lg' href='/accounts/login/'>LOGIN</a></body><html>"
            return  HttpResponse(html)

        else:
            print(register_form.errors,profile_form.errors)

    return render(request,'registration/registration.html',{'register_form':register_form,
                                                    'profile_form':profile_form,
                                                    'registered':registered})

@login_required
def add_comment_to_post(request,pk):
    post = get_object_or_404(Post,pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.posted_by = request.user
            comment.post = post
            comment.save()
            return redirect('post_detail',pk=post.pk)

    else:
        form = CommentForm()
    return render(request,'blog/comment_form.html',{'form':form})

@login_required
def comment_disapprove(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    comment.disapprove()
    return redirect('post_detail',pk=comment.post.pk)

@login_required
def comment_remove(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail',pk=post_pk)

@login_required
def post_publish(request,pk):
    post = get_object_or_404(Post,pk=pk)
    post.posted_by = request.user
    post.publish()
    return redirect('post_detail',pk=pk)

@login_required
def like_post(request,pk):
    post = get_object_or_404(Post , pk=pk)
    is_liked = False
    if post.likes.filter(pk=request.user.pk).exists():
        post.likes.remove(request.user)
        is_liked = False
    else:
        post.likes.add(request.user)
        is_liked = True
    return redirect('post_detail', pk=pk)
