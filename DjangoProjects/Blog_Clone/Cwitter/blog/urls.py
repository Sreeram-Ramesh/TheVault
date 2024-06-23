from django.conf.urls import url
from blog import views

urlpatterns = [
    url(r"^$",views.HomeView.as_view(),name='home'),
    url(r"^about/$",views.AboutView.as_view(),name='about'),
    url(r"^post/(?P<pk>\d+)$",views.PostDetailView.as_view(),name='post_detail'),
    url(r"^post/new/$",views.CreatePostView.as_view(),name='new_post'),
    url(r"^post/(?P<pk>\d+)/update/$",views.UpdatePostView.as_view(),name='update_post'),
    url(r"^post/(?P<pk>\d+)/delete/$",views.PostDeleteView.as_view(),name='delete_post'),
    url(r"^post/drafts/$",views.DraftPostView.as_view(),name='drafts'),
    url(r"^post/(?P<pk>\d+)/comment/$",views.add_comment_to_post,name='create_comment'),
    url(r"^post/(?P<pk>\d+)/disapprove/$",views.comment_disapprove,name='disapprove_comment'),
    url(r"^post/(?P<pk>\d+)/remove/$",views.comment_remove,name='remove_comment'),
    url(r"^post/(?P<pk>\d+)/publish/$",views.post_publish,name='publish_post'),
    url(r"^register/$",views.register,name='register'),
    url(r"^profile/(?P<pk>\d+)/$",views.UserProfileView.as_view(),name='profile'),
    url(r"^post/(?P<pk>\d+)/like/$",views.like_post,name='like_post'),
]
