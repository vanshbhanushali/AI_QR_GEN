import os
import sys
import subprocess # Need this to run commands
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# --- Vercel Build Hook ---
# Check if running in Vercel build environment (Vercel sets VERCEL_ENV=production during build)
IS_VERCEL_BUILD = os.environ.get('VERCEL_ENV') == 'production' 

if IS_VERCEL_BUILD:
    print("Build Hook: Vercel build environment detected.")
    # Use python3.11 as specified in vercel.json
    PYTHON_EXEC = "python3.11" 
    try:
        print("Build Hook: Running migrate...")
        # Use check=True to raise an error if the command fails
        subprocess.run(
            [PYTHON_EXEC, "manage.py", "migrate", "--noinput"], 
            check=True, capture_output=True, text=True
        )
        print("Build Hook: Migrate successful.")

        print("Build Hook: Running collectstatic...")
        # Use check=True to raise an error if the command fails
        subprocess.run(
            [PYTHON_EXEC, "manage.py", "collectstatic", "--noinput", "--clear"], 
            check=True, capture_output=True, text=True
        )
        print("Build Hook: Collectstatic successful.")

    except subprocess.CalledProcessError as e:
        # Print detailed error information if a command fails
        print(f"Build Hook Error: Command '{' '.join(e.cmd)}' failed.")
        print(f"Build Hook Error: Return Code: {e.returncode}")
        print(f"Build Hook Error: STDOUT:\n{e.stdout}")
        print(f"Build Hook Error: STDERR:\n{e.stderr}")
        sys.exit(1) # Exit with error code to explicitly fail the build
    except Exception as e:
        print(f"Build Hook Error: An unexpected error occurred: {e}")
        sys.exit(1) # Exit with error code
# --- End Vercel Build Hook ---

# Standard WSGI setup
application = get_wsgi_application()
# Expose 'app' for Vercel
app = application