"""
Vistas de Django para Autenticación, Dashboard e Inspección de Vehículos
"""
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from functools import wraps
from .services import FastAPIService

def inspector_login_required(view_func):
    """Decorador para proteger vistas del frontend mediante sesión"""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Permitir si hay sesión de Django o token en sesión
        if request.user.is_authenticated or request.session.get("is_authenticated"):
            return view_func(request, *args, **kwargs)
        messages.warning(request, "Por favor inicie sesión para acceder al sistema de inspección.")
        return redirect("login")
    return _wrapped_view


def login_view(request):
    """Vista de inicio de sesión de inspector"""
    if request.user.is_authenticated or request.session.get("is_authenticated"):
        return redirect("dashboard")

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()

        # Permitir credenciales por defecto o usuarios creados
        if (username == "inspector" and password == "sena2026") or (username == "admin" and password == "admin123"):
            request.session["is_authenticated"] = True
            request.session["username"] = username
            request.session["full_name"] = "Jonathan SENA - Inspector" if username == "inspector" else "Administrador"
            request.session["role"] = "Inspector Vehicular" if username == "inspector" else "Administrador"
            messages.success(request, f"¡Bienvenido, {request.session['full_name']}!")
            return redirect("dashboard")
        else:
            # Intentar auth nativo Django
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                request.session["is_authenticated"] = True
                request.session["username"] = user.username
                request.session["full_name"] = user.get_full_name() or user.username
                request.session["role"] = "Inspector Vehicular"
                messages.success(request, f"¡Bienvenido, {request.session['full_name']}!")
                return redirect("dashboard")
            else:
                messages.error(request, "Credenciales incorrectas. Verifique usuario y contraseña.")

    return render(request, "login.html")


def logout_view(request):
    """Cerrar sesión"""
    logout(request)
    request.session.flush()
    messages.info(request, "Sesión cerrada exitosamente.")
    return redirect("login")


@inspector_login_required
def dashboard_view(request):
    """Dashboard principal de inspecciones"""
    return render(request, "dashboard.html", {
        "user_name": request.session.get("full_name", "Inspector"),
        "role": request.session.get("role", "Inspector Vehicular"),
    })


@inspector_login_required
def inspect_view(request):
    """Vista de captura de cámara e inspección con IA"""
    return render(request, "inspect.html", {
        "user_name": request.session.get("full_name", "Inspector"),
        "role": request.session.get("role", "Inspector Vehicular"),
    })


@inspector_login_required
def report_view(request):
    """Vista de reporte / acta digital de entrega"""
    return render(request, "report.html", {
        "user_name": request.session.get("full_name", "Inspector"),
        "role": request.session.get("role", "Inspector Vehicular"),
    })


@csrf_exempt
def api_inspect_proxy(request):
    """
    Proxy HTTP seguro entre el cliente frontend Django y la API FastAPI.
    Permite enviar capturas de cámara multipart hacia POST /api/v1/inspect-vehicle
    evitando bloqueos de CORS o diferencias de dominio.
    """
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido. Use POST."}, status=405)

    try:
        vehicle_id = request.POST.get("vehicle_id", "ABC-123")
        side_position = request.POST.get("side_position", "Lateral Derecho")
        notes = request.POST.get("notes", "")

        file = request.FILES.get("file")
        if not file:
            return JsonResponse({"error": "No se recibió archivo de imagen."}, status=400)

        image_bytes = file.read()
        filename = file.name

        # Llamar al servicio FastAPI
        result = FastAPIService.inspect_vehicle(
            image_bytes=image_bytes,
            filename=filename,
            vehicle_id=vehicle_id,
            side_position=side_position,
            notes=notes
        )

        return JsonResponse(result, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e), "damage_detected": False}, status=500)

