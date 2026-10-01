# 🏛️ ديارنا الحديثة — الرخام والحجر الطبيعي

موقع متكامل لتجارة الرخام والحجر الطبيعي وتركيب الواجهات والأرضيات.

**التقنية:** Astro 5 (static) — سرعة تحميل عالية وتوليد صفحات ثابتة مثالية لمحركات البحث.

## البنية

```
src/
├── data/
│   ├── company.js        هوية الشركة: الاسم، الهاتف، التواصل، التصنيفات
│   └── products.js       كتالوج المنتجات (15 منتج) — مصدر الحقيقة الوحيد
├── components/
│   ├── ProductCard.astro   بطاقة المنتج في الشبكات
│   └── ProductImage.astro  صورة المنتج أو placeholder "تحت البحث عن صورة"
├── layouts/
│   └── Base.astro        الهيكل العام (هيدر/فوتر/SEO meta)
├── pages/
│   ├── index.astro          الرئيسية
│   ├── products/
│   │   ├── index.astro       إعادة توجيه لكل المنتجات
│   │   ├── [cat].astro       الكتالوج حسب النوع (مع فلترة المصدر)
│   │   └── [slug].astro      صفحة المنتج: مواصفات، مميزات، نصائح، FAQ، ذات صلة
│   ├── services.astro     خدمات التركيب
│   ├── about.astro        عن الشركة
│   ├── contact.astro      نموذج طلب عرض سعر (يتحول إلى واتساب — بلا خادم)
│   └── sitemap.xml.js     خريطة الموقع
└── styles/global.css     نظام التصميم (RTL، داكن، ذهبي)
```

## الأوامر

```bash
npm install       # تثبيت الحزم
npm run dev       # خادم التطوير (http://localhost:4321)
npm run build     # بناء الإنتاج إلى dist/
npm run preview   # معاينة البناء
```

## إضافة منتج

أضف عنصراً إلى `src/data/products.js`:

```js
{
  id: 'p016',
  slug: 'my-new-stone',        // يظهر في الرابط
  name: 'رخام ...',
  nameEn: 'English Name',
  category: 'marble',           // marble|granite|travertine|limestone
  origin: 'turkish',            // turkish|italian|omani|spanish|indian|egyptian
  image: null,                  // مسار الصورة أو null للـ placeholder
  code: 'غير محدد',
  color: '...',
  thickness: ['20 مم'],
  finish: ['مصقول (Polished)'],
  hardness: '3 – 5',
  uses: ['أرضيات'],
  excerpt: 'وصف قصير...',
  features: ['ميزة 1', 'ميزة 2'],
  tips: ['نصيحة 1'],
}
```

الصفحة تُولَّد تلقائياً عند `npm run build`.

## الصور

كل المنتجات حالياً تستخدم placeholder يحمل نص **«تحت البحث عن صورة»**.
لإضافة صورة: ضعها في `public/images/products/` واضبط الحقل `image` في المنتج:

```js
image: '/images/products/my-stone.jpg',
```

## النشر

الموقع static وجاهز للنشر على:
- GitHub Pages
- Cloudflare Pages
- Netlify
- أي استضافة تدعم ملفات ثابتة

بعد النشر حدّث `site` في `astro.config.mjs` إلى نطاقك النهائي.

## المعلومات

- الهاتف: 0536089153
- واتساب: 966536089153

## تنبيه

هذا المشروع تجريبي ويُنشر للمراجعة. الأسعار والمواصفات المتوقعة قابلة للتحديث من
`src/data/products.js` حسب مصادر الموردين.