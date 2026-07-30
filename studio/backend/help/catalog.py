"""Persian help catalog for AIDK commands."""

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
        "description_fa": "بررسی نصب، محیط پایتون و ابزارهای موردنیاز.",
        "category": "system",
        "safety": "read-only",
    },
    "workspace": {
        "title_fa": "تحلیل فضای کاری",
        "description_fa": "شناسایی ساختار، فناوری‌ها و فایل‌های اصلی پروژه.",
        "category": "project",
        "safety": "read-only",
    },
    "git": {
        "title_fa": "وضعیت گیت",
        "description_fa": "نمایش شاخه، ریموت، کامیت‌ها و وضعیت فایل‌ها.",
        "category": "git",
        "safety": "read-only",
    },
    "git-report": {
        "title_fa": "گزارش گیت",
        "description_fa": "تولید گزارش ساختاریافته از مخزن گیت.",
        "category": "git",
        "safety": "read-only",
    },
    "audit": {
        "title_fa": "ممیزی مهندسی",
        "description_fa": "بررسی کیفیت، ساختار، تنظیمات و ریسک‌های پروژه.",
        "category": "quality",
        "safety": "read-only",
    },
    "dashboard": {
        "title_fa": "داشبورد پروژه",
        "description_fa": "نمایش خلاصه سلامت و وضعیت عمومی پروژه.",
        "category": "project",
        "safety": "read-only",
    },
    "improve": {
        "title_fa": "برنامه بهبود",
        "description_fa": "تهیه پیشنهادهای اولویت‌بندی‌شده برای بهبود پروژه.",
        "category": "quality",
        "safety": "read-only",
    },
    "fix": {
        "title_fa": "مرکز اصلاح",
        "description_fa": "آماده‌سازی و اعمال اصلاحات پس از تأیید کاربر.",
        "category": "changes",
        "safety": "confirmation-required",
    },
    "scan": {
        "title_fa": "اسکن پروژه",
        "description_fa": "اسکن پروژه و ثبت نتایج در پایگاه داده.",
        "category": "database",
        "safety": "writes-database",
    },
    "db": {
        "title_fa": "پایگاه داده",
        "description_fa": "مدیریت سوابق و داده‌های ثبت‌شده پروژه‌ها.",
        "category": "database",
        "safety": "confirmation-required",
    },
    "deps": {
        "title_fa": "وابستگی‌ها",
        "description_fa": "شناسایی و تحلیل وابستگی‌های نرم‌افزاری.",
        "category": "dependencies",
        "safety": "read-only",
    },
    "deps-db": {
        "title_fa": "سوابق وابستگی‌ها",
        "description_fa": "مشاهده اطلاعات وابستگی‌های ثبت‌شده.",
        "category": "dependencies",
        "safety": "read-only",
    },
    "deps-check": {
        "title_fa": "سلامت وابستگی‌ها",
        "description_fa": "بررسی سازگاری و سلامت وابستگی‌ها.",
        "category": "dependencies",
        "safety": "read-only",
    },
    "deps-lock": {
        "title_fa": "قفل وابستگی‌ها",
        "description_fa": "بررسی Lockfile و بازتولیدپذیری محیط.",
        "category": "dependencies",
        "safety": "read-only",
    },
    "deps-licenses": {
        "title_fa": "مجوز وابستگی‌ها",
        "description_fa": "بررسی مجوزهای بسته‌های نرم‌افزاری.",
        "category": "dependencies",
        "safety": "read-only",
    },
}
