from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Main Campaign Dashboard
    path('', views.campaign_dashboard, name='dashboard'),
    
    # DM Review Panel Routing Hub
    path('review/', views.dm_review_panel, name='dm_review_panel'),
    path('review/action/<int:post_id>/<str:decision>/', views.approve_merge_action, name='approve_merge'),
    
    # 🗑️ DM Data Purge Endpoints (New Deletion Routes)
    path('delete-asset/<int:asset_id>/', views.delete_background_asset, name='delete_background_asset'),
    path('delete-post/<int:post_id>/', views.delete_player_post, name='delete_player_post'),
    
    # 🔴 Real-Time API Endpoints
    path('api/live-feed/', views.api_live_feed, name='api_live_feed'),
    path('api/pending-queue/', views.api_pending_queue, name='api_pending_queue'),
    path('api/active-map/', views.api_active_map, name='api_active_map'),
    
    # Explicitly Named Authentication Endpoints
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    
    # Password Reset Flow
    path('password-reset/', 
         auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'),
         name='password_reset'),
    path('password-reset/done/', 
         auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/', 
         auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
         name='password_reset_complete'),
    
    # Password Change (for logged-in users)
    path('password-change/', 
         auth_views.PasswordChangeView.as_view(template_name='registration/password_change_form.html', success_url='/password-change/done/'),
         name='password_change'),
    path('password-change/done/', 
         auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'),
         name='password_change_done'),
]
