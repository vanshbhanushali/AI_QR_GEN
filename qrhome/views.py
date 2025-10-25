from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse, JsonResponse  # <-- JsonResponse is essential
from django.db import IntegrityError

from .models import QRCodeHistory, UserProfile  # <-- Ensure these models are imported
from django.urls import reverse

# Libraries for QR Code Generation
import qrcode
from io import BytesIO
import base64
from PIL import Image

# Gemini API Imports
from google import genai 
from google.genai.errors import APIError

# --- Configuration ---
# WARNING: Store this securely in settings.py or environment variables in a real project!
GEMINI_API_KEY = "AIzaSyARUjS52hufeEvp1nL9EIk1cvTguu766oA" 


# ------------------------------------------------------------------
# GEMINI AI FUNCTION (Replaces the Mock function)
# ------------------------------------------------------------------

def ai_content_generator(prompt: str) -> str:
    """Uses the Gemini API to generate content based on the user's prompt."""
    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
        
        system_instruction = (
            "You are a QR code content generator. Based on the user's request, "
            "provide a single, clean output suitable for direct encoding into a QR code. "
            "This should be a simple URL, vCard text, or a short, single message. "
            "Do not include any introductory phrases like 'Here is the link:', only the content itself."
        )

        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=genai.types.GenerateContentConfig(
                system_instruction=system_instruction
            )
        )
        
        return response.text.strip()

    except APIError as e:
        print(f"Gemini API Error: {e}")
        # Return a safe error message/link for the QR code
        return "https://api-error.check-console.com"
    except Exception as e:
        print(f"General Error during Gemini call: {e}")
        return "Internal_Error_Try_Again"


# ------------------------------------------------------------------
# UTILITY FUNCTION: QR Code Generation
# ------------------------------------------------------------------

def generate_qr_code(data_content: str) -> str:
    """Generates a QR code image as a base64 encoded string."""
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data_content)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white").convert('RGB')
    
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    
    qr_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    
    return qr_base64


# ------------------------------------------------------------------
# CORE VIEW FUNCTIONS
# ------------------------------------------------------------------

def login_signup_view(request):
    """Handles both user login and registration."""
    # ... (Your existing login_signup_view logic here, using the UserProfile model)
    if request.user.is_authenticated:
        return redirect('qrhome:index')

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'register':
            name = request.POST.get('name')
            mobile_number = request.POST.get('mobile_number')
            password = request.POST.get('password')
            
            if not all([name, mobile_number, password]):
                messages.error(request, "All fields are required for registration.")
                return redirect('qrhome:login_signup')

            try:
                user = User.objects.create_user(
                    username=mobile_number, 
                    password=password,
                    first_name=name 
                )
                UserProfile.objects.create(user=user, mobile_number=mobile_number)
                
                messages.success(request, "Registration successful! You can now log in.")
                return redirect('qrhome:login_signup') 
                
            except IntegrityError:
                messages.error(request, "A user with this mobile number already exists.")
            except Exception as e:
                messages.error(request, f"An unexpected error occurred: {e}")
                
        elif action == 'login':
            username = request.POST.get('username')
            password = request.POST.get('password')
            
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {user.first_name}!")
                return redirect('qrhome:index')
            else:
                messages.error(request, "Invalid mobile number or password.")
                
    return render(request, 'qrhome/login_signup.html')


def user_logout(request):
    """Logs out the user and redirects to the home page."""
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('qrhome:index')


def index(request):
    """The home page with project description and toggle bar."""
    context = {
        'project_title': 'AIQRGen: The Smart QR Generator',
        'objective': 'Generate dynamic and visually appealing QR codes powered by AI.',
        'features': [
            'AI-Powered Content Suggestions',
            'Customizable QR Appearance',
            'Easy History Tracking'
        ],
    }
    return render(request, 'qrhome/index.html', context)


# ------------------------------------------------------------------
# QRCODE GENERATOR (HANDLING AJAX BEFORE DECORATOR)
# ------------------------------------------------------------------

def qrcode_generator(request):
    """
    Handles both AJAX content generation and standard QR code submission.
    NOTE: The manual authentication check for AJAX is done inside the function.
    """
    
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
    
    # 1. SPECIAL CASE: HANDLE UNAUTHENTICATED AJAX REQUESTS
    # The @login_required decorator is NOT used here because we need to return
    # JSON for AJAX, not an HTML redirect. We check manually.
    if is_ajax and not request.user.is_authenticated:
        # Return a 401 status code with a JSON payload
        return JsonResponse({
            'error': 'Authentication required. Please log in.',
            'login_url': reverse('qrhome:login_signup')
        }, status=401)


    # 2. HANDLE AI GENERATION VIA AJAX (If user IS authenticated)
    if is_ajax and request.method == 'POST':
        prompt = request.POST.get('prompt_used', '').strip()
        
        if prompt:
            try:
                generated_content = ai_content_generator(prompt)
                return JsonResponse({'content': generated_content})
            except Exception as e:
                print(f"Server-side AI Error: {e}")
                return JsonResponse({'error': 'AI service failed due to a server error.'}, status=500)
        else:
            return JsonResponse({'error': 'Prompt cannot be empty.'}, status=400)


    # 3. HANDLE STANDARD QR CODE SUBMISSION (POST or GET)
    
    # Standard security check for non-AJAX POST requests
    if not request.user.is_authenticated and request.method == 'POST':
        messages.error(request, "You must be logged in to generate QR codes.")
        return redirect('qrhome:login_signup')
        
    qr_code_base64 = None
    data_content = request.POST.get('data_content', '').strip()
    prompt_used = request.POST.get('prompt_used', '').strip()

    if request.method == 'POST':
        
        if not data_content:
            messages.error(request, "Please enter content to generate the QR code.")
            
        else:
            try:
                # Generate QR code
                qr_code_base64 = generate_qr_code(data_content)
                
                # Save to History
                QRCodeHistory.objects.create(
                    user=request.user,
                    data_content=data_content,
                    prompt_used=prompt_used if prompt_used else None,
                    qr_code_path=qr_code_base64 
                )
                
                messages.success(request, "QR Code generated and saved to your history!")
                
            except Exception as e:
                messages.error(request, f"Failed to generate QR Code: {e}")

    context = {
        'qr_code_base64': qr_code_base64,
        'initial_data_content': data_content,
        'initial_prompt_used': prompt_used
    }
    return render(request, 'qrhome/qrcode.html', context)


@login_required(login_url='/login_signup/')
def history_view(request):
    """Displays the user's QR code generation history."""
    # Fetch history for the logged-in user
    history = QRCodeHistory.objects.filter(user=request.user).order_by('-generated_at')
    context = {
        'history': history,
        'count': history.count()
    }
    return render(request, 'qrhome/history.html', context)