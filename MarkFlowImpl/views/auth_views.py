import random
import re
import smtplib
import string
import traceback
import redis
from venv import logger

from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import send_mail
from django.http import JsonResponse
from faker import Faker
from rest_framework.decorators import api_view
from rest_framework.response import Response

from MarkFlow import settings
from MarkFlowImpl.models import *


# Create your views here.
@api_view(["POST"])
def login(request):
    # 1. 获取请求参数
    account = request.data.get('account')
    password = request.data.get('password')
    # 2. 参数验证
    if not account or not password:
        return Response({'success': False, 'userName': None})
        # 检查account是否包含无效字符（如仅含换行符、空格等）
    if re.fullmatch(r'\s*', account):  # 匹配纯空白字符（包括换行符）
        print(f"错误：account参数为无效空白字符：{account}")
        return JsonResponse({'success': False, 'userName': None})

    # 3. 查询用户
    try:
        # 先尝试按邮箱查询
        user = User.objects.get(email=account)
    except User.DoesNotExist:
        try:
            if not account.isdigit():  # 判断是否为纯数字
                print(f"错误：账号{account}既不是邮箱也不是数字ID")
                return JsonResponse({'success': False, 'userName': None})
            # 再尝试按ID查询
            user = User.objects.get(id=account)
        except User.DoesNotExist:
            return Response({'success': False, 'userName': None})

    # 4. 验证密码
    # 使用Django内置的check_password函数验证密码
    # 该函数会自动处理密码的哈希比较，无需手动实现
    # check_password会执行以下操作：
    # 1. 从数据库中获取存储的密码哈希值（user.password_hash）
    # 2. 解析哈希值中的算法和盐值
    # 3. 使用相同的算法和盐值对用户输入的密码进行哈希处理
    # 4. 将处理后的哈希值与数据库中存储的哈希值进行比较
    # 5. 返回比较结果（布尔值）
    if not check_password(password, user.password_hash):
        return Response({'success': False, 'userName': None})
    print(user.id)
    print("登录成功")
    # 5. 登录成功，返回用户信息
    return Response({
        'success': True,
        'username': user.id,  # 返回用户名而不是ID
        'userId': user.user_name  # 同时返回用户ID

    })


@api_view(["POST"])
def verification(request):
    try:
        # 1. 获取并验证邮箱
        email = request.data.get('email')
        print(email)
        if not email:
            return JsonResponse({'success': False, 'message': '邮箱为空'})

        if User.objects.filter(email=email).exists():
            return JsonResponse({
                'success': False,
                'message': "该邮箱已注册"
            })
        print("here1")
        # 2. 连接 Redis
        try:
            logger.debug("开始连接 Redis...")
            r = redis.Redis(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB,
                password=settings.REDIS_PASSWORD,
                decode_responses=True,
                socket_timeout=5,
                socket_connect_timeout=5
            )

            # 强制测试连接
            logger.debug("执行 Redis ping 测试...")
            ping_response = r.ping()
            logger.debug(f"Redis ping 响应: {ping_response}")

        except Exception as e:
            # 关键：使用 traceback 获取完整堆栈信息
            error_stack = traceback.format_exc()
            logger.error(f"Redis 连接失败: {str(e)}\n堆栈信息:\n{error_stack}")
            return JsonResponse({'success': False, 'message': '验证码服务暂时不可用，请稍后再试'})
        print("here2")
        # 3. 检查发送频率（防止恶意请求）
        cooldown_key = f'verification:cooldown:{email}'
        if r.exists(cooldown_key):
            return JsonResponse({'success': False, 'message': '请求过多'})
        print("here3")
        # 4. 生成随机6位验证码
        verification_code = ''.join(random.choices(string.digits, k=6))
        print("here4")
        # 5. 存储验证码到 Redis，设置5分钟过期时间
        code_key = f'verification:code:{email}'
        r.set(code_key, verification_code, ex=300)  # 300秒 = 5分钟
        print("here5")
        # 6. 设置发送冷却时间（1分钟内不能重复发送）
        r.set(cooldown_key, 1, ex=60)
        print("here6")
        # 7. 发送邮件（邮件内容包含真实验证码）
        subject = '账号验证 - 验证码'
        message = f'您的验证码是：{verification_code}，请在5分钟内使用。'
        try:
            # 发送邮件
            send_mail(subject, message, "", [email])
            print(f"[成功] 验证码邮件已发送至: {email}")
        except smtplib.SMTPException as e:
            # SMTP 协议相关错误（如连接失败、认证错误）
            print(f"[错误] 邮件发送失败 (SMTP 错误): {str(e)}")
            # 可以选择删除 Redis 中的验证码，避免用户收到无效验证码
            r.delete(f'verification:code:{email}')
            return JsonResponse({'success': False, 'message': '验证码发送失败，请稍后再试'})
        except ConnectionRefusedError as e:
            # 连接被拒绝（如 SMTP 服务器未运行或端口错误）
            print(f"[错误] 邮件服务器连接被拒绝: {str(e)}")
            r.delete(f'verification:code:{email}')
            return JsonResponse({'success': False, 'message': '邮件服务器暂时不可用，请稍后再试'})
        except TimeoutError as e:
            # 连接超时
            print(f"[错误] 邮件发送超时: {str(e)}")
            r.delete(f'verification:code:{email}')
            return JsonResponse({'success': False, 'message': '验证码发送超时，请稍后再试'})
        except Exception as e:
            # 其他未知错误
            print(f"[错误] 邮件发送异常: {str(e)}")
            r.delete(f'verification:code:{email}')
            return JsonResponse({'success': False, 'message': '服务器内部错误，请联系管理员'})
        print("here7")
        # 8. 返回成功响应（verificationCode 为空，前端仅知道发送成功）
        return JsonResponse({'success': True})

    except Exception as e:
        str(e)
        return JsonResponse({'success': False, 'message': '服务器出差了'})


@api_view(["POST"])
def register(request):
    try:
        # 1. 获取注册数据
        email = request.data.get('email')
        verification_code = request.data.get('verification')
        password = request.data.get('password')
        print(email, verification_code, password)
        # 2. 参数验证
        if not all([email, verification_code, password]):
            print("错误: 缺少必要参数（email、verification 或 password）")
            return JsonResponse({
                'success': False,
                'message': "缺失必要参数"  # 注册失败时 userId 为 None
            })
        # 7. 检查邮箱是否已注册
        if User.objects.filter(email=email).exists():
            print(f"检查邮箱是否已注册: {email} ")
            return JsonResponse({
                'success': False,
                'message': "邮箱已注册"
            })
        # 3. 连接 Redis 验证验证码
        try:
            r = redis.Redis(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB,
                password=settings.REDIS_PASSWORD,
                decode_responses=True,
                socket_timeout=5  # 设置超时，避免无限等待
            )
            # 测试 Redis 连接
            r.ping()
            print("Redis 连接成功")
        except Exception as e:
            print(f"Redis 连接失败: {str(e)}")
            print(f"Redis 错误堆栈: {traceback.format_exc()}")
            return JsonResponse({
                'success': False,
                'message': "服务器出差了"
            })

        # 4. 获取存储的验证码
        code_key = f'verification:code:{email}'
        stored_code = r.get(code_key)
        print(f"从 Redis 获取验证码 - key: {code_key}, stored_code: {stored_code}")

        # 5. 验证验证码（检查是否存在、是否匹配）
        if not stored_code:
            print("错误: Redis 中未找到验证码（可能已过期）")
            return JsonResponse({
                'success': False,
                'message': "验证码不存在"
            })
        if stored_code != verification_code:
            print(f"错误: 验证码不匹配 - 提交的: {verification_code}, 存储的: {stored_code}")
            return JsonResponse({
                'success': False,
                'message': "验证码不匹配"
            })

        # 6. 验证通过后，删除 Redis 中的验证码（防止重复使用）
        r.delete(code_key)
        print(f"已删除 Redis 中的验证码: {code_key}")

        # 8. 密码哈希加密（使用 Django 内置函数）
        password_hash = make_password(password)
        print(f"密码加密完成 - 原始密码长度: {len(password)}, 哈希后长度: {len(password_hash)}")

        # 9. 生成用户名
        fake = Faker('zh_CN')  # 使用中文环境
        username = fake.user_name()  # 生成用户名

        # 确保用户名长度在2-5个字符之间
        while len(username) < 2 or len(username) > 5:
            username = fake.user_name()

        # 确保用户名唯一
        while User.objects.filter(username=username).exists():
            username = fake.user_name()
            # 再次检查长度
            while len(username) < 2 or len(username) > 5:
                username = fake.user_name()

        print(f"为用户生成用户名: {username}")

        # 10. 创建用户
        try:
            user = User(
                email=email,
                password_hash=password_hash,
                username=username
            )
            user.save()
            print(f"用户创建成功 - id: {user.id}, email: {user.email}")
        except Exception as e:
            print(f"用户创建失败: {str(e)}")
            print(f"用户创建错误堆栈: {traceback.format_exc()}")
            return JsonResponse({
                'success': False,
                'message': "服务器出差了"
            })
        return JsonResponse({
            'success': True,
            'message': "注册成功"
        })

    except Exception as e:
        error_stack = traceback.format_exc()
        logger.error(f"Redis 连接失败: {str(e)}\n堆栈信息:\n{error_stack}")
        return JsonResponse({
            'success': False,
            'message': "服务器出差了"
        })

