# Google Search Console API — dyarnaa.com

نظام فهرسة آلي ومجاني لفحص حالة فهرسة موقع `dyarnaa.com` على Google.

## ما لا يفعله هذا النظام

- **لا يستخدم Google Indexing API** لفهرسة صفحات الخدمات أو المنتجات أو المقالات.
- **لا يطلب فهرسة فورية** — الفحص فقط.
- **لا يحتاج اشتراكات مدفوعة** — يستخدم الواجهات الرسمية المجانية من Google.

## الهيكل

```
scripts/
  search_console/
    __init__.py           — حزمة الوحدة
    auth.py               — مصادقة Service Account
    sites_api.py          — واجهة Sites API (قائمة الخصائص، التحقق من الملكية)
    inspect_urls.py       — URL Inspection API (فحص حالة الفهرسة)
    sitemap_manager.py    — Sitemaps API (إرسال/فحص حالة خريطة الموقع)
    search_analytics.py   — Search Analytics API (أداء البحث)
    report.py             — إنشاء تقارير JSON + Markdown
    audit_site.py         — المدير الرئيسي: ينسق جميع الوحدات
    config.example.json   — نموذج إعداد (لا يحتوي أسرار)

scripts/
  indexing_monitor.py     — مراقب يومي مستقل (يعمل بدون GSC API)
  seo_audit.py            — مدقق SEO شامل

/opt/data/scripts/
  dyarnaa-index-monitor.sh — سكربت تشغيل للمراقبة اليومية
```

## الاستخدام

### المراقبة اليومية (لا يحتاج GSC credentials)
```bash
# ملخص فقط
python3 scripts/indexing_monitor.py --summary

# مع تفاصيل كل URL
python3 scripts/indexing_monitor.py

# مع فحص GSC API (إذا توفرت الاعتماديات)
python3 scripts/indexing_monitor.py --inspect 50
```

### مدقق SEO الشامل
```bash
python3 scripts/seo_audit.py
python3 scripts/seo_audit.py --max-urls 20
```

### تدقيق كامل مع GSC API (يتطلب credentials)
```bash
# تدقيق محلي فقط (بدون GSC)
python3 -m search_console.audit_site --summary

# مع URL Inspection API
python3 -m search_console.audit_site --inspect 20

# مع إرسال Sitemap إلى GSC
python3 -m search_console.audit_site --submit

# مع تحليل أداء البحث
python3 -m search_console.audit_site --analytics
```

## إعداد Google Search Console API

اتبع التعليمات في `SETUP_GSC.md` أو:

1. أنشئ **Service Account** في Google Cloud Console
2. فعّل **Search Console API**
3. نزّل مفتاح JSON
4. خزّنه في `/opt/data/secrets/gsc-service-account.json` أو اضبط متغير `GSC_SERVICE_ACCOUNT`
5. امنح الحساب صلاحية على الخاصية في Google Search Console

## المهام المجدولة

| المهمة | الجدولة | الحالة |
|--------|---------|--------|
| Dyarnaa Google Indexing Monitor | يومياً 09:00 UTC | نشطة |
| Diarna Pipeline Morning | يومياً 09:00 UTC | متوقفة |
| Diarna Pipeline Publish | يومياً 10:00 UTC | متوقفة |
| مقالات عامة (4 جوبات) | 01/10/16/19 KSA | نشطة |
| سوشيال (6 جوبات) | 05/07:30/10/12:30/15/17:30 KSA | نشطة |

## التقارير

```
reports/indexing/    — تقارير المراقبة اليومية
reports/seo_audit/   — تقارير فحص SEO
```

كل تشغيل يُنتج:
- `report-<timestamp>.json` — تقرير كامل بتوقيت
- `latest.json` — آخر تقرير (للمقارنة التلقائية)

## النسخ الاحتياطي

قبل أي تعديل:
```bash
# أنشئ نسخة احتياطية يدوياً
cp src/pages/sitemap.xml.js /opt/data/cache/sitemap-backup.xml.js
```

## ملاحظات

- الفحص المحلي يعمل دائماً حتى بدون credentials
- GSC API يعتمد على حصص Google (URL Inspection: ~600 req/day)
- لا يُطلب فهرسة آلي — فقط فحص
- آخر فحص: 254 URL، 200 OK للكل، 0 تكرارات في Sitemap
