from recommender import load_catalog, recommend, baseline_recommend, demo_profiles

def test_recommendations_are_sorted():
    catalog = load_catalog()
    profile = demo_profiles()["Начинающий предприниматель"]
    result = recommend(catalog, profile)
    assert len(result) == len(catalog)
    assert result.iloc[0]["score"] >= result.iloc[-1]["score"]

def test_cold_start_returns_results():
    catalog = load_catalog()
    profile = {"stage": "Идея", "industry": "Другое", "task": "Запустить бизнес",
               "experience": "Начинающий", "history": []}
    assert not recommend(catalog, profile).empty

def test_baseline_exists():
    result = baseline_recommend(load_catalog(), demo_profiles()["Владелец магазина"])
    assert "score" in result.columns
