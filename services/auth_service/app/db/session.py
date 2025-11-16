# نستورد المحرك async من SQLAlchemy
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

# هذا المسار يحتوي على URL الاتصال بقاعدة البيانات (PostgreSQL, MySQL, ...)
from shared.db.database import DATABASE_URL


# --------------------------------------------------------
# 1) إنشاء محرك اتصال Asynchronous Engine
# --------------------------------------------------------
# create_async_engine:
#  - ينشئ اتصال Async لقاعدة البيانات
#  - لا يوقف الـ event loop (أسرع و scalable)
#  - echo=False يعني لا يطبع كل SQL Query
engine = create_async_engine(DATABASE_URL, echo=False)


# --------------------------------------------------------
# 2) إنشاء Session factory (غير متزامنة)
# --------------------------------------------------------
# async_sessionmaker:
#  - ينشئ جلسة DB لجلب البيانات بطريقة async
#  - expire_on_commit=False يعني لا يعيد تحميل البيانات بعد commit
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False
)


# --------------------------------------------------------
# 3) Dependency Injection للـ FastAPI
# --------------------------------------------------------
# get_db():
#   - لكل طلب API → يتم فتح session جديدة
#   - بعد انتهاء الطلب → session تُغلق تلقائياً
#   - async with → طريقة آمنة للتعامل مع الموارد داخل async
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
