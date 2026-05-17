from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm # 🧙‍♂️ Added for administrative registration
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

    # 🛠️ Initialize an empty registration form shell context if the user is a DM
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
                # We do not redirect on a validation fail so the field errors render in place!

        # 👑 SUBMISSION A: DM Map Control Update Event
        elif "dm_map_control" in request.POST:
            if not request.user.is_superuser:
                return redirect('dashboard')
                
            bg_id = request.POST.get('active_map')
            if bg_id:
                selected_bg = BackgroundAsset.objects.get(id=bg_id)
                # Save a system master declaration track straight to the database
                PlayerPost.objects.create(
                    player=request.user,
                    message=f"DM updated active battlefield scene to: {selected_bg.title}",
                    selected_background=selected_bg,
                    status='APPROVED'
                )
                messages.success(request, f"Tabletop canvas transitioned to {selected_bg.title}!")
            return redirect('dashboard')

        # 🧝 SUBMISSION B: Normal Player Character Token/Action Post
        else:
            message_text = request.POST.get('message')
            uploaded_token = request.FILES.get('token_image') # Handled cleanly via FileField now!
            
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
        'user_form': user_form, # Injected back to layout template canvas context
    }
    return render(request, 'index.html', context)


# 👑 THE DM REVIEW ENDPOINTS
@login_required
def dm_review_panel(request):
    # Kick anyone out who tries to type this URL manually without admin clearance
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
    # Security checkpoint: Only the DM can delete files
    if not request.user.is_superuser:
        return redirect('dashboard')
        
    asset = get_object_or_404(BackgroundAsset, id=asset_id)
    title = asset.title
    
    # This automatically removes the record from your DB 
    # (And django-storages will handle letting Supabase know to clear the file!)
    asset.delete()
    
    messages.success(request, f"Successfully purged map scene: '{title}'")
    return redirect('dashboard')


@login_required
def delete_player_post(request, post_id):
    if not request.user.is_superuser:
        return redirect('dashboard')
        
    post = get_object_or_404(PlayerPost, id=post_id)
    player_name = post.player.username
    
    post.delete()
    
    messages.success(request, f"Removed action layer submitted by {player_name}.")
    return redirect('dashboard')