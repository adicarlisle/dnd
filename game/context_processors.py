from django.conf import settings

def supabase_config(request):
    """
    Context processor to make Supabase configuration available in templates
    """
    return {
        'SUPABASE_URL': settings.SUPABASE_URL,
        'SUPABASE_ANON_KEY': settings.SUPABASE_ANON_KEY,
    }
