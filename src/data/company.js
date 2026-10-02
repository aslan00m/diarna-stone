// هوية الشركة — بيانات مركزية تُستخدم في كل الصفحات
export const COMPANY = {
  name: 'شركة ديارنا الحديثة',
  tagline: 'تجارة الرخام والحجر الطبيعي وتركيب الواجهات والأرضيات',
  phone: '0536089153',
  whatsapp: '966536089153',
  email: 'info@diarna.sa',
  city: 'الرياض، المملكة العربية السعودية',
  hours: 'السبت – الخميس: 8 صباحاً – 6 مساءً',
  description:
    'شركة ديارنا الحديثة لتجارة الرخام والحجر الطبيعي وتركيب الواجهات والأرضيات في المملكة العربية السعودية. نوفر مجموعة مختارة من الرخام والجرانيت والترافرتينو من أفضل المصادر العالمية.',
};

// روابط التواصل
export const LINKS = {
  phone: `tel:+${COMPANY.phone}`,
  whatsappNumber: COMPANY.whatsapp,
  whatsapp: `https://wa.me/${COMPANY.whatsapp}?text=${encodeURIComponent('مرحباً، أود الاستفسار عن أسعار الحجر')}`,
};

// التصنيف حسب النوع (نفس هيكل حجر الدار)
export const CATEGORIES = [
  { slug: 'marble', name: 'رخام', icon: '▦' },
  { slug: 'granite', name: 'جرانيت', icon: '◈' },
  { slug: 'travertine', name: 'ترافنتينو', icon: '▤' },
  { slug: 'limestone', name: 'حجر جيري', icon: '▨' },
  { slug: 'sinks', name: 'المغاسل', icon: '◐' },
];

// التصنيف حسب المصدر
export const ORIGINS = [
  { slug: 'turkish', name: 'تركي', flag: '🇹🇷' },
  { slug: 'italian', name: 'إيطالي', flag: '🇮🇹' },
  { slug: 'omani', name: 'عماني', flag: '🇴🇲' },
  { slug: 'spanish', name: 'إسباني', flag: '🇪🇸' },
  { slug: 'indian', name: 'هندي', flag: '🇮🇳' },
  { slug: 'egyptian', name: 'مصري', flag: '🇪🇬' },
  { slug: 'brazilian', name: 'برازيلي', flag: '🇧🇷' },
  { slug: 'chinese', name: 'صيني', flag: '🇨🇳' },
  { slug: 'greek', name: 'يوناني', flag: '🇬🇷' },
  { slug: 'portuguese', name: 'برتغالي', flag: '🇵🇹' },
];

// استخدامات شائعة
export const USES = [
  'أرضيات',
  'جدران',
  'واجهات',
  'أسوار',
  'سطوح طاولات',
  'أرضيات حمامات',
  'جدران حمامات',
  'مغاسل',
  'درج',
  'مداخل',
];