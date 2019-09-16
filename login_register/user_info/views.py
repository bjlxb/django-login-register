import io
import re
import base64
import time

from captcha.image import ImageCaptcha
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.


# 提前准备注册
from django.views.decorators.csrf import csrf_exempt

from user_info.models import CodeHistory
from user_info.utils import IpUtil, RandomUtil


@csrf_exempt
def do_prepare_register(request):
    if request.method != "POST":
        return JsonResponse({"status": "error", "data": {}, "msg": "请求方式不正确！"})
    phone = request.POST.get("phone")
    email = request.POST.get("email")

    if phone:
        ret = re.match("^((13[0-9])|(14[5,7])|(15[0-3,5-9])|(17[0,3,5-8])|(18[0-9])|166|198|199|(147))\\d{8}$",
                       phone.replace(' ', ''))
        if not ret:
            return JsonResponse({"status": "error", "data": {}, "msg": "手机号有误！"})
    elif email:
        ret = re.match("^([\w\.\-]+)\@(\w+)(\.([\w^\_]+)){1,2}$", email.replace(' ', ''))
        if not ret:
            return JsonResponse({"status": "error", "data": {}, "msg": "邮箱有误！"})
    else:
        return JsonResponse({"status": "error", "data": {}, "msg": "缺少参数！"})

    ip_util = IpUtil()
    now_time = time.time()
    ip = ip_util.get_ip(request)

    randomu_til = RandomUtil()
    random_str_for_img_captcha = randomu_til.num_random()
    random_str_for_code = randomu_til.num_random()

    image = ImageCaptcha()

    # captcha_number = "123456"  # random_str_for_img_captcha
    captcha_number = random_str_for_img_captcha
    captcha_img = image.generate_image(captcha_number)
    buffer = io.BytesIO()
    captcha_img.save(buffer, format="PNG")
    img_str = base64.b64encode(buffer.getvalue())

    code_history = CodeHistory()
    code_history.email_or_phone = email if email else phone
    code_history.kind = "准备注册"
    code_history.captcha_for_img = captcha_number
    code_history.code = random_str_for_code
    code_history.ip_address = ip
    code_history.expire_datetime = now_time + 20 * 60
    code_history.save()

    data = {
        "tracking_id": "",
        "image": str(img_str, "utf-8")
    }
    print(img_str)
    print(str(img_str, "utf-8"))
    return JsonResponse({"status": "success", "data": data, "msg": "获取成功！"})


# 注册
def do_register(request):
    pass


# 登录
def do_login_by_pwd(request):
    pass
