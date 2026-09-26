import streamlit as st
from openai import OpenAI
import json

st.set_page_config(
    page_title="Alder Desk",
    page_icon="📦",
    layout="centered"
)

st.title("📦 Alder Desk")
st.subheader("مساعد طلبات موزعي مستحضرات التجميل")

st.write(
    "أدخل رسالة العميل، وسيحوّلها Alder Desk إلى مسودة طلب منظمة."
)

order_text = st.text_area(
    "📝 رسالة العميل",
    placeholder="مثال: محتاج 12 شامبو 400 مل و6 كريم و3 سيروم"
)

if st.button("🔄 تحويل إلى مسودة طلب"):
    if not order_text.strip():
        st.warning("من فضلك أدخل طلب العميل أولاً.")
        st.stop()

    try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

        response = client.responses.create(
            model="gpt-5-mini",
            input=[
                {
                    "role": "system",
                    "content": """
أنت مساعد مبيعات لموزعي مستحضرات التجميل.
حوّل رسالة العميل إلى قائمة طلب منظمة.
استخرج فقط:
product = اسم المنتج
sku = رقم المنتج إن وُجد، وإلا اتركه فارغاً
quantity = الكمية
unit = الوحدة

أعد النتيجة بصيغة JSON فقط.
"""
                },
                {
                    "role": "user",
                    "content": order_text
                }
            ]
        )

        result = json.loads(response.output_text)

        st.success("✅ تم إنشاء مسودة الطلب")

        st.json(result)

    except Exception as e:
        st.error("حدث خطأ أثناء تشغيل الذكاء الاصطناعي.")
        st.info(
            "سنقوم في الخطوة التالية بإعداد مفتاح OpenAI وربط Alder Desk بالذكاء الاصطناعي."
        )
