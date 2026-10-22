<!--
  DEVELOPER ARCHITECTURE NOTE:
  MODULE:    Grand Public Production Launch & System Handover
  TOPIC:     Phase 141 SEO, 64-District OpenGraph Engine, Production CI/CD & National Handover
  FILE:      DEPLOYMENT_HANDBOOK.md
  PHASE:     Phase 141 - Grand Public Production Launch & Final Handover
  PURPOSE:   Master production deployment, operations, and incident runbook handbook (Bilingual)
  STANDARDS: Zero-Emoji, Zero-IDOR, Production Grade, WCAG 2.2 AAA, Full 64-District Support
-->

# Student Life Circle (অগ্রযাত্রা) — Master Production Deployment & Operations Handbook

---

## ১. প্ল্যাটফর্ম আর্কিটেকচার ওভারভিউ (System Architecture Overview)

Student Life Circle (অগ্রযাত্রা) একটি আধুনিক, উচ্চ-ক্ষমতাসম্পন্ন এবং দুর্যোগ-সহনশীল জাতীয় শিক্ষা প্ল্যাটফর্ম। এটি বাংলাদেশের প্রাথমিক থেকে শুরু করে এসএসসি, এইচএসসি, বিশ্ববিদ্যালয় ভর্তি এবং বিসিএস/ক্যারিয়ার পর্যায় পর্যন্ত সম্পূর্ণ শিক্ষা জীবনচক্রকে সেবা প্রদান করে।

```
                       [ Cloudflare CDN & DDoS Shield ]
                                      │
                         [ Nginx Reverse Proxy (TLS 1.3) ]
                                      │
            ┌─────────────────────────┴─────────────────────────┐
            ▼                                                   ▼
[ Next.js 15 Standalone Cluster ]                   [ FastAPI Python Async Core ]
(React 19, TypeScript, PWA Engine)                  (Payment Core, Psychometrics, NLP)
            │                                                   │
            ├─────────────────────────┬─────────────────────────┤
            ▼                         ▼                         ▼
   [ PostgreSQL 16+ ]           [ Redis 7+ Cache ]     [ Bangladeshi Gateways ]
(ACID, pgvector, RLS)      (Idempotency, Timers)     (bKash, Nagad, SSLCommerz)
```

### প্রধান প্রযুক্তি উপাদানসমূহ:
1. **ওয়েব ফ্রন্টএন্ড**: Next.js 15.5+ (Pages Router, React 19, TypeScript, Tailwind CSS, Lucide SVG Icons, PWA Offline Service Worker)।
2. **ব্যাকএন্ড API কোর**: Python 3.12+ FastAPI (Asyncpg, Pydantic v2, HMAC-SHA256 সিগনেচার ভ্যালিডেশন, OWASP ASVS Level 2)।
3. **পেমেন্ট ও এসক্রো**: সার্ভার-অথরিটেটিভ বিকাশ, নগদ এবং এসএসএলকমার্জ কার্ড পেমেন্ট; ২৪ ঘণ্টার অটো-রিলিজ ডিজিটাল এসক্রো এবং স্বয়ংক্রিয় ঘণ্টায় ঘণ্টায় রিকনসিলিয়েশন।
4. **অফলাইন রেজিলিয়েন্স**: Workbox PWA সার্ভিস ওয়ার্কার, IndexedDB বোর্ড প্রশ্ন আর্কাইভ এবং লো-ব্যান্ডউইথ SMS/LoRa দুর্যোগ ব্রিজিং।

---

## ২. প্রোডাকশন সার্ভার সেটআপ গাইড (Production Server Setup Guide)

### পূর্বশর্ত (Prerequisites):
- Ubuntu 22.04 LTS অথবা 24.04 LTS 64-bit সার্ভার (ন্যূনতম 4 vCPU, 8GB RAM, 80GB NVMe SSD)।
- Node.js 20.x LTS ও npm 10+।
- Python 3.12+ ও pip।
- PostgreSQL 16+ এবং Redis 7+।
- Nginx এবং Certbot (Let's Encrypt)।

### ধাপ ১: রিপোজিটরি ক্লোন ও কনফিগারেশন
```bash
git clone https://github.com/organization/student-life-circle.git /var/www/studentlifecircle
cd /var/www/studentlifecircle

# প্রোডাকশন এনভায়রনমেন্ট কনফিগারেশন কপি করুন
cp .env.production.example .env
chmod 600 .env
```

### ধাপ ২: ফ্রন্টএন্ড ডিপেন্ডেন্সি ও বিল্ড
```bash
cd /var/www/studentlifecircle/frontend
npm ci
npm run build

# Standalone অ্যাসেট সিনক্রোনাইজেশন
cp -r public .next/standalone/
cp -r .next/static .next/standalone/.next/
```

### ধাপ ৩: ব্যাকএন্ড ডিপেন্ডেন্সি ও টেস্ট ভেরিফিকেশন
```bash
cd /var/www/studentlifecircle
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# সম্পূর্ণ টেস্ট স্যুট রান করে যাচাই করুন
python3 -m unittest discover -s backend/tests -p "test_*.py"
```

### ধাপ ৪: Nginx ও SSL সক্রিয়করণ
```bash
sudo cp nginx/studentlifecircle.conf /etc/nginx/sites-available/studentlifecircle.conf
sudo ln -s /etc/nginx/sites-available/studentlifecircle.conf /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx

# Let's Encrypt SSL সার্টিফিকেট ইস্যু
sudo certbot --nginx -d studentlifecircle.com -d www.studentlifecircle.com
```

---

## ৩. গুরুত্বপূর্ণ এনভায়রনমেন্ট ভেরিয়েবল রেফারেন্স (Environment Variables)

| ভেরিয়েবল নাম | প্রয়োজনীয়তা | উদ্দেশ্য ও বিবরণ |
| :--- | :---: | :--- |
| `NODE_ENV` | বাধ্যতামূলক | `production` সেট করুন |
| `PAYMENT_MODE` | বাধ্যতামূলক | লাইভ ট্রানজ্যাকশনের জন্য `live`, টেস্টের জন্য `sandbox` |
| `DATABASE_URL` | বাধ্যতামূলক | প্রোডাকশন PostgreSQL কানেকশন স্ট্রিং |
| `REDIS_URL` | বাধ্যতামূলক | ইন-মেমোরি ক্যাশ ও সেশন ব্রোকার URL |
| `BKASH_APP_KEY` | পেমেন্ট | বিকাশ মার্চেন্ট পোর্টাল থেকে প্রাপ্ত প্রোডাকশন অ্যাপ কি |
| `BKASH_APP_SECRET` | পেমেন্ট | বিকাশ মার্চেন্ট প্রোডাকশন অ্যাপ সিক্রেট |
| `NAGAD_MERCHANT_ID` | পেমেন্ট | নগদ কর্তৃক অনুমোদিত মার্চেন্ট আইডি |
| `SSLC_STORE_ID` | পেমেন্ট | এসএসএলকমার্জ অনুমোদিত লাইভ স্টোর আইডি |
| `SSLC_STORE_PASSWD`| পেমেন্ট | এসএসএলকমার্জ স্টোর পাসওয়ার্ড (সিগনেচার যাচাইয়ের জন্য) |
| `JWT_SECRET` | সিকিউরিটি | টোকেন সাইনিংয়ের জন্য শক্তিশালী ৬৪-অক্ষরের র‍্যান্ডম হেক্স কি |

---

## ৪. সাধারণ জরুরি পরিস্থিতি ও রানবুক (Incident Runbooks)

### রানবুক ১: জাতীয় বোর্ড পরীক্ষার ফল প্রকাশের সময় ট্রাফিক বৃদ্ধি (Traffic Spike Surge)
- **লক্ষণ**: সার্ভারের CPU ব্যবহার $\ge 85\%$, রেসপন্স টাইম বৃদ্ধি।
- **সমাধান**:
  1. Nginx ক্যাশিং ভ্যালিডিটি বৃদ্ধি করুন এবং স্ট্যাটিক অ্যাসেট সরাসরি ক্লাউডফ্লেয়ার এজ থেকে সার্ভ করার নির্দেশ দিন।
  2. স্ট্যান্ডঅ্যালোন নোড ক্লাস্টারের ওয়ার্কার সংখ্যা বৃদ্ধি করুন:
     ```bash
     pm2 scale studentlifecircle-frontend +4
     ```
  3. ডাটাবেজ কানেকশন পুল পর্যবেক্ষণ করুন এবং ভারী নন-এসেনশিয়াল রিপোর্ট সাময়িকভাবে ডিফার করুন।

### রানবুক ২: পেমেন্ট গেটওয়ে টাইমআউট বা অসম্পূর্ণ ট্রানজ্যাকশন (Gateway Discrepancy)
- **লক্ষণ**: শিক্ষার্থী টাকা পরিশোধ করেছেন কিন্তু কোর্স আনলক হয়নি বা গেটওয়ে IPN পাঠাতে দেরি করেছে।
- **সমাধান**:
  1. স্বয়ংক্রিয় ঘণ্টায় ঘণ্টায় রিকনসিলিয়েশন জব চালু আছে কি না তা যাচাই করুন:
     ```bash
     curl -X POST http://localhost:8000/api/v1/payments/reconciliation/run
     ```
  2. নির্দিষ্ট ট্রানজ্যাকশন আইডির লাইভ স্ট্যাটাস কুয়েরি করুন:
     ```bash
     curl http://localhost:8000/api/v1/payments/bkash/query/{payment_id}
     ```
  3. সার্ভার স্বয়ংক্রিয়ভাবে অডিট লেজারে রেকর্ড সিঙ্ক করে ডিজিটাল এসক্রো আপডেট করবে।

### রানবুক ৩: তাৎক্ষণিক রোলব্যাক পদ্ধতি (Sub-30-Second Rollback Procedure)
- **লক্ষণ**: নতুন ডেপ্লয়মেন্টের পর কোনো অপ্রত্যাশিত ক্র্যাশ বা গুরুতর ত্রুটি দেখা দিলে।
- **সমাধান**:
  ```bash
  cd /var/www/studentlifecircle
  bash scripts/rollback.sh previous
  ```
  স্ক্রিপ্টটি স্বয়ংক্রিয়ভাবে পূর্ববর্তী ভেরিফাইড রিলিজ ট্যাগ চেকআউট করবে, বিল্ড অ্যাসেট সিঙ্ক করবে, সার্ভিস রিস্টার্ট করবে এবং হেলথ চেক নিশ্চিত করবে।

---

## ৫. রক্ষণাবেক্ষণ ও ভবিষ্যৎ সম্প্রসারণ (Maintenance & Extension Guide)

1. **ডাটাবেজ ব্যাকআপ**: প্রতিদিন রাত ২টায় `scripts/backup_database.sh` ক্রনজব আকারে চালনা করুন:
   ```bash
   0 2 * * * /bin/bash /var/www/studentlifecircle/scripts/backup_database.sh >> /var/log/slc_backup.log 2>&1
   ```
2. **নতুন পরিভাষা যুক্তকরণ (NCTB Lexicon)**: `backend/curriculum/lexicon_service.py`-তে নতুন টার্ম যোগ করে ইউনিট টেস্ট রান করুন।
3. **৬৪ জেলার কনটেন্ট কাস্টমাইজেশন**: `frontend/src/lib/districts.ts`-এ জেলাভিত্তিক শিক্ষার্থী পরিসংখ্যান বা নতুন ফোকাস স্ট্রিম আপডেট করুন।
