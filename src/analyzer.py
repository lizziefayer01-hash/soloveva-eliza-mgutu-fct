"""
Анализатор урожайности пшеницы на основе математической модели
MVP версия для акселератора Leader.ID
"""


def predict_wheat_yield(soil_params, weather_data):
    """
    Прогнозирует урожайность пшеницы на основе математической модели

    Args:
        soil_params (dict): Параметры почвы
        weather_data (dict): Метеорологические данные

    Returns:
        float: Прогнозируемая урожайность (ц/га)
    """
    # Математическая модель из ВКР (упрощенная версия)
    a = 0.5  # Коэффициент для влажности почвы
    b = 0.3  # Коэффициент для температуры
    c = 0.2  # Коэффициент для NPK
    d = 15.0  # Базовый уровень урожайности

    soil_moisture = soil_params.get('moisture', 0.7)
    temperature = weather_data.get('avg_temperature', 20.0)
    npk = soil_params.get('npk_index', 0.6)

    yield_prediction = a * soil_moisture + b * temperature + c * npk + d

    return round(yield_prediction, 2)


def analyze_growth_stage(ndvi_value, days_after_sowing):
    """
    Анализирует стадию роста пшеницы

    Args:
        ndvi_value (float): Значение NDVI (0-1)
        days_after_sowing (int): Дней после посева

    Returns:
        dict: Информация о стадии роста
    """
    if ndvi_value < 0.3:
        stage = "Всходы"
        recommendation = "Проверить влажность почвы"
    elif ndvi_value < 0.6:
        stage = "Кущение"
        recommendation = "Внести азотные удобрения"
    elif ndvi_value < 0.8:
        stage = "Выход в трубку"
        recommendation = "Контроль влажности"
    else:
        stage = "Колошение"
        recommendation = "Подготовка к уборке"

    return {
        "growth_stage": stage,
        "ndvi": ndvi_value,
        "days": days_after_sowing,
        "health_status": "Хорошее" if ndvi_value > 0.5 else "Требует внимания",
        "recommendation": recommendation
    }


def optimize_fertilizer(soil_analysis, target_yield):
    """
    Оптимизация внесения удобрений

    Args:
        soil_analysis (dict): Анализ почвы
        target_yield (float): Целевая урожайность

    Returns:
        dict: Рекомендации по удобрениям
    """
    n_base = soil_analysis.get('nitrogen', 0)
    p_base = soil_analysis.get('phosphorus', 0)
    k_base = soil_analysis.get('potassium', 0)

    n_deficit = max(0, target_yield * 0.03 - n_base)
    p_deficit = max(0, target_yield * 0.01 - p_base)
    k_deficit = max(0, target_yield * 0.02 - k_base)

    return {
        "nitrogen_kg_ha": round(n_deficit, 1),
        "phosphorus_kg_ha": round(p_deficit, 1),
        "potassium_kg_ha": round(k_deficit, 1),
        "total_fertilizer": round(n_deficit + p_deficit + k_deficit, 1),
        "model_version": "1.0"
    }


if __name__ == "__main__":
    soil_data = {'moisture': 0.75, 'npk_index': 0.65}
    weather_data = {'avg_temperature': 22.5, 'precipitation': 350}

    yield_pred = predict_wheat_yield(soil_data, weather_data)
    print(f"Прогнозируемая урожайность: {yield_pred} ц/га")

    growth_info = analyze_growth_stage(0.72, 45)
    print(f"Стадия роста: {growth_info['growth_stage']}")
