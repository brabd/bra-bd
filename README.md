# ব্রা বাংলাদেশ (bra.bd)

বাংলা ভাষায় ব্রা ও ইনারওয়্যার বিষয়ক নিশ কনটেন্ট সাইট। স্ট্যাটিক HTML — GitHub → Vercel-এ সরাসরি ডিপ্লয়যোগ্য।

## স্ট্রাকচার
- `site/` — সম্পূর্ণ ওয়েবসাইট (Vercel-এ এই ফোল্ডারটাই root/output directory)
- `content/` — আর্টিকেল বডি (HTML) + `manifest.json` (টাইটেল/মেটা/FAQ)
- `build.py` — টেমপ্লেট থেকে সব পেজ জেনারেট করে
- `fetch_images.py` — Pexels API থেকে আর্টিকেল ইমেজ নামায়

## নতুন আর্টিকেল যোগ করা
1. `content/<slug>.html` ফাইলে আর্টিকেল বডি লিখুন (বিদ্যমান ফাইল দেখে ফরম্যাট নিন)
2. `content/manifest.json`-এ এন্ট্রি যোগ করুন (cat, slug, title, desc, excerpt, minutes, alt, faq_schema)
3. `python build.py` চালান — পেজ + sitemap অটো আপডেট হবে
4. ইমেজ: `site/images/articles/<cat>/<slug>.jpg`

## ডিপ্লয়মেন্ট (GitHub → Vercel)
1. এই ফোল্ডার GitHub রিপোতে পুশ করুন
2. Vercel-এ Import → Framework: **Other** → Output Directory: `site`
3. Domain সেটিংসে `bra.bd` যোগ করুন
4. লাইভ হওয়ার পর Google Search Console ও Bing Webmaster-এ sitemap সাবমিট করুন: `https://bra.bd/sitemap.xml`

## এডমিন প্যানেল
`/admin/` — অ্যাডস ম্যানেজার (ডামি/কাস্টম/AdSense, চালু-বন্ধ, ভিউ/ক্লিক/CTR), AdSense Publisher ID, Google Analytics, GSC/Bing ভেরিফিকেশন কোড, ট্রাফিক ওভারভিউ (৬ মাস) ও কনটেন্ট লিস্ট। সেটিংস localStorage-ভিত্তিক; robots.txt-এ `/admin/` ব্লক করা আছে।

## ইমেজ লাইসেন্স
সব ছবি Pexels থেকে (Pexels License — বাণিজ্যিক ব্যবহারে অনুমোদিত, অ্যাট্রিবিউশন ঐচ্ছিক)।
