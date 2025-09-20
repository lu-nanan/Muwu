from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q, F
from MarkFlowImpl.models import User, UserWords


class UserWordStatsAPIView(APIView):
    """
    用户单词统计接口（简单版，兼容所有Django版本）
    接收：userid → 返回：username + 三类单词数量
    """

    def post(self, request):
        print("\n" + "=" * 80)
        print(f"[UserWordStatsAPIView] 收到用户单词统计请求，开始处理")
        print("=" * 80)

        # -------------------------- 1. 接收参数 --------------------------
        print(f"\n[Step 1/4] 接收请求参数")
        try:
            request_data = request.data if isinstance(request.data, dict) else request.POST.dict()
            userid = request_data.get("userid")
            print(f"[Step 1/4] 解析到userid：{userid}")
        except Exception as e:
            error_msg = f"参数解析失败：{str(e)}"
            print(error_msg)
            return Response({"success": False, "message": error_msg}, status=400)

        # -------------------------- 2. 校验用户 --------------------------
        print(f"\n[Step 2/4] 校验用户合法性")
        # 校验userid格式
        if not userid or not userid.isdigit():
            error_msg = "userid必须是整数"
            print(error_msg)
            return Response({"success": False, "message": error_msg}, status=400)
        userid = int(userid)

        # 校验用户是否存在
        try:
            user = User.objects.get(id=userid)
            username = user.user_name or "未设置用户名"  # 处理空用户名
            print(f"[Step 2/4] 用户存在：userid={userid}，username={username}")
        except User.DoesNotExist:
            error_msg = f"用户不存在（userid={userid}）"
            print(error_msg)
            return Response({"success": False, "message": error_msg}, status=400)

        # -------------------------- 3. 统计单词（核心：用字段运算判断正确率） --------------------------
        print(f"\n[Step 3/4] 开始统计各类型单词数量")
        # 基础条件：当前用户 + 有基础单词关联
        base_filter = Q(user_id=userid) & Q(word__isnull=False)

        # 1. familiar：学习次数>0 且 正确率>0.75 → 用整数运算避免浮点数问题（correct_count*100 > learning_count*75）
        familiar_count = UserWords.objects.filter(
            base_filter,
            learning_count__gt=0,  # 先确保学习次数>0，避免除以0
            correct_count__gt=F('learning_count') * 75 / 100  # 正确率>0.75
        ).count()

        # 2. vague：两种情况（学习次数=0）+（学习次数>0且0.45≤正确率≤0.75）
        # 情况1：学习次数=0
        vague_case1 = UserWords.objects.filter(base_filter, learning_count__exact=0).count()
        # 情况2：学习次数>0 且 0.45≤正确率≤0.75 → 整数运算：correct_count*100 ≥ 45*learning_count 且 ≤75*learning_count
        vague_case2 = UserWords.objects.filter(
            base_filter,
            learning_count__gt=0,
            correct_count__gte=F('learning_count') * 45 / 100,
            correct_count__lte=F('learning_count') * 75 / 100
        ).count()
        vague_count = vague_case1 + vague_case2

        # 3. unfamiliar：学习次数>0 且 正确率<0.45 → 整数运算：correct_count*100 < 45*learning_count
        unfamiliar_count = UserWords.objects.filter(
            base_filter,
            learning_count__gt=0,
            correct_count__lt=F('learning_count') * 45 / 100  # 正确率<0.45
        ).count()

        # 打印统计结果
        print(f"[Step 3/4] 统计完成：")
        print(f"  - familiar：{familiar_count}个 | vague：{vague_count}个 | unfamiliar：{unfamiliar_count}个")

        # -------------------------- 4. 返回响应 --------------------------
        print(f"\n[Step 4/4] 返回响应")
        response_data = {
            "success": True,
            "message": "统计成功",
            "data": {
                "userid": userid,
                "username": username,
                "familiar_count": familiar_count,
                "vague_count": vague_count,
                "unfamiliar_count": unfamiliar_count,
                "total_count": familiar_count + vague_count + unfamiliar_count
            }
        }
        print(f"[Step 4/4] 响应完成：用户{username}共{response_data['data']['total_count']}个单词")
        print("=" * 80 + "\n")

        return Response(response_data)