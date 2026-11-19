# Deploy SortLab 3D on Render

This project needs GCC at runtime because the Flask backend compiles and runs C sorting programs. Deploy it as a Docker Web Service.

## Files
- `Dockerfile` installs GCC and Python dependencies, then starts Flask with Gunicorn.
- `requirements.txt` includes Flask and Gunicorn.
- `.dockerignore` excludes the local virtual environment.

## Steps
1. Extract this folder and create a GitHub repository.
2. Upload the contents of this folder to the repository root. Do not upload `venv`.
3. On Render, choose **New + → Web Service** and connect the GitHub repository.
4. Set **Language/Runtime** to **Docker**. Keep the Dockerfile path as `./Dockerfile`.
5. Choose a region and plan, then create the service. No separate build or start command is required; the Dockerfile supplies them.
6. Wait for the deploy to finish and open the `https://<service-name>.onrender.com` URL.

Free Render web services may spin down after inactivity, so the first visit after a quiet period can take longer. Check Render's current plan limits before using it for a class session.
