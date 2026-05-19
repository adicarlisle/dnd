from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
from .models import BackgroundAsset, PlayerPost

@login_required
def campaign_dashboard(request):
    # 1. Gather all approved logs & token layers to render on the template canvas
    live_feed = PlayerPost.objects.filter(status='APPROVED').order_by('-created_at')
    backgrounds = BackgroundAsset.objects.all()
    
    # 2. Track down which map layer is explicitly active for the table sessions
    active_background = BackgroundAsset.objects.filter(
        playerpost__status='APPROVED', 
        playerpost__character_token__isnull=True
    ).last()
    
    # Default fallback to the first asset if the DM hasn't pushed a shift alert post yet
    if not active_background and backgrounds.exists():
        active_background = backgrounds.first()

    # Initialize an empty registration form shell context if the user is a DM
    user_form = UserCreationForm() if request.user.is_superuser else None

    # 3. Process Actions when a form is submitted
    if request.method == "POST":
        
        # 🧙‍♂️ SUBMISSION AA: DM Manual Player Registration Control
        if "create_player_account" in request.POST:
            if not request.user.is_superuser:
                return redirect('dashboard')
            
            user_form = UserCreationForm(request.POST)
            if user_form.is_valid():
                new_user = user_form.save()
                messages.success(request, f"Player account '{new_user.username}' created successfully!")
                return redirect('dashboard')
            else:
                messages.error(request, "Failed to create player account. Please fix the form formatting constraints.")

        # 🎨 SUBMISSION A-ALT: DM New Map Asset Upload Modal Form
        elif request.POST.get('action_type') == 'upload_asset':
            if not request.user.is_superuser:
                return redirect('dashboard')
                
            map_name = request.POST.get('map_name')
            map_file = request.FILES.get('map_file')
            
            if map_name and map_file:
                # Use .title here to align with your existing BackgroundAsset database structure
                new_asset = BackgroundAsset.objects.create(title=map_name, image=map_file)
                
                # Log the creation safely inside your central Approved Campaign Actions column
                PlayerPost.objects.create(
                    player=request.user,
                    message=f"added a new map layout option: '{map_name}' to the DM storage vault.",
                    status='APPROVED'
                )
                messages.success(request, f"Successfully uploaded '{map_name}' to the campaign vault!")
            return redirect('dashboard')

        # 👑 SUBMISSION A: DM Map Control Update Event (From Dropdown Select)
        elif "dm_map_control" in request.POST or "active_map_id" in request.POST:
            if not request.user.is_superuser:
                return redirect('dashboard')
                
            bg_id = request.POST.get('active_map') or request.POST.get('active_map_id')
            if bg_id:
                try:
                    selected_bg = BackgroundAsset.objects.get(id=bg_id)
                    
                    # Target .title here as well to fix the crash on line 77!
                    PlayerPost.objects.create(
                        player=request.user,
                        message=f"updated active battlefield scene to: '{selected_bg.title}'",
                        selected_background=selected_bg,
                        status='APPROVED'
                    )
                    messages.success(request, f"Tabletop canvas transitioned to {selected_bg.title}!")
                except BackgroundAsset.DoesNotExist:
                    pass
            return redirect('dashboard')

        # 🧝 SUBMISSION B: Normal Player Character Token/Action Post
        else:
            message_text = request.POST.get('message')
            uploaded_token = request.FILES.get('token_image') or request.FILES.get('map_file')
            
            # Send standard player inputs right down the path to your DM review vault
            PlayerPost.objects.create(
                player=request.user,
                message=message_text,
                character_token=uploaded_token,
                selected_background=active_background,
                status='PENDING'
            )
            messages.success(request, "Your action placement has been submitted to the DM review queue!")
            return redirect('dashboard')

    context = {
        'live_feed': live_feed,
        'backgrounds': backgrounds,
        'active_background': active_background,
        'user_form': user_form,
    }
    return render(request, 'index.html', context)


# 👑 THE DM REVIEW ENDPOINTS
@login_required
def dm_review_panel(request):
    if not request.user.is_superuser:
        return redirect('dashboard')
        
    pending_submissions = PlayerPost.objects.filter(status='PENDING').order_by('created_at')
    return render(request, 'dm_review.html', {'pending_submissions': pending_submissions})


@login_required
def approve_merge_action(request, post_id, decision):
    if not request.user.is_superuser:
        return redirect('dashboard')
        
    submission = get_object_or_404(PlayerPost, id=post_id)
    
    if decision == 'approve':
        submission.status = 'APPROVED'
        submission.save()
        messages.success(request, f"Successfully merged asset layer into the master canvas!")
    elif decision == 'reject':
        submission.status = 'REJECTED'
        submission.save()
        
    return redirect('dm_review_panel')


@login_required
def delete_background_asset(request, asset_id):
    if not request.user.is_superuser:
        return redirect('dashboard')
        
    asset = get_object_or_404(BackgroundAsset, id=asset_id)
    name = asset.title
    
    asset.delete()
    messages.success(request, f"Successfully purged map scene: '{name}'")
    return redirect('dashboard')



@login_required
def delete_player_post(request, post_id):
    if not request.user.is_superuser:
        return redirect('dashboard')
        
    post = get_object_or_404(PlayerPost, id=post_id)
    player_name = post.display_name # Uses your polished QoL display property!
    
    post.delete()
    messages.success(request, f"Removed action layer submitted by {player_name}.")
    return redirect('dashboard')


# 🔴 REAL-TIME API ENDPOINTS FOR SUPABASE INTEGRATION
@login_required
def api_live_feed(request):
    """API endpoint to fetch approved actions for live feed"""
    live_feed = PlayerPost.objects.filter(status='APPROVED').order_by('-created_at')[:50]
    
    data = [{
        'id': post.id,
        'display_name': post.display_name,
        'message': post.message,
        'created_at': post.created_at.isoformat(),
        'character_token': post.character_token.url if post.character_token else None,
    } for post in live_feed]
    
    return JsonResponse({'feed': data})


@login_required
def api_pending_queue(request):
    """API endpoint to fetch pending DM review submissions"""
    if not request.user.is_superuser:
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    pending = PlayerPost.objects.filter(status='PENDING').order_by('created_at')
    
    data = [{
        'id': post.id,
        'display_name': post.display_name,
        'message': post.message,
        'created_at': post.created_at.isoformat(),
        'character_token': post.character_token.url if post.character_token else None,
    } for post in pending]
    
    return JsonResponse({'queue': data, 'count': len(data)})


@login_required
def api_active_map(request):
    """API endpoint to get current active map"""
    active_background = BackgroundAsset.objects.filter(
        playerpost__status='APPROVED', 
        playerpost__character_token__isnull=True
    ).last()
    
    if not active_background:
        backgrounds = BackgroundAsset.objects.all()
        if backgrounds.exists():
            active_background = backgrounds.first()
    
    if active_background:
        data = {
            'id': active_background.id,
            'title': active_background.title,
            'image_url': active_background.image.url,
        }
    else:
        data = None
    
    return JsonResponse({'active_map': data})
