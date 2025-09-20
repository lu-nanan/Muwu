# 项目根目录/celery.py（如 MarkFlow/celery.py）
import os
from celery import Celery
from celery.schedules import crontab

# 加载Django环境变量（必须在创建Celery实例前）
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MarkFlow.settings')  # 替换为你的项目settings路径

# 创建Celery实例（项目名+消息代理地址）
app = Celery('MarkFlow')  # 项目名自定义，与项目保持一致

# 从Django settings中读取Celery配置（后续在settings.py中配置）
app.config_from_object('django.conf:settings', namespace='CELERY')

# 自动发现所有Django应用中的tasks.py文件（任务定义文件）
app.autodiscover_tasks()

# 配置定时任务（核心：同步缓存到数据库的定时规则，可自定义时间）
app.conf.beat_schedule = {
    # 任务名：自定义，用于标识任务
    'sync-cache-to-db-every-30-minutes': {
        'task': 'MarkFlowImpl.tasks.sync_cache_to_db',  # 任务路径（应用名.tasks.任务函数名）
        'schedule': crontab(minute='*/30'),  # 定时频率：每30分钟执行一次（可调整）
        # 'schedule': timedelta(minutes=10),  # 也支持按时间间隔（如每10分钟）
        'args': (),  # 任务无参数，留空
    },
}


def shared_task():
    return None