import os
import requests
from datetime import datetime
import anthropic

TELEGRAM_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]
ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY"]

def build_prompt():
    today = datetime.now().strftime("%A، %d %B %Y")
    return f"""أنت خبير متخصص في أسواق الخضروات والفواكه الدولية مع تركيز على التصدير إلى السويد.

أنشئ تقريراً يومياً احترافياً ومختصراً بعنوان:
"تقرير يومي تنافسي – تصدير خضار وفواكه إلى مالمو (السويد)"
التاريخ: {today} | الساعة: 19:00 CEST

سعر الصرف: قدّر سعر اليوم (1 € ≈ X SEK).
المنتجات: طماطم، فلفل حلو، خيار، بطيخ أحمر seedless.
الشحن: Reefer FTL door-to-door إلى مالمو. مناولة 0.05 €/كجم. لا جمارك.

الهيكل (موجز مناسب لتلغرام):

1⃣ أسعار الجملة اليوم (€/كجم)
جدول نصي: المغرب | إسبانيا | هولندا

2⃣ تكاليف الشحن إلى مالمو
تكلفة €/كجم + وقت التسليم لكل مصدر

3⃣ Landed Cost + هامش الربح
جدول مختصر لكل منتج ومصدر

4⃣ أبرز توصية اليوم
جملتان: أفضل منتج + أفضل مصدر + السبب

5⃣ تنبيه السوق
أي نقص أو فرصة أو خطر مستجد اليوم

الأسلوب: موجز، جداول ASCII بسيطة، أرقام واضحة، ≤600 كلمة.
"""

def generate_report():
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    message = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=2048,
        messages=[{"role": "user", "content": build_prompt()}]
    )
    return message.content[0].text

def send_to_telegram(text: str):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    chunks = [text[i:i+4000] for i in range(0, len(text), 4000)]
    for chunk in chunks:
        payload = {"chat_id": TELEGRAM_CHAT_ID, "text": chunk, "parse_mode": "Markdown"}
        resp = requests.post(url, json=payload, timeout=30)
        resp.raise_for_status()
    print(f"✅ أُرسل التقرير ({len(chunks)} جزء) بنجاح.")

if __name__ == "__main__":
    print("⏳ جاري توليد التقرير...")
    report_text = generate_report()
    print("📤 جاري الإرسال...")
    send_to_telegram(report_text)
