from pathlib import Path
import pandas as pd

DATA_PATH = Path(__file__).parent / "data" / "materials.csv"

def load_catalog():
    return pd.read_csv(DATA_PATH).fillna("")

def demo_profiles():
    return {
        "Начинающий предприниматель": {
            "stage": "Идея", "industry": "Услуги", "task": "Запустить бизнес",
            "experience": "Начинающий", "history": []
        },
        "Владелец магазина": {
            "stage": "Первые продажи", "industry": "Торговля", "task": "Маркетинг и продвижение",
            "experience": "Есть опыт", "history": ["Продажи"]
        },
        "Соло-фаундер": {
            "stage": "Развитие", "industry": "IT и digital", "task": "Команда и процессы",
            "experience": "Опытный", "history": ["Маркетинг и продвижение", "Продажи"]
        },
    }

def _score(row, profile, personalized=True):
    if not personalized:
        return 1.0 if row["topic"] == profile["task"] else 0.0
    score = 0.0
    reasons = []
    if row["topic"] == profile["task"]:
        score += 0.42
    if profile["stage"] in str(row["stages"]).split(";"):
        score += 0.22
    if profile["industry"] in str(row["industries"]).split(";") or "Все" in str(row["industries"]).split(";"):
        score += 0.12
    if profile["experience"] in str(row["levels"]).split(";") or "Любой" in str(row["levels"]).split(";"):
        score += 0.10
    if row["topic"] in profile.get("history", []):
        score += 0.08
    if row["access"] == "Бесплатный":
        score += 0.04
    return min(score, 1.0)

def recommend(catalog, profile):
    result = catalog.copy()
    result["score"] = result.apply(lambda row: _score(row, profile), axis=1)
    return result.sort_values(["score", "title"], ascending=[False, True]).reset_index(drop=True)

def baseline_recommend(catalog, profile):
    result = catalog.copy()
    result["score"] = result.apply(lambda row: _score(row, profile, personalized=False), axis=1)
    return result.sort_values(["score", "title"], ascending=[False, True]).reset_index(drop=True)

def explain_match(row, profile):
    reasons = []
    if row["topic"] == profile["task"]:
        reasons.append("тема совпадает с вашей текущей задачей")
    if profile["stage"] in str(row["stages"]).split(";"):
        reasons.append("материал подходит для вашей стадии бизнеса")
    if profile["industry"] in str(row["industries"]).split(";") or "Все" in str(row["industries"]).split(";"):
        reasons.append("учтена ваша сфера")
    if profile["experience"] in str(row["levels"]).split(";") or "Любой" in str(row["levels"]).split(";"):
        reasons.append("подходит ваш уровень опыта")
    if row["topic"] in profile.get("history", []):
        reasons.append("учтен ваш интерес к теме")
    return "; ".join(reasons) if reasons else "это полезный вводный материал для расширения кругозора"
