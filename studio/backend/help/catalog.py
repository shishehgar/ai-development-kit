"""Persian contextual help catalog for AIDK Studio."""

from __future__ import annotations

HELP_CATALOG: dict[str, dict[str, str]] = {
    "version": {
        "title_fa": "نسخه",
        "description_fa": "نمایش نسخه نصب‌شده AIDK.",
        "category": "system",
        "safety": "read-only",
    },
    "doctor": {
        "title_fa": "بررسی سلامت",
        "description_fa": (
            "بررسی نصب، محیط پایتون، وابستگی‌ها و ابزارهای موردنیاز."
        ),
        "category": "system",
        "safety": "read-only",
    },
    "workspace": {
        "title_fa": "تحلیل فضای کاری",
        "description_fa": (
            "شناسایی ساختار پروژه، فایل‌های اصلی، فناوری‌ها و نقاط ورود."
        ),
        "category": "project",
        "safety": "read-only",
    },
    "git": {
        "title_fa": "وضعیت Git",
        "description_fa": (
            "نمایش مخزن، شاخه فعال، Remote، آخرین Commit و وضعیت فایل‌ها."
        ),
        "category": "git",
        "safety": "read-only",
    },
    "git-report": {
        "title_fa": "گزارش Git",
        "description_fa": "تولید گزارش ساختاریافته از وضعیت مخزن Git.",
        "category": "git",
        "safety": "read-only",
    },
    "audit": {
        "title_fa": "ممیزی مهندسی",
        "description_fa": (
            "تحلیل کیفیت، ساختار، تنظیمات و ریسک‌های مهندسی پروژه."
        ),
        "category": "quality",
        "safety": "read-only",
    },
    "dashboard": {
        "title_fa": "داشبورد پروژه",
        "description_fa": "نمایش خلاصه وضعیت و شاخص‌های اصلی پروژه.",
        "category": "project",
        "safety": "read-only",
    },
    "improve": {
        "title_fa": "برنامه بهبود",
        "description_fa": (
            "تهیه فهرست اولویت‌بندی‌شده پیشنهادهای بهبود پروژه."
        ),
        "category": "quality",
        "safety": "read-only",
    },
    "fix": {
        "title_fa": "مرکز اصلاح",
        "description_fa": (
            "تهیه یا اعمال اصلاحات پروژه پس از نمایش تغییر و تأیید کاربر."
        ),
        "category": "changes",
        "safety": "confirmation-required",
    },
    "scan": {
        "title_fa": "اسکن پروژه",
        "description_fa": (
            "اسکن پروژه و ثبت اطلاعات آن در پایگاه داده AIDK."
        ),
        "category": "database",
        "safety": "writes-database",
    },
    "db": {
        "title_fa": "پایگاه داده",
        "description_fa": "مدیریت داده‌ها و سوابق ذخیره‌شده پروژه‌ها.",
        "category": "database",
        "safety": "confirmation-required",
    },
    "deps": {
        "title_fa": "وابستگی‌ها",
        "description_fa": "شناسایی و تحلیل وابستگی‌های نرم‌افزاری پروژه.",
        "category": "dependencies",
        "safety": "read-only",
    },
    "deps-db": {
        "title_fa": "سوابق وابستگی‌ها",
        "description_fa": (
            "مشاهده اطلاعات وابستگی‌های ثبت‌شده در پایگاه داده."
        ),
        "category": "dependencies",
        "safety": "read-only",
    },
    "deps-check": {
        "title_fa": "سلامت وابستگی‌ها",
        "description_fa": (
            "بررسی سازگاری، بازتولیدپذیری و سلامت وابستگی‌ها."
        ),
        "category": "dependencies",
        "safety": "read-only",
    },
    "deps-lock": {
        "title_fa": "قفل وابستگی‌ها",
        "description_fa": "بررسی وجود و اعتبار Lockfileهای پروژه.",
        "category": "dependencies",
        "safety": "read-only",
    },
    "deps-licenses": {
        "title_fa": "مجوز وابستگی‌ها",
        "description_fa": "بررسی مجوزهای حقوقی بسته‌های نرم‌افزاری.",
        "category": "dependencies",
        "safety": "read-only",
    },
}
