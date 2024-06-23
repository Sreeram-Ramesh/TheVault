from django.contrib import admin
from blog.models import Post , Comment , UserProfileInfo
from django.forms import Select
# Register your models here.
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(UserProfileInfo)

class UserProfileInfoAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        # 1. Get the form from the parent class:
        form = super(UserProfileInfoAdmin, self).get_form(request, obj, **kwargs)
        # 2. Change the widget:
        form.base_fields['profile_pic'].widget = Select(choices=(
            ('', 'No Image'),
            ('profile_pics/avatar_1.jpg', 'Avatar 1'),
            ('profile_pics/avatar_2.jpg', 'Avatar 2'),
            ('profile_pics/avatar_3.jpg', 'Avatar 3'),
            ('profile_pics/avatar_4.jpg', 'Avatar 4')
        ))

        # 3. Return the form!
        return form
