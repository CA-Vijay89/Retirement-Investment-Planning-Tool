from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.template.loader import get_template

from django.contrib import messages

from xhtml2pdf import pisa

# ---------------- ML IMPORTS ----------------
from ML_MODELS.risk_profile_predictor import predict_risk_profile
from ML_MODELS.Inflation_DL import predict_inflation_rate

from Project_Input import (
    cagr_Nifty50,
    cagr_gold,
    cagr_silver,
    FD_yield
)

# ------------------------------------------------
# CONSTANT TEXT
# ------------------------------------------------

EXECUTIVE_SUMMARY = (
    "This AI-powered retirement planning report provides a personalized investment "
    "strategy based on demographic and financial inputs. The recommendations aim to "
    "ensure retirement adequacy while maintaining affordability and risk alignment."
)

AI_METHODOLOGY = (
    "The risk profile in this report is generated using a machine learning model "
    "trained on demographic, educational, and professional attributes. The model "
    "assesses the user’s ability to take risk and recommends an optimal asset allocation."
)

RISK_DESCRIPTIONS = {
    "Conservative": (
        "A Conservative investor prioritizes capital protection and stable returns, "
        "with higher allocation to fixed income and lower equity exposure."
    ),
    "Moderate": (
        "A Moderate investor seeks a balance between growth and stability through a "
        "diversified mix of equity, debt, and precious metals."
    ),
    "Aggressive": (
        "An Aggressive investor focuses on long-term capital appreciation and is "
        "comfortable with higher market volatility, allocating more towards equities."
    )
}

# ------------------------------------------------
# AUTH
# ------------------------------------------------

def home(request):
    return redirect("login")



def register_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        # --- VALIDATIONS ---
        if not all([username, email, password1, password2]):
            messages.error(request, "All fields are required.")
            return render(request, "register.html")

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return render(request, "register.html")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, "register.html")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return render(request, "register.html")

        # --- CREATE USER ---
        User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )

        messages.success(request, "Account created successfully. Please log in.")
        return redirect("login")

    return render(request, "register.html")



def login_user(request):
    if request.method == "POST":
        user = authenticate(
            username=request.POST["username"],
            password=request.POST["password"]
        )
        if user:
            login(request, user)
            return redirect("dashboard")
    return render(request, "login.html")


def logout_user(request):
    logout(request)
    return redirect("login")

# ------------------------------------------------
# HELPERS
# ------------------------------------------------

def monthly_factor(annual_return, months):
    r_m = annual_return / 12
    if abs(r_m) < 1e-9:
        return months
    return ((1 + r_m) ** months - 1) / r_m


def get_asset_weights(risk):
    risk = risk.lower()
    if risk == "aggressive":
        return {"Nifty 50": 0.70, "Gold": 0.15, "Silver": 0.15, "FD": 0.00}
    elif risk == "moderate":
        return {"Nifty 50": 0.40, "Gold": 0.20, "Silver": 0.20, "FD": 0.20}
    return {"Nifty 50": 0.30, "Gold": 0.30, "Silver": 0.00, "FD": 0.40}

# ------------------------------------------------
# DASHBOARD
# ------------------------------------------------

@login_required
def dashboard(request):
    context = {}

    if request.method == "POST":

        # -------- INPUTS --------
        age = int(request.POST["age"])
        gender = request.POST["gender"]
        education = request.POST["education"]
        field = request.POST["field"]
        expenses = float(request.POST["expenses"])
        retirement_age = int(request.POST.get("retirement_age") or 60)

        years = retirement_age - age
        months = years * 12
        annuity_rate = 7

        # -------- ML OUTPUTS --------
        risk = predict_risk_profile(age, gender, education, field)
        if risk.lower() == "agressive":
            risk = "aggressive"
        risk = risk.title()

        inflation = predict_inflation_rate()

        # -------- RETIREMENT CALCULATIONS --------
        projected_expenses = expenses * ((1 + inflation) ** years)
        corpus_required = (projected_expenses * 12) / (annuity_rate / 100)

        # -------- ASSET RETURNS --------
        assets = {
            "Nifty 50": cagr_Nifty50,
            "Gold": cagr_gold,
            "Silver": cagr_silver,
            "FD": FD_yield / 100
        }

        weights = get_asset_weights(risk)

        # -------- SIP CALCULATION --------
        factors = {a: monthly_factor(r, months) for a, r in assets.items()}
        denom = sum(weights[a] * factors[a] for a in weights)
        monthly_sip = corpus_required / denom

        asset_sip_table = [
            (a, int(weights[a] * 100), round(monthly_sip * weights[a], 0))
            for a in weights
        ]

        # -------- SIP GROWTH (CORRECT) --------
        asset_balances = {a: 0 for a in weights}
        sip_growth, growth_years = [], []

        for m in range(1, months + 1):
            for a in weights:
                asset_balances[a] = (
                    asset_balances[a] * (1 + assets[a] / 12)
                    + monthly_sip * weights[a]
                )
            if m % 12 == 0:
                sip_growth.append(round(sum(asset_balances.values()), 0))
                growth_years.append(m // 12)

        context = {
            "inputs": {
                "age": age,
                "gender": gender,
                "education": education,
                "field": field,
                "expenses": expenses,
                "retirement_age": retirement_age
            },
            "result": {
                "risk": risk,
                "investment_years": years,
                "projected_expenses": round(projected_expenses, 0),
                "corpus_required": round(corpus_required, 0),
                "monthly_sip": round(monthly_sip, 0)
            },
            "assumptions": {
                "inflation": round(inflation * 100, 2),
                "annuity": annuity_rate,
                "returns": {
                    "Nifty 50": round(cagr_Nifty50 * 100, 2),
                    "Gold": round(cagr_gold * 100, 2),
                    "Silver": round(cagr_silver * 100, 2),
                    "FD": round(FD_yield, 2)
                }
            },
            "asset_sip_table": asset_sip_table,
            "allocation_labels": list(weights.keys()),
            "allocation_percentages": [int(v * 100) for v in weights.values()],
            "allocation_sip_values": [round(monthly_sip * v, 0) for v in weights.values()],
            "growth_years": growth_years,
            "growth_values": sip_growth,
            "charts": {
                "allocation": request.POST.get("allocation_chart_img"),
                "growth": request.POST.get("growth_chart_img")
            },
            "executive_summary": EXECUTIVE_SUMMARY,
            "ai_methodology": AI_METHODOLOGY,
            "risk_description": RISK_DESCRIPTIONS.get(risk, "")
        }

        request.session["report_context"] = context

    return render(request, "dashboard.html", context)

# ------------------------------------------------
# PDF DOWNLOAD
# ------------------------------------------------

@login_required
def download_report(request):
    context = request.session.get("report_context")
    if not context:
        return redirect("dashboard")

    template = get_template("report.html")
    html = template.render(context)

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="Retirement_Planner_Report.pdf"'

    pisa.CreatePDF(html, dest=response)
    return response


import json
from django.views.decorators.csrf import csrf_exempt

@login_required
@csrf_exempt
def store_charts(request):
    if request.method == "POST":
        data = json.loads(request.body)
        context = request.session.get("report_context", {})
        context["charts"] = {
            "allocation": data.get("allocation"),
            "growth": data.get("growth")
        }
        request.session["report_context"] = context
        return HttpResponse("OK")

