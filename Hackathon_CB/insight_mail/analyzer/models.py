from django.db import models

class Email(models.Model):
    CATEGORY_CHOICES = [
        ('inquiry', 'General Inquiry'),
        ('complaint', 'Complaint'),
        ('support', 'Technical Support'),
        ('finance', 'Billing/Finance'),
        ('other', 'Other'),
    ]

    # 1. Basic Email Info
    subject = models.CharField(max_length=255)
    sender = models.EmailField()
    body = models.TextField()
    received_at = models.DateTimeField(auto_now_add=True)
    
    # 2. Workflow Status (To track progress on dashboard)
    is_analyzed = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.sender} - {self.subject}"

class AnalysisResult(models.Model):
    # Link this analysis to a specific email
    email = models.OneToOneField(Email, on_delete=models.CASCADE, related_name='analysis')
    
    # 1. The AI Interpretation
    summary = models.TextField(help_text="Short AI generated summary")
    sentiment = models.CharField(max_length=50, help_text="Positive, Neutral, Negative")
    tone = models.CharField(max_length=50, help_text="Formal, Aggressive, Urgent, etc.")
    
    # 2. Risk & Compliance
    risk_score = models.IntegerField(default=0, help_text="0-100 Risk Score")
    flagged_keywords = models.CharField(max_length=255, blank=True, null=True)
    
    # 3. Actionable Output
    suggested_category = models.CharField(max_length=50, default="inquiry")
    suggested_reply = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Analysis for: {self.email.subject}"