import streamlit as st
import pandas as pd
from recommender import load_catalog, recommend, baseline_recommend, demo_profiles, explain_match

st.set_page_config(page_title="Альфа Навигатор", page_icon="🧭", layout="wide")
st.title("🧭 Альфа Навигатор")
st.caption("Персональные рекомендации образовательных материалов для предпринимателей")

catalog = load_catalog()
profiles = demo_profiles()

with st.sidebar:
    st.header("Ваш бизнес-профиль")
    profile_name = st.selectbox("Быстрый пример", ["Свой профиль"] + list(profiles.keys()))
    preset = profiles.get(profile_name, {})
    stage = st.selectbox("Стадия бизнеса", ["Идея", "Запуск", "Первые продажи", "Развитие", "Масштабирование"],
                         index=["Идея", "Запуск", "Первые продажи", "Развитие", "Масштабирование"].index(preset.get("stage", "Развитие")))
    industry = st.selectbox("Сфера", ["Услуги", "Торговля", "Производство", "IT и digital", "Общепит", "Другое"],
                            index=["Услуги", "Торговля", "Производство", "IT и digital", "Общепит", "Другое"].index(preset.get("industry", "Услуги")))
    task = st.selectbox("Главная задача сейчас", ["Запустить бизнес", "Маркетинг и продвижение", "Продажи", "Финансы и учет", "Команда и процессы", "Юридические вопросы"],
                        index=["Запустить бизнес", "Маркетинг и продвижение", "Продажи", "Финансы и учет", "Команда и процессы", "Юридические вопросы"].index(preset.get("task", "Маркетинг и продвижение")))
    experience = st.selectbox("Опыт", ["Начинающий", "Есть опыт", "Опытный"], index=["Начинающий", "Есть опыт", "Опытный"].index(preset.get("experience", "Есть опыт")))
    history = st.multiselect("Темы просмотренных материалов (необязательно)",
                             ["Маркетинг и продвижение", "Продажи", "Финансы и учет", "Команда и процессы", "Юридические вопросы", "Запуск бизнеса"],
                             default=preset.get("history", []))
    show_baseline = st.toggle("Сравнить с обычной подборкой", value=True)

profile = {"stage": stage, "industry": industry, "task": task, "experience": experience, "history": history}
results = recommend(catalog, profile)
st.subheader("Подобрано для вас")
st.write("Подборка учитывает вашу задачу, стадию бизнеса, опыт и интересы. Чем выше совпадение, тем выше материал в списке.")

for _, row in results.head(5).iterrows():
    with st.container(border=True):
        c1, c2 = st.columns([4, 1])
        with c1:
            st.markdown(f"**{row['title']}**")
            st.caption(f"{row['topic']} · {row['format']} · {row['access']}")
            st.write(row["short_description"])
            st.write("**Почему рекомендуем:** " + explain_match(row, profile))
            st.write("**Следующий шаг:** " + row["next_step"])
        with c2:
            st.metric("Совпадение", f"{int(row['score'] * 100)}%")
            st.button("Открыть материал", key=f"open_{row['id']}", disabled=True,
                      help="В демо-данных нет реальных ссылок на материалы.")

if show_baseline:
    st.subheader("Проверка персонализации")
    left, right = st.columns(2)
    with left:
        st.markdown("**Персональная подборка**")
        st.dataframe(results[["title", "topic", "score"]].head(5), hide_index=True, use_container_width=True)
    with right:
        st.markdown("**Бейзлайн: совпадение только по теме**")
        base = baseline_recommend(catalog, profile)
        st.dataframe(base[["title", "topic", "score"]].head(5), hide_index=True, use_container_width=True)
    overlap = len(set(results.head(5)["id"]) & set(base.head(5)["id"]))
    st.info(f"Совпадение топ-5 подборок: {overlap}/5. Это демонстрационное сравнение на синтетическом каталоге, а не оценка бизнес-эффекта.")

with st.expander("Как работает система"):
    st.markdown("""
    1. Для каждого материала рассчитывается соответствие задаче, стадии бизнеса, сфере, опыту и истории интересов.
    2. Совпадения складываются с весами; затем применяется небольшой бонус за формат и доступность.
    3. Материалы сортируются по итоговому баллу.
    4. Объяснение формируется из факторов, которые повлияли на оценку.

    При отсутствии истории просмотров система продолжает работать: история — дополнительный сигнал, а не обязательное условие.
    """)
st.caption("Демо-прототип. Каталог и тестовые профили синтетические; перед внедрением загрузите согласованную выгрузку «Альфа-Курса».")
