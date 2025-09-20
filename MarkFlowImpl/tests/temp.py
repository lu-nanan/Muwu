# -------------------------- 第一步：先初始化Django环境（必须放在最前面！） --------------------------
import os
import sys
import django

from MarkFlow import settings

# 1. 计算项目根目录（关键：让Python能找到你的Django项目）
# 脚本路径：MarkFlowImpl/tests/temp.py → 向上跳2级到项目根目录（MarkFlow/）
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
# 把项目根目录加入Python的模块搜索路径
sys.path.append(project_root)

# 2. 指定Django的settings模块（格式：项目主配置目录.settings）
# 假设你的settings.py在 "MarkFlow/settings.py"（Django项目默认结构）
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MarkFlow.settings")

# 3. 初始化Django（这一步会加载settings配置）
django.setup()
print("✅ Django环境初始化完成，可正常使用Redis连接")

# -------------------------- 第二步：再导入并使用WordCacheManager --------------------------
from django_redis import get_redis_connection
import json
# 导入你的WordCacheManager（路径确保正确，你的原导入没问题）
from MarkFlowImpl.utils.word_cache_manager import WordCacheManager

try:
    # 要查看的用户ID（这里是10000，可根据需要修改）
    target_user_id = 10000
    # 生成缓存键（可选，仅用于打印确认）
    cache_key = f"word_cache:{target_user_id}"
    print(f"\n📌 准备查看用户 {target_user_id} 的缓存（Redis键：{cache_key}）")

    # 创建缓存管理器实例（此时get_redis_connection会正常读取settings的CACHES配置）
    cache_manager = WordCacheManager(target_user_id)

    # 查看缓存内容（调用你之前添加的print_cache_words()方法，格式清晰）
    print("\n" + "="*60)
    print(f"📋 用户 {target_user_id} 的Redis缓存详情：")
    cache_manager.print_cache_words()
    # # 2. 查看两种键前缀
    # print("=" * 60)
    # print("📌 缓存键前缀查看结果")
    # print("=" * 60)
    #
    # # （1）查看Django缓存框架的全局前缀（KEY_PREFIX）
    # django_cache_prefix = settings.CACHES["default"].get("KEY_PREFIX", "无")
    # print(f"1. Django缓存框架全局前缀（KEY_PREFIX）：{django_cache_prefix}")
    # print(f"   说明：Django会自动为所有通过cache.set()存储的键添加此前缀，格式如：{django_cache_prefix}:实际键名")
    #
    # # （2）查看WordCacheManager的自定义前缀
    # target_user_id = 10000  # 你要查看的用户ID
    # word_cache_prefix = "word_cache:"  # 从代码中提取的自定义前缀
    # full_cache_key = f"{word_cache_prefix}{target_user_id}"  # 完整的Redis键
    # print(f"\n2. WordCacheManager自定义前缀：{word_cache_prefix}")
    # print(f"   说明：用户单词缓存的完整键格式为「前缀+用户ID」")
    # print(f"   示例（用户{target_user_id}的完整缓存键）：{full_cache_key}")
    # print("=" * 60)

except Exception as e:
    print(f"\n❌ 操作失败：{str(e)}")
    # 常见错误提示（帮助你快速排查）
    if "Connection refused" in str(e):
        print("   ⚠️  提示：Redis服务未启动，请先启动Redis（命令：redis-server）")
    elif "NOAUTH Authentication required" in str(e):
        print("   ⚠️  提示：Redis需要密码，但settings.py的CACHES中未配置密码")
def delete_specific_cache(user_id):
    """
    删除指定用户的单词缓存
    :param user_id: 目标用户ID（如10000）
    """
    # 1. 明确要删除的完整缓存键
    target_cache_key = f"word_cache:{user_id}"
    print(f"📌 准备删除用户 {user_id} 的缓存，完整键：{target_cache_key}")

    try:
        # 方式A：用WordCacheManager的clear_cache()方法（推荐，适配你的缓存逻辑）
        cache_manager = WordCacheManager(user_id)
        cache_manager.clear_cache()  # 调用自带的清空方法（之前的代码中已实现）
        print(f"✅ 成功删除用户 {user_id} 的缓存（通过WordCacheManager）")

        # # 方式B：直接用Redis连接删除（备用，适用于无clear_cache方法的场景）
        # redis_conn = get_redis_connection("default")
        # # 先检查键是否存在
        # if redis_conn.exists(target_cache_key):
        #     redis_conn.delete(target_cache_key)
        #     print(f"✅ 成功删除缓存键：{target_cache_key}")
        # else:
        #     print(f"⚠️  缓存键 {target_cache_key} 不存在，无需删除")

    except Exception as e:
        print(f"❌ 删除失败：{str(e)}")
        if "Connection refused" in str(e):
            print("   ⚠️  提示：Redis服务未启动，请先启动Redis（命令：redis-server）")
        elif "NOAUTH Authentication required" in str(e):
            print("   ⚠️  提示：Redis需要密码，需在settings.py的CACHES中配置OPTIONS.PASSWORD")

#执行删除（替换为你要删除的用户ID，如10000）
if __name__ == "__main__":
    target_user_id = 10000  # 要删除缓存的用户ID
    delete_specific_cache(target_user_id)