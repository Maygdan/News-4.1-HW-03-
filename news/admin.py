from django.contrib import admin
from .models import *
from modeltranslation.admin import TranslationAdmin

admin.site.register(Author)

admin.site.register(Comment)
admin.site.register(Post_Category)
class CategoryAdmin(TranslationAdmin):
    model = Category
 
 
class PostAdmin(TranslationAdmin):
    model = Post
 
 
admin.site.register(Post)
admin.site.register(Category)
