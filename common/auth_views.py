import random
import uuid
import base64
import requests
from django.conf import settings
from django.shortcuts import render, redirect
from methodism import generate_key
from common.models import User, Otp
from django.contrib.auth import login



def custom_encoder(data: str) -> str:
    """Base64 bilan shifrlash"""
    return base64.b64encode(data.encode()).decode()

def custom_decoder(data: str) -> str:
    """Base64 bilan shifrni ochish"""
    return base64.b64decode(data.encode()).decode()


def send_sms(code, mobile=None):
    if mobile is None:
        mobile = '998976755895'  # test uchun
    url = 'https://notify.eskiz.uz/api/message/sms/send'
    payload = {
        'mobile_phone': mobile,
        'message': f'Sizning OTP kodingiz: {code}',
        'from': '4546',
        'callback': 'http://0000.uz/test.php'
    }
    headers = {
        'Authorization': f"Bearer {settings.ESKIZ_TOKEN}"
    }
    # requests.post(url, headers=headers, data=payload)   # test uchun o'chirildi


def auth(request):
    phone = None
    if request.method == "POST":
        key = request.POST.get('login')
        data = request.POST
        if key:
            phone = data.get("login_phone")
            pas = data.get("login_pass")
            user = User.objects.filter(phone=phone).first()
            if not user or not user.check_password(str(pas)):
                return render(request, "auth/login.html", {"error": "Phone yoki Parol Xato"})
        else:
            phone = data.get("regis_phone")

        if not phone:
            return render(request, "auth/login.html", {"error": "Telefon raqam topilmadi"})

        # OTP yaratish
        code = random.randint(100_000, 999_999)

        try:
            message = f"Sizning OTP kodingiz : {code}"
            url = f"https://api.telegram.org/bot{settings.TG_TOKEN}/sendMessage?chat_id={6717501063}&text={message}"
            requests.get(url, timeout=5)
        except Exception as e:
            print("Telegram send error:", e)

        # OTP ni encode qilib saqlash (base64)
        unical = uuid.uuid4()
        gen_code = generate_key(15)
        natija = f"{unical}${code}${gen_code}"
        shifr = custom_encoder(natija)

        otp = Otp.objects.create(mobile=phone, key=shifr)
        request.session['key'] = otp.key

        return redirect("otp")

    return render(request, 'auth/login.html')



def otp(request):
    token = request.session.get("key")
    if not token:
        return redirect("auth")

    otp_obj = Otp.objects.filter(key=token).first()
    if not otp_obj:
        return redirect("auth")

    if request.method == "POST":
        otp_values = request.POST.getlist("otp[]")
        otp_values = [v.strip() for v in otp_values if v is not None]
        entered_code = "".join(otp_values)

        if not entered_code or len(entered_code) != 6 or not entered_code.isdigit():
            return render(request, "auth/otp.html", {"error": "Iltimos, 6 ta raqam kiriting"})

        try:
            decoded = custom_decoder(otp_obj.key)
        except Exception as e:
            print("custom_decoder error:", e)
            return render(request, "auth/otp.html", {"error": "Serverda xatolik yuz berdi (decode)"})

        parts = decoded.split("$")
        real_code = parts[1] if len(parts) > 1 else None

        if real_code and entered_code == real_code:
            #  OTP muvaffaqiyatli bo‘lsa:
            request.session["is_verified"] = True
            request.session["phone"] = otp_obj.mobile

            #  Endi foydalanuvchini Django auth tizimiga ham login qilamiz
            user = User.objects.filter(phone=otp_obj.mobile).first()
            if user:
                login(request, user)

            return redirect("home")
        else:
            return render(request, "auth/otp.html", {"error": "Noto‘g‘ri OTP kodi ❌ qayta urinib ko‘ring!"})

    return render(request, "auth/otp.html")



def logout(request):
    request.session.flush()
    return redirect('otp')
