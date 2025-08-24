from handlers.main_menu import router as main_menu_router
from handlers.registration import router as registration_router
from handlers.applications import router as applications_router
from handlers.admin.stats import router as admin_router
from handlers.admin.mailing import router as admin_mailing_router


routers = [
    registration_router,
    main_menu_router,
    applications_router,
    admin_router,
    admin_mailing_router
]
