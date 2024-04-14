import transformers


class PhiWrapper:
    def __init__(self):
        self.model_id = "microsoft/phi-2"
        self.tokenizer = transformers.AutoTokenizer.from_pretrained(
            self.model_id, trust_remote_code=True
        )
        self.model = transformers.AutoModelForCausalLM.from_pretrained(
            self.model_id, trust_remote_code=True
        )

    def generate(self, input_text, **generation_kwargs):
        # Подготовка входных данных для модели
        inputs = self.tokenizer(input_text, return_tensors="pt")
        # Генерация текста
        generated_tokens = self.model.generate(
            **inputs,
            **generation_kwargs,
        )
        # Декодирование сгенерированного текста
        return self.tokenizer.decode(generated_tokens[0], skip_special_tokens=True)


def construct_model():
    # Настройка параметров для генерации текста
    generation_kwargs = {
        "max_new_tokens": 20,  # Максимальное количество новых токенов
    }
    # Создание объекта обертки модели
    model = PhiWrapper()
    return model, generation_kwargs
