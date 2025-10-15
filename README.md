# 🌊 Windsurf Spoofer

[English](#english) | [Русский](#russian)

---

<a name="english"></a>
## 🇬🇧 English

### 📋 Description

**Windsurf Spoofer** is an automated tool for creating unlimited Windsurf IDE trial accounts with full premium subscription features.

### ✨ Features

- 🚀 **Full automation** — from creating temporary email to account confirmation
- 📧 **Built-in temporary email** (mail.tm) with automatic code parsing
- 🔄 **Automatic cleanup** of all Windsurf traces on macOS
- 💾 **Save all accounts** in convenient format
- 🌐 **Cloudflare bypass** and automatic form filling
- 📊 **Easy management** of created accounts
- 🌍 **Multi-language** interface (English/Russian)

### 🎯 How It Works

1. **Creates temporary email** via mail.tm API
2. **Automatically fills** Windsurf registration form
3. **Parses verification code** from email and enters it automatically
4. **Saves account data** for future use
5. **Cleans up traces** of previous account before creating new one

### 🛠️ Installation

#### Requirements:
- Python 3.8+
- Google Chrome

#### Quick Install:

```bash
git clone https://github.com/Ggvp1/Windsurf-Spoofer-MacOS
cd windsurf-spoof
pip3 install -r requirements.txt
python3 ws-spoof.py
```

#### Dependencies:
```
requests
selenium
webdriver-manager
```

### 📖 Usage

#### Main Menu:

```
======================================================
 Windsurf Spoofer v0.1
======================================================
1) 🔧 Scan and show Windsurf data
2) 🗑️  Delete found data
3) 📧 Temporary mail and code parsing
4) 🚀 Register Windsurf automatically
5) 📋 View created accounts
6) 🌐 Change Language
0) 🛑 Exit
======================================================
```

#### Creating Account:

**Step 1:** Select option `4) Register Windsurf automatically`

**Step 2:** Script will automatically:
- Create temporary email
- Generate random name/surname
- Fill registration form
- Get verification code from email
- Enter code and complete registration

**Step 3:** Account data will be saved to `accounts/windsurf_accounts.json`

### 📁 Project Structure

```
windsurf-spoof/
├── ws-spoof.py              # Main script
├── fix_chromedriver.py      # ChromeDriver cache cleanup utility
├── requirements.txt         # Dependencies
├── README.md                # This file
├── logs/                    # Operation logs
│   └── windsurf_clean.log
└── accounts/                # Saved accounts
    ├── windsurf_accounts.json
    ├── mail_accounts.json
    └── accounts_export.txt
```

### 🔥 Features

#### 1. Automatic Code Parsing
Script extracts 6-digit code directly from email subject and automatically enters it:

```
🔑 CODE FOUND IN EMAIL SUBJECT:
   ➜➜➜ 123456 ⬅⬅⬅

🔄 Entering code automatically...
✅ Code entered successfully!
```

#### 2. Smart Data Cleanup
Automatic scanning and removal of all Windsurf traces:
- Application Support
- Preferences
- Caches
- Containers
- Saved Application State

#### 3. Temporary Email Management
- Create new emails
- Login to saved emails
- Check messages in real-time
- Automatic verification code parsing

### ⚙️ Settings

#### Headless Mode (background operation):
Uncomment line in `ws-spoof.py`:
```python
chrome_options.add_argument('--headless')
```

### 🐛 Troubleshooting

#### ChromeDriver Error:
```bash
python3 fix_chromedriver.py
```

#### Error 429 (rate limit) when creating email:
- Wait 90 seconds
- Or use your own email manually

#### Can't find elements on page:
- Check Chrome version
- Update dependencies: `pip3 install -U selenium webdriver-manager`

### 📊 Statistics

- ⚡ **Speed:** ~2-3 minutes per account
- 🎯 **Success rate:** 95%+ with stable internet
- 💾 **Storage:** JSON format for easy export
- 🔄 **Automation:** 100% hands-free

### ⚠️ Disclaimer

This tool is created solely for educational purposes to demonstrate vulnerabilities in trial subscription systems. The author is not responsible for the use of this software. Use at your own risk.

### 📝 License

MIT License - see LICENSE file for details

---

<a name="russian"></a>
## 🇷🇺 Русский

### 📋 Описание

**Windsurf Spoofer** — автоматизированный инструмент для создания неограниченного количества trial аккаунтов Windsurf IDE с полным функционалом премиум подписки.

### ✨ Возможности

- 🚀 **Полная автоматизация** — от создания временной почты до подтверждения аккаунта
- 📧 **Встроенная временная почта** (mail.tm) с автоматическим парсингом кодов
- 🔄 **Автоматическая очистка** всех следов Windsurf на macOS
- 💾 **Сохранение всех аккаунтов** в удобном формате
- 🌐 **Обход Cloudflare** и автоматическое заполнение форм
- 📊 **Удобное управление** созданными аккаунтами
- 🌍 **Мультиязычный** интерфейс (Английский/Русский)

### 🎯 Как это работает

1. **Создание временной почты** через API mail.tm
2. **Автоматическое заполнение** регистрационной формы Windsurf
3. **Парсинг кода подтверждения** из письма и автоматический ввод
4. **Сохранение данных** аккаунта для дальнейшего использования
5. **Очистка следов** предыдущего аккаунта перед созданием нового

### 🛠️ Установка

#### Требования:
- Python 3.8+
- Google Chrome

#### Быстрая установка:

```bash
git clone https://github.com/Ggvp1/Windsurf-Spoofer-MacOS
cd windsurf-spoof
pip3 install -r requirements.txt
python3 ws-spoof.py
```

#### Зависимости:
```
requests
selenium
webdriver-manager
```

### 📖 Использование

#### Главное меню:

```
======================================================
 Windsurf Spoofer v0.1
======================================================
1) 🔧 Сканировать и показать найденные данные Windsurf
2) 🗑️  Удалить найденные данные
3) 📧 Временная почта и парсинг кодов
4) 🚀 Зарегистрировать Windsurf автоматически
5) 📋 Просмотр созданных аккаунтов
6) 🌐 Изменить язык
0) 🛑 Выход
======================================================
```

#### Создание аккаунта:

**Шаг 1:** Выбери опцию `4) Зарегистрировать Windsurf автоматически`

**Шаг 2:** Скрипт автоматически:
- Создаст временную почту
- Сгенерирует случайное имя/фамилию
- Заполнит форму регистрации
- Получит код подтверждения из письма
- Введет код и завершит регистрацию

**Шаг 3:** Данные аккаунта сохранятся в `accounts/windsurf_accounts.json`

### 📁 Структура проекта

```
windsurf-spoof/
├── ws-spoof.py              # Основной скрипт
├── fix_chromedriver.py      # Утилита очистки кеша chromedriver
├── requirements.txt         # Зависимости
├── README.md                # Этот файл
├── logs/                    # Логи операций
│   └── windsurf_clean.log
└── accounts/                # Сохраненные аккаунты
    ├── windsurf_accounts.json
    ├── mail_accounts.json
    └── accounts_export.txt
```

### 🔥 Фишки

#### 1. Автоматический парсинг кодов
Скрипт извлекает 6-значный код прямо из темы письма и автоматически вводит его:

```
🔑 НАЙДЕН КОД В ТЕМЕ ПИСЬМА:
   ➜➜➜ 123456 ⬅⬅⬅

🔄 Автоматически ввожу код в форму...
✅ Код введен автоматически!
```

#### 2. Умная очистка данных
Автоматическое сканирование и удаление всех следов Windsurf:
- Application Support
- Preferences
- Caches
- Containers
- Saved Application State

#### 3. Управление временными почтами
- Создание новых почт
- Вход в сохраненные почты
- Проверка писем в реальном времени
- Автоматический парсинг кодов подтверждения

### ⚙️ Настройки

#### Headless режим (фоновая работа):
Раскомментируй строку в `ws-spoof.py`:
```python
chrome_options.add_argument('--headless')
```

### 🐛 Решение проблем

#### Ошибка chromedriver:
```bash
python3 fix_chromedriver.py
```

#### Ошибка 429 (rate limit) при создании почты:
- Подожди 90 секунд
- Или используй свой email вручную

#### Не находит элементы на странице:
- Проверь версию Chrome
- Обнови зависимости: `pip3 install -U selenium webdriver-manager`

### 📊 Статистика

- ⚡ **Скорость:** ~2-3 минуты на один аккаунт
- 🎯 **Успешность:** 95%+ при стабильном интернете
- 💾 **Хранение:** JSON формат для удобного экспорта
- 🔄 **Автоматизация:** 100% без ручного вмешательства

### ⚠️ Дисклеймер

Этот инструмент создан исключительно в образовательных целях для демонстрации уязвимостей в системе trial подписок. Автор не несет ответственности за использование данного ПО. Используйте на свой страх и риск.

### 📝 Лицензия

MIT License - подробности в файле LICENSE

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Contact

For questions and support, please open an issue on GitHub.

---

**Enjoy unlimited Windsurf trial! 🌊**
