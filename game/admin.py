from django.contrib import admin
from .models import BackgroundAsset, PlayerPost

# 👑 Registering the models exposes them to the Django admin panel interface
@admin.register(BackgroundAsset)
class BackgroundAssetAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_at')
    search_fields = ('title',)

@admin.register(PlayerPost)
class PlayerPostAdmin(admin.ModelAdmin):
    list_display = ('player', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('player__username', 'message')