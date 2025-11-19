from django.shortcuts import render, redirect, get_object_or_404
from .models import Email, AnalysisResult
from .ai_engine import analyze_email_content  # Import our brain

def dashboard(request):
    # Get all emails, newest first
    emails = Email.objects.all().order_by('-received_at')
    
    # Calculate some basic stats for the top of the dashboard
    total_emails = emails.count()
    high_risk_count = AnalysisResult.objects.filter(risk_score__gt=70).count()
    
    context = {
        'emails': emails,
        'total_emails': total_emails,
        'high_risk_count': high_risk_count
    }
    return render(request, 'dashboard.html', context)

def analyze_email(request, email_id):
    """
    This view is triggered when the user clicks 'Analyze' button.
    It calls the AI Engine and saves the result to the DB.
    """
    email = get_object_or_404(Email, id=email_id)
    
    # 1. Call the Brain
    analysis_data = analyze_email_content(email.subject, email.body)
    
    # 2. Save the Result to Database
    AnalysisResult.objects.update_or_create(
        email=email,
        defaults={
            'summary': analysis_data['summary'],
            'sentiment': analysis_data['sentiment'],
            'tone': analysis_data['tone'],
            'risk_score': analysis_data['risk_score'],
            'suggested_category': analysis_data['suggested_category'],
            'suggested_reply': analysis_data['suggested_reply'],
        }
    )
    
    # 3. Mark email as analyzed
    email.is_analyzed = True
    email.save()
    
    return redirect('dashboard')