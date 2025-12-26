Minfin Currency Parser для Corezoid
Опис
Цей скрипт парсить курси валют USD з сайту Minfin.ua (стовбчик "При оплаті карткою") та повертає дані у форматі JSON
Структура проекту
minfin-parser/
├── main.py            # Основний файл з логікою парсингу
├── requirements.txt   # Python залежності
└── README.md          # Документація

Повертає:
json{
  "status": "success",
  "total_banks": 10,
  "currency_rates": [
    {
      "bank": "ПриватБанк",
      "buy": "41.00",
      "sell": "41.50",
      "updated": "11:30"
    },
    ...
  ]
}

Для використання Corezoid
pip install -r requirements.txt --break-system-packages