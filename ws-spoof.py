
import warnings
import logging
warnings.filterwarnings("ignore")
logging.disable(logging.CRITICAL)

import os
import shutil
import time
import re
import json
import random
import string
from pathlib import Path
try:
    import requests
except ImportError:
    requests = None
try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options
    from selenium.common.exceptions import TimeoutException, NoSuchElementException
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager
except ImportError:
    webdriver = None

HOME = Path.home()
CLEAR_CMD = "clear" if os.name == "posix" else "cls"

PROJECT_DIR = Path(__file__).parent
LOGS_DIR = PROJECT_DIR / "logs"
ACCOUNTS_DIR = PROJECT_DIR / "accounts"
LANG_FILE = PROJECT_DIR / "language.txt"

LOGS_DIR.mkdir(exist_ok=True)
ACCOUNTS_DIR.mkdir(exist_ok=True)

LOG_FILE = LOGS_DIR / "windsurf_clean.log"
WINDSURF_ACCOUNTS_FILE = ACCOUNTS_DIR / "windsurf_accounts.json"
MAIL_ACCOUNTS_FILE = ACCOUNTS_DIR / "mail_accounts.json"

CURRENT_LANG = "ru"

TRANSLATIONS = {
    "ru": {
        "main_menu_title": " Windsurf Spoofer v0.1",
        "scan_data": "🔧 Сканировать и показать найденные данные Windsurf",
        "delete_data": "🗑️  Удалить найденные данные",
        "temp_mail": "📧 Временная почта и парсинг кодов",
        "register_auto": "🚀 Зарегистрировать Windsurf автоматически",
        "view_accounts": "📋 Просмотр созданных аккаунтов",
        "change_language": "🌐 Изменить язык (Change Language)",
        "exit": "🛑 Выход",
        "back": "⬅️  Назад",
        "choose_action": "Выбери действие: ",
        "exiting": "Выход...",
        "invalid_choice": "Неверный выбор.",
        "data_not_found": "Данных Windsurf не найдено.",
        "found_items": "Найдено {} элементов:\n",
        "press_enter": "\nНажми Enter для продолжения...",
        "press_enter_short": "\nНажми Enter...",
        "no_data_to_delete": "Данных для удаления не найдено.",
        "found_items_to_delete": "Найдено {} элементов для удаления.",
        
        "view_accounts_title": " 📋 Просмотр созданных аккаунтов",
        "view_only_mails": "📧 Только почты (mail.tm)",
        "view_only_windsurf": "🌊 Только Windsurf аккаунты",
        "view_full_list": "📝 Полный список (mail:mailpass:windsurfpass)",
        
        "saved_mails_title": " 📧 Созданные почты (mail.tm)",
        "windsurf_accounts_title": " 🌊 Windsurf аккаунты",
        "full_list_title": " 📝 Полный список (mail:mailpass:windsurfpass)",
        
        "file_not_found": "\n❌ Файл с почтами не найден.",
        "windsurf_file_not_found": "\n❌ Файл с Windsurf аккаунтами не найден.",
        "no_saved_mails": "\n📭 Нет сохраненных почт.",
        "no_saved_accounts": "\n📭 Нет сохраненных Windsurf аккаунтов.",
        "no_saved_accounts_generic": "\n📭 Нет сохраненных аккаунтов.",
        
        "total_mails": "\n📬 Всего почт: {}\n",
        "total_accounts": "\n🌊 Всего аккаунтов: {}\n",
        "total_accounts_generic": "\n📋 Всего аккаунтов: {}\n",
        
        "email": "Email",
        "password": "Password",
        "created": "Создан",
        "used_for": "Использован для",
        "name": "Имя",
        "mail": "Почта",
        "windsurf_password": "Пароль",
        
        "format_label": "Формат: email:email_password:windsurf_password\n",
        "save_to_file": "\n💾 Сохранить в файл? (y/n): ",
        "exported_to": "\n✅ Экспортировано в: {}",
        "read_error": "\n❌ Ошибка чтения файла: {}",
        
        "mail_menu_title": " 📧 Временная почта и парсинг кодов",
        "current_mail": "📧 Текущая почта: {}",
        "check_messages": "Проверить новые письма",
        "logout_mail": "Выйти из почты",
        "create_new_mail": "Создать новую почту",
        "create_temp_mail": "Создать временную почту",
        "login_saved_mail": "Войти в сохраненную почту",
        "back_to_main": "Назад в главное меню",
        
        "saved_mails_menu_title": " 📧 Сохраненные почты",
        "choose_mail_number": "Выбери номер почты (или 0 для отмены): ",
        "logging_in": "\n🔄 Вхожу в {}...",
        "login_success": "✅ Успешный вход!",
        "login_error": "❌ Ошибка авторизации",
        "invalid_number": "❌ Неверный номер",
        "invalid_input": "❌ Неверный ввод",
        "error": "\n❌ Ошибка: {}",
        
        "logging_out": "\n🔄 Выхожу из {}...",
        "logged_out": "✅ Вышел из почты",
        
        "getting_domains": "\n🔄 Получаю доступные домены...",
        "domains_error": "❌ Не удалось получить домены",
        "available_domains": "✅ Доступные домены: {}",
        "enter_username": "\nВведи имя для почты (или Enter для случайного): ",
        "creating_account": "\n🔄 Создаю аккаунт {}...",
        "account_created": "✅ Аккаунт создан!",
        "account_create_error": "❌ Не удалось создать аккаунт",
        "auth_success": "✅ Авторизация успешна",
        "auth_error": "❌ Ошибка авторизации",
        "mail_saved": "💾 Данные почты сохранены в: {}",
        
        "checking_messages": "\n🔄 Проверяю письма...",
        "no_messages": "📭 Писем пока нет",
        "received_messages": "📬 Получено писем: {}",
        "subject": "Тема",
        "from": "От",
        "date": "Дата",
        "view_message": "Просмотреть письмо",
        "choose_message": "Выбери номер письма (или 0 для выхода): ",
        "message_body": "\n📧 Содержимое письма:",
        "found_codes": "\n🔑 Найденные коды:",
    },
    "en": {
        "main_menu_title": " Windsurf Spoofer v0.1",
        "scan_data": "🔧 Scan and show Windsurf data",
        "delete_data": "🗑️  Delete found data",
        "temp_mail": "📧 Temporary mail and code parsing",
        "register_auto": "🚀 Register Windsurf automatically",
        "view_accounts": "📋 View created accounts",
        "change_language": "🌐 Изменить язык (Change Language)",
        "exit": "🛑 Exit",
        "back": "⬅️  Back",
        "choose_action": "Choose action: ",
        "exiting": "Exiting...",
        "invalid_choice": "Invalid choice.",
        "data_not_found": "Windsurf data not found.",
        "found_items": "Found {} items:\n",
        "press_enter": "\nPress Enter to continue...",
        "press_enter_short": "\nPress Enter...",
        "no_data_to_delete": "No data to delete.",
        "found_items_to_delete": "Found {} items to delete.",
        
        "view_accounts_title": " 📋 View created accounts",
        "view_only_mails": "📧 Emails only (mail.tm)",
        "view_only_windsurf": "🌊 Windsurf accounts only",
        "view_full_list": "📝 Full list (mail:mailpass:windsurfpass)",
        
        "saved_mails_title": " 📧 Created emails (mail.tm)",
        "windsurf_accounts_title": " 🌊 Windsurf accounts",
        "full_list_title": " 📝 Full list (mail:mailpass:windsurfpass)",
        
        "file_not_found": "\n❌ Email file not found.",
        "windsurf_file_not_found": "\n❌ Windsurf accounts file not found.",
        "no_saved_mails": "\n📭 No saved emails.",
        "no_saved_accounts": "\n📭 No saved Windsurf accounts.",
        "no_saved_accounts_generic": "\n📭 No saved accounts.",
        
        "total_mails": "\n📬 Total emails: {}\n",
        "total_accounts": "\n🌊 Total accounts: {}\n",
        "total_accounts_generic": "\n📋 Total accounts: {}\n",
        
        "email": "Email",
        "password": "Password",
        "created": "Created",
        "used_for": "Used for",
        "name": "Name",
        "mail": "Email",
        "windsurf_password": "Password",
        
        "format_label": "Format: email:email_password:windsurf_password\n",
        "save_to_file": "\n💾 Save to file? (y/n): ",
        "exported_to": "\n✅ Exported to: {}",
        "read_error": "\n❌ Read error: {}",
        
        "mail_menu_title": " 📧 Temporary mail and code parsing",
        "current_mail": "📧 Current email: {}",
        "check_messages": "Check new messages",
        "logout_mail": "Logout from email",
        "create_new_mail": "Create new email",
        "create_temp_mail": "Create temporary email",
        "login_saved_mail": "Login to saved email",
        "back_to_main": "Back to main menu",
        
        "saved_mails_menu_title": " 📧 Saved emails",
        "choose_mail_number": "Choose email number (or 0 to cancel): ",
        "logging_in": "\n🔄 Logging into {}...",
        "login_success": "✅ Login successful!",
        "login_error": "❌ Authorization error",
        "invalid_number": "❌ Invalid number",
        "invalid_input": "❌ Invalid input",
        "error": "\n❌ Error: {}",
        
        "logging_out": "\n🔄 Logging out from {}...",
        "logged_out": "✅ Logged out",
        
        "getting_domains": "\n🔄 Getting available domains...",
        "domains_error": "❌ Failed to get domains",
        "available_domains": "✅ Available domains: {}",
        "enter_username": "\nEnter email username (or Enter for random): ",
        "creating_account": "\n🔄 Creating account {}...",
        "account_created": "✅ Account created!",
        "account_create_error": "❌ Failed to create account",
        "auth_success": "✅ Authorization successful",
        "auth_error": "❌ Authorization error",
        "mail_saved": "💾 Email data saved to: {}",
        
        "checking_messages": "\n🔄 Checking messages...",
        "no_messages": "📭 No messages yet",
        "received_messages": "📬 Received messages: {}",
        "subject": "Subject",
        "from": "From",
        "date": "Date",
        "view_message": "View message",
        "choose_message": "Choose message number (or 0 to exit): ",
        "message_body": "\n📧 Message content:",
        "found_codes": "\n🔑 Found codes:",
    }
}

def t(key):
    return TRANSLATIONS.get(CURRENT_LANG, TRANSLATIONS["ru"]).get(key, key)

def load_language():
    global CURRENT_LANG
    if LANG_FILE.exists():
        try:
            with open(LANG_FILE, 'r') as f:
                lang = f.read().strip()
                if lang in ["ru", "en"]:
                    CURRENT_LANG = lang
        except:
            pass

def save_language(lang):
    global CURRENT_LANG
    CURRENT_LANG = lang
    with open(LANG_FILE, 'w') as f:
        f.write(lang)

TARGET_KEYWORDS = ["windsurf"]
SEARCH_PATHS = [
    HOME / "Library" / "Application Support",
    HOME / "Library" / "Preferences",
    HOME / "Library" / "Caches",
    HOME / "Library" / "Containers",
    HOME / "Library" / "Group Containers",
    HOME / "Library" / "Saved Application State",
    HOME / "Library" / "Logs",
]


def clear_screen():
    os.system(CLEAR_CMD)

def log(msg: str):
    ts = time.strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"[{ts}] {msg}\n")
    except Exception:
        pass

def human_size(n: int) -> str:
    for u in ("B","KB","MB","GB","TB"):
        if n < 1024.0:
            return f"{n:3.2f} {u}"
        n /= 1024.0
    return f"{n:.2f} PB"

def folder_size(path: Path) -> int:
    total = 0
    try:
        if path.is_file():
            return path.stat().st_size
        for root, _, files in os.walk(path):
            for f in files:
                try:
                    total += (Path(root) / f).stat().st_size
                except Exception:
                    pass
    except Exception:
        pass
    return total


class MailTM:
    BASE_URL = "https://api.mail.tm"
    
    def __init__(self):
        self.token = None
        self.email = None
        self.password = None
        self.account_id = None
    
    def get_domains(self):
        """Получить доступные домены"""
        try:
            resp = requests.get(f"{self.BASE_URL}/domains")
            if resp.status_code == 200:
                data = resp.json()
                return [d["domain"] for d in data.get("hydra:member", [])]
        except Exception as e:
            print(f"Ошибка получения доменов: {e}")
        return []
    
    def create_account(self, address, password):
        """Создать аккаунт"""
        try:
            payload = {"address": address, "password": password}
            resp = requests.post(f"{self.BASE_URL}/accounts", json=payload)
            if resp.status_code == 201:
                data = resp.json()
                self.email = data["address"]
                self.password = password
                self.account_id = data["id"]
                return True
            else:
                print(f"Ошибка создания аккаунта: {resp.status_code}")
        except Exception as e:
            print(f"Ошибка создания аккаунта: {e}")
        return False
    
    def get_token(self):
        """Получить токен авторизации"""
        try:
            payload = {"address": self.email, "password": self.password}
            resp = requests.post(f"{self.BASE_URL}/token", json=payload)
            if resp.status_code == 200:
                data = resp.json()
                self.token = data["token"]
                return True
        except Exception as e:
            print(f"Ошибка получения токена: {e}")
        return False
    
    def get_messages(self):
        """Получить список сообщений"""
        if not self.token:
            return []
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            resp = requests.get(f"{self.BASE_URL}/messages", headers=headers)
            if resp.status_code == 200:
                data = resp.json()
                return data.get("hydra:member", [])
        except Exception as e:
            print(f"Ошибка получения сообщений: {e}")
        return []
    
    def get_message(self, msg_id):
        """Получить конкретное сообщение"""
        if not self.token:
            return None
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            resp = requests.get(f"{self.BASE_URL}/messages/{msg_id}", headers=headers)
            if resp.status_code == 200:
                return resp.json()
        except Exception as e:
            print(f"Ошибка получения сообщения: {e}")
        return None


def extract_codes(text):
    """Извлечь коды из текста (6-значные числа, коды типа ABC-123, и т.д.)"""
    codes = []
    codes.extend(re.findall(r'\b\d{6}\b', text))
    codes.extend(re.findall(r'\b\d{4,8}\b', text))
    codes.extend(re.findall(r'\b[A-Z0-9]{3,}-?[A-Z0-9]{3,}\b', text))
    patterns = [
        r'(?:verification|confirmation|code|pin|otp)[:\s]+([A-Z0-9-]{4,})',
        r'([A-Z0-9-]{4,})\s+(?:is your|verification|confirmation)',
    ]
    for pattern in patterns:
        codes.extend(re.findall(pattern, text, re.IGNORECASE))
    return list(set(codes))


def generate_random_name():
    """Генерация случайного имени и фамилии"""
    first_names = [
        "Alex", "Jordan", "Taylor", "Morgan", "Casey", "Riley", "Avery", "Quinn",
        "Skyler", "Cameron", "Dakota", "Peyton", "Reese", "Charlie", "Finley",
        "Rowan", "Sage", "River", "Phoenix", "Kai", "Emerson", "Blake", "Parker",
        "Hayden", "Kendall", "Sawyer", "Logan", "Drew", "Dylan", "Jesse"
    ]
    
    last_names = [
        "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller",
        "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez",
        "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin",
        "Lee", "Walker", "Hall", "Allen", "Young", "King", "Wright", "Scott",
        "Torres", "Nguyen", "Hill", "Flores", "Green", "Adams", "Nelson"
    ]
    
    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    return first_name, last_name


def register_windsurf_auto():
    """Автоматическая регистрация Windsurf"""
    if webdriver is None:
        print("⚠️ Selenium не установлен!")
        print("Установи: pip install selenium")
        input("\nНажми Enter...")
        return
    
    if requests is None:
        print("⚠️ Модуль requests не установлен!")
        print("Установи: pip install requests")
        input("\nНажми Enter...")
        return
    
    print("\n" + "="*55)
    print(" АВТОМАТИЧЕСКАЯ РЕГИСТРАЦИЯ WINDSURF")
    print("="*55)
    
    mail = MailTM()
    email_created = False
    
    print("\n🔄 Создаю временную почту...")
    domains = mail.get_domains()
    
    if domains:
        username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
        email_address = f"{username}@{domains[0]}"
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
        
        if mail.create_account(email_address, password):
            if mail.get_token():
                print(f"✅ Email создан: {mail.email}")
                log(f"windsurf registration: email created {mail.email}")
                email_created = True
    
    if not email_created:
        print("\n⚠️  Не удалось создать временную почту автоматически")
        print("Причины: rate limit (429), проблемы с API, или домены недоступны")
        print("\nВарианты:")
        print("1) Ввести свой email вручную")
        print("2) Подождать 1-2 минуты и попробовать снова")
        print("3) Использовать другой сервис временной почты")
        print("0) Отмена")
        
        choice = input("\nВыбери вариант: ").strip()
        
        if choice == "1":
            manual_email = input("\nВведи email: ").strip()
            if not manual_email or '@' not in manual_email:
                print("❌ Неверный формат email")
                input("\nНажми Enter...")
                return
            mail.email = manual_email
            mail.password = None
            print(f"✅ Будет использован email: {mail.email}")
            print("⚠️  Проверка писем будет недоступна")
        elif choice == "2":
            print("\n⏳ Жду 90 секунд...")
            time.sleep(90)
            print("\n🔄 Пробую создать почту снова...")
            
            domains = mail.get_domains()
            if domains:
                username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
                email_address = f"{username}@{domains[0]}"
                password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
                
                if mail.create_account(email_address, password) and mail.get_token():
                    print(f"✅ Email создан: {mail.email}")
                    log(f"windsurf registration: email created {mail.email}")
                else:
                    print("❌ Снова не удалось. Попробуй позже или используй свой email")
                    input("\nНажми Enter...")
                    return
            else:
                print("❌ Не удалось получить домены")
                input("\nНажми Enter...")
                return
        else:
            print("Отменено")
            input("\nНажми Enter...")
            return
    
    first_name, last_name = generate_random_name()
    print(f"✅ Имя: {first_name} {last_name}")
    log(f"windsurf registration: name {first_name} {last_name}")
    
    print("\n🔄 Запускаю браузер...")
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    try:
        print("🔄 Скачиваю chromedriver...")
        driver_path = ChromeDriverManager().install()
        
        driver_path_obj = Path(driver_path)
        
        if 'THIRD_PARTY_NOTICES' in driver_path or 'LICENSE' in driver_path:
            parent_dir = driver_path_obj.parent
            correct_driver = parent_dir / "chromedriver"
            if correct_driver.exists():
                driver_path = str(correct_driver)
                driver_path_obj = correct_driver
                print(f"🔧 Исправлен путь на: {driver_path}")
                
                try:
                    os.chmod(correct_driver, 0o755)
                    print(f"🔧 Установлены права на выполнение")
                except Exception as e:
                    print(f"⚠️  Ошибка установки прав: {e}")
                
                try:
                    os.system(f'xattr -d com.apple.quarantine "{correct_driver}" 2>/dev/null')
                except:
                    pass
        
        if not driver_path_obj.is_file() or not os.access(driver_path, os.X_OK):
            parent_dir = driver_path_obj.parent
            
            possible_paths = [
                parent_dir / "chromedriver",
                parent_dir / "chromedriver-mac-x64" / "chromedriver",
                parent_dir / "chromedriver-mac-arm64" / "chromedriver",
            ]
            
            for item in parent_dir.rglob("chromedriver"):
                if item.is_file() and os.access(item, os.X_OK):
                    possible_paths.insert(0, item)
                    break
            
            driver_found = False
            for path in possible_paths:
                if path.exists() and path.is_file():
                    if not os.access(path, os.X_OK):
                        try:
                            os.chmod(path, 0o755)
                            print(f"🔧 Установлены права на выполнение: {path}")
                        except Exception as e:
                            print(f"⚠️  Не удалось установить права: {e}")
                            continue
                    
                    if os.name == 'posix':
                        try:
                            os.system(f'xattr -d com.apple.quarantine "{path}" 2>/dev/null')
                        except:
                            pass
                    
                    driver_path = str(path)
                    driver_found = True
                    print(f"✅ Найден chromedriver: {driver_path}")
                    break
            
            if not driver_found:
                print(f"❌ Не удалось найти исполняемый chromedriver в: {parent_dir}")
                print("Попробуй очистить кеш: python3 fix_chromedriver.py")
                input("\nНажми Enter...")
                return
        
        service = Service(driver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        print("✅ Браузер запущен")
        print("\n🔄 Открываю страницу регистрации Windsurf...")
        
        driver.get("https://codeium.com/account/register")
        time.sleep(3)
        
        print("✅ Страница загружена")
        print("\n🔄 Заполняю первый этап (имя, фамилия, email)...")
        
        wait = WebDriverWait(driver, 20)
        
        try:
            first_name_field = wait.until(
                EC.presence_of_element_located((By.NAME, "firstName"))
            )
            first_name_field.clear()
            first_name_field.send_keys(first_name)
            print(f"✅ Имя введено: {first_name}")
            time.sleep(0.5)
            
            last_name_field = driver.find_element(By.NAME, "lastName")
            last_name_field.clear()
            last_name_field.send_keys(last_name)
            print(f"✅ Фамилия введена: {last_name}")
            time.sleep(0.5)
            
            email_field = driver.find_element(By.NAME, "email")
            email_field.clear()
            email_field.send_keys(mail.email)
            print(f"✅ Email введен: {mail.email}")
            time.sleep(0.5)
            
            print("\n🔄 Принимаю условия использования...")
            try:
                terms_checkbox = driver.find_element(By.ID, "terms")
                if not terms_checkbox.is_selected():
                    terms_checkbox.click()
                    print("✅ Галочка на terms поставлена")
                    time.sleep(0.5)
            except Exception as e:
                print(f"⚠️  Не удалось найти чекбокс: {e}")
            
            print("\n🔄 Нажимаю кнопку Continue...")
            try:
                continue_button = None
                try:
                    continue_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Continue')]")
                except:
                    try:
                        continue_button = driver.find_element(By.XPATH, "//button[@type='submit']")
                    except:
                        try:
                            continue_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
                        except:
                            continue_button = driver.find_element(By.TAG_NAME, "button")
                
                if continue_button:
                    continue_button.click()
                    print("✅ Кнопка Continue нажата")
            except Exception as e:
                print(f"⚠️  Не удалось найти кнопку: {e}")
                print("Нажми кнопку Continue вручную в браузере!")
                time.sleep(10)
            
            time.sleep(3)
            
            print("\n🔄 Заполняю второй этап (пароль)...")
            windsurf_password = ''.join(random.choices(string.ascii_letters + string.digits + "!@#$%", k=12))
            
            password_field = wait.until(
                EC.presence_of_element_located((By.NAME, "password"))
            )
            password_field.clear()
            password_field.send_keys(windsurf_password)
            print(f"✅ Пароль введен: {windsurf_password}")
            time.sleep(0.5)
            
            try:
                confirm_password_field = driver.find_element(By.ID, "passwordConfirmation")
                confirm_password_field.clear()
                confirm_password_field.send_keys(windsurf_password)
                print("✅ Повтор пароля введен")
                time.sleep(0.5)
            except:
                try:
                    confirm_password_field = driver.find_element(By.NAME, "confirmPassword")
                    confirm_password_field.clear()
                    confirm_password_field.send_keys(windsurf_password)
                    print("✅ Повтор пароля введен")
                    time.sleep(0.5)
                except:
                    print("⚠️ Поле повтора пароля не найдено")
            
            print("\n🔄 Жду активации кнопки Continue...")
            time.sleep(1)
            
            try:
                continue_button = wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Continue') and not(@disabled)]"))
                )
                print("✅ Кнопка Continue активна")
                time.sleep(0.5)
                
                driver.execute_script("arguments[0].scrollIntoView(true);", continue_button)
                time.sleep(0.3)
                continue_button.click()
                print("✅ Кнопка Continue нажата")
            except TimeoutException:
                print("⚠️  Кнопка Continue не стала активной, пробую альтернативные методы...")
                try:
                    buttons = driver.find_elements(By.XPATH, "//button[contains(text(), 'Continue')]")
                    for btn in buttons:
                        if btn.is_enabled() and btn.is_displayed():
                            driver.execute_script("arguments[0].click();", btn)
                            print("✅ Кнопка Continue нажата (JS)")
                            break
                except Exception as e:
                    print(f"⚠️  Не удалось нажать кнопку: {e}")
                    print("Нажми кнопку Continue вручную в браузере!")
                    time.sleep(10)
            
            time.sleep(3)
            
            print("\n⚠️  CLOUDFLARE CAPTCHA: Теперь подтверди капчу и введи код из письма!")
            print("📬 Проверяю почту каждые 10 секунд...")
            
            code_found = False
            verification_code = None
            
            if mail.token:
                for attempt in range(6):
                    print(f"\n🔄 Попытка {attempt + 1}/6: Проверяю письма...")
                    time.sleep(10)
                    
                    messages = mail.get_messages()
                    if messages:
                        print(f"📬 Получено писем: {len(messages)}")
                        for msg in messages:
                            subject = msg.get('subject', '')
                            print(f"📧 Тема: {subject}")
                            
                            code_match = re.match(r'^(\d{6})', subject)
                            if code_match:
                                verification_code = code_match.group(1)
                                print(f"\n🔑 НАЙДЕН КОД В ТЕМЕ ПИСЬМА:")
                                print(f"   ➜➜➜ {verification_code} ⬅⬅⬅")
                                log(f"verification code from subject: {verification_code}")
                                code_found = True
                                break
                            
                            full_msg = mail.get_message(msg['id'])
                            if full_msg and not code_found:
                                text_content = full_msg.get('text', '')
                                html_content = full_msg.get('html', [])
                                all_text = text_content + ' ' + ' '.join(html_content)
                                
                                codes = extract_codes(all_text)
                                if codes:
                                    verification_code = codes[0]
                                    print(f"\n🔑 НАЙДЕН КОД В ПИСЬМЕ:")
                                    print(f"   ➜➜➜ {verification_code} ⬅⬅⬅")
                                    log(f"verification code from body: {verification_code}")
                                    code_found = True
                                    break
                        
                        if code_found:
                            break
                    else:
                        print("📭 Писем пока нет, жду...")
                
                if code_found and verification_code and len(verification_code) == 6:
                    print("\n🔄 Автоматически ввожу код в форму...")
                    try:
                        code_inputs = driver.find_elements(By.XPATH, "//input[@maxlength='1' and @pattern='[A-Za-z0-9]']")
                        
                        if len(code_inputs) == 6:
                            for i, digit in enumerate(verification_code):
                                code_inputs[i].clear()
                                code_inputs[i].send_keys(digit)
                                time.sleep(0.2)
                            
                            print("✅ Код введен автоматически!")
                            time.sleep(1)
                            
                            try:
                                create_button = wait.until(
                                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Create account') and not(@disabled)]"))
                                )
                                create_button.click()
                                print("✅ Кнопка 'Create account' нажата!")
                            except:
                                print("⚠️  Кнопка 'Create account' не найдена или не активна")
                        else:
                            print(f"⚠️  Найдено {len(code_inputs)} полей вместо 6. Введи код вручную: {verification_code}")
                    except Exception as e:
                        print(f"⚠️  Ошибка при вводе кода: {e}")
                        print(f"Введи код вручную: {verification_code}")
                else:
                    print("\n⚠️  Код не найден автоматически. Проверь почту вручную через меню Mail.tm")
            else:
                print("\n⏳ Жду 60 секунд...")
                time.sleep(60)
            
            windsurf_data = {
                "email": mail.email,
                "email_password": mail.password if mail.password else "N/A (manual email)",
                "first_name": first_name,
                "last_name": last_name,
                "windsurf_password": windsurf_password,
                "created_at": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            
            windsurf_accounts = []
            if WINDSURF_ACCOUNTS_FILE.exists():
                try:
                    with open(WINDSURF_ACCOUNTS_FILE, 'r', encoding='utf-8') as f:
                        windsurf_accounts = json.load(f)
                except:
                    pass
            
            windsurf_accounts.append(windsurf_data)
            with open(WINDSURF_ACCOUNTS_FILE, 'w', encoding='utf-8') as f:
                json.dump(windsurf_accounts, f, indent=2, ensure_ascii=False)
            
            if mail.password:
                mail_data = {
                    "email": mail.email,
                    "password": mail.password,
                    "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "used_for": "windsurf_registration"
                }
                
                mail_accounts = []
                if MAIL_ACCOUNTS_FILE.exists():
                    try:
                        with open(MAIL_ACCOUNTS_FILE, 'r', encoding='utf-8') as f:
                            mail_accounts = json.load(f)
                    except:
                        pass
                
                mail_accounts.append(mail_data)
                with open(MAIL_ACCOUNTS_FILE, 'w', encoding='utf-8') as f:
                    json.dump(mail_accounts, f, indent=2, ensure_ascii=False)
            
            print(f"\n💾 Данные Windsurf сохранены в: {WINDSURF_ACCOUNTS_FILE}")
            if mail.password:
                print(f"💾 Данные почты сохранены в: {MAIL_ACCOUNTS_FILE}")
            log(f"windsurf registration completed: {mail.email}")
            
            print("\n⏳ Даю еще 20 секунд на завершение...")
            time.sleep(20)
            
        except TimeoutException:
            print("\n❌ Не удалось найти поля формы. Возможно, структура сайта изменилась.")
            print("Попробуй зарегистрироваться вручную.")
        except NoSuchElementException as e:
            print(f"\n❌ Элемент не найден: {e}")
        
        print("\n✅ Процесс завершен. Браузер останется открытым 10 секунд.")
        time.sleep(10)
        
    except Exception as e:
        print(f"\n❌ Ошибка: {e}")
        log(f"windsurf registration error: {e}")
    finally:
        try:
            driver.quit()
            print("\n🔄 Браузер закрыт")
        except:
            pass
    
    input("\nНажми Enter для возврата в меню...")


def mail_tm_menu():
    """Меню работы с mail.tm"""
    if requests is None:
        print("⚠️ Модуль requests не установлен!")
        print("Установи: pip install requests")
        input("\nНажми Enter...")
        return
    
    mail = MailTM()
    
    while True:
        clear_screen()
        print("="*55)
        print(t("mail_menu_title"))
        print("="*55)
        
        if mail.email:
            print(t("current_mail").format(mail.email))
            print("="*55)
            print(f"1) {t('check_messages')}")
            print(f"2) {t('logout_mail')}")
            print(f"3) {t('create_new_mail')}")
            print(f"0) {t('back_to_main')}")
        else:
            print(f"1) {t('create_temp_mail')}")
            print(f"2) {t('login_saved_mail')}")
            print(f"0) {t('back')}")
        
        print("="*55)
        choice = input(t("choose_action")).strip()
        
        if choice == "0":
            break
        elif choice == "2" and mail.email:
            print(t("logging_out").format(mail.email))
            mail.email = None
            mail.password = None
            mail.token = None
            print(t("logged_out"))
            log("logged out from mail")
            time.sleep(1)
        elif choice == "2" and not mail.email:
            clear_screen()
            print("="*55)
            print(t("saved_mails_menu_title"))
            print("="*55)
            
            if not MAIL_ACCOUNTS_FILE.exists():
                print(t("file_not_found"))
                input(t("press_enter_short"))
                continue
            
            try:
                with open(MAIL_ACCOUNTS_FILE, 'r', encoding='utf-8') as f:
                    mail_accounts = json.load(f)
                
                if not mail_accounts:
                    print(t("no_saved_mails"))
                    input(t("press_enter_short"))
                    continue
                
                print(t("total_mails").format(len(mail_accounts)))
                for i, acc in enumerate(mail_accounts, 1):
                    print(f"{i}. {acc.get('email', 'N/A')}")
                    print(f"   {t('created')}: {acc.get('created_at', 'N/A')}")
                    print()
                
                print("="*55)
                choice_num = input(t("choose_mail_number")).strip()
                
                if choice_num == "0":
                    continue
                
                try:
                    idx = int(choice_num) - 1
                    if 0 <= idx < len(mail_accounts):
                        selected = mail_accounts[idx]
                        email = selected.get('email')
                        password = selected.get('password')
                        
                        print(t("logging_in").format(email))
                        
                        mail.email = email
                        mail.password = password
                        
                        if mail.get_token():
                            print(t("login_success"))
                            log(f"logged into saved mail: {email}")
                        else:
                            print(t("login_error"))
                            mail.email = None
                            mail.password = None
                    else:
                        print(t("invalid_number"))
                except ValueError:
                    print(t("invalid_input"))
                
            except Exception as e:
                print(t("error").format(e))
            
            input(t("press_enter_short"))
        
        elif choice == "1" and not mail.email:
            print(t("getting_domains"))
            domains = mail.get_domains()
            if not domains:
                print(t("domains_error"))
                input(t("press_enter_short"))
                continue
            
            print(t("available_domains").format(', '.join(domains)))
            username = input(t("enter_username")).strip()
            if not username:
                import random
                import string
                username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
            
            email_address = f"{username}@{domains[0]}"
            password = ''.join(__import__('random').choices(__import__('string').ascii_letters + __import__('string').digits, k=12))
            
            print(t("creating_account").format(email_address))
            if mail.create_account(email_address, password):
                print(t("account_created"))
                print(f"📧 {t('email')}: {mail.email}")
                print(f"🔑 {t('password')}: {mail.password}")
                log(f"mail.tm account created: {mail.email}")
                
                mail_data = {
                    "email": mail.email,
                    "password": mail.password,
                    "created_at": time.strftime("%Y-%m-%d %H:%M:%S")
                }
                
                mail_accounts = []
                if MAIL_ACCOUNTS_FILE.exists():
                    try:
                        with open(MAIL_ACCOUNTS_FILE, 'r', encoding='utf-8') as f:
                            mail_accounts = json.load(f)
                    except:
                        pass
                
                mail_accounts.append(mail_data)
                with open(MAIL_ACCOUNTS_FILE, 'w', encoding='utf-8') as f:
                    json.dump(mail_accounts, f, indent=2, ensure_ascii=False)
                
                print(t("mail_saved").format(MAIL_ACCOUNTS_FILE))
                
                if mail.get_token():
                    print(t("auth_success"))
                else:
                    print(t("auth_error"))
            else:
                print(t("account_create_error"))
            
            input(t("press_enter_short"))
        
        elif choice == "3" and mail.email:
            print("\n🔄 Получаю доступные домены...")
            domains = mail.get_domains()
            if not domains:
                print("❌ Не удалось получить домены")
                input("\nНажми Enter...")
                continue
            
            print(f"✅ Доступные домены: {', '.join(domains)}")
            username = input("\nВведи имя для почты (или Enter для случайного): ").strip()
            if not username:
                import random
                import string
                username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
            
            email_address = f"{username}@{domains[0]}"
            password = ''.join(__import__('random').choices(__import__('string').ascii_letters + __import__('string').digits, k=12))
            
            print(f"\n🔄 Создаю аккаунт {email_address}...")
            
            new_mail = MailTM()
            if new_mail.create_account(email_address, password):
                print(f"✅ Аккаунт создан!")
                print(f"📧 Email: {new_mail.email}")
                print(f"🔑 Password: {new_mail.password}")
                log(f"mail.tm account created: {new_mail.email}")
                
                mail_data = {
                    "email": new_mail.email,
                    "password": new_mail.password,
                    "created_at": time.strftime("%Y-%m-%d %H:%M:%S")
                }
                
                mail_accounts = []
                if MAIL_ACCOUNTS_FILE.exists():
                    try:
                        with open(MAIL_ACCOUNTS_FILE, 'r', encoding='utf-8') as f:
                            mail_accounts = json.load(f)
                    except:
                        pass
                
                mail_accounts.append(mail_data)
                with open(MAIL_ACCOUNTS_FILE, 'w', encoding='utf-8') as f:
                    json.dump(mail_accounts, f, indent=2, ensure_ascii=False)
                
                print(f"💾 Данные почты сохранены в: {MAIL_ACCOUNTS_FILE}")
                
                if new_mail.get_token():
                    print("✅ Авторизация успешна")
                    mail = new_mail
                else:
                    print("❌ Ошибка авторизации")
            else:
                print("❌ Не удалось создать аккаунт")
            
            input("\nНажми Enter...")
        
        elif choice == "1" and mail.email:
            print("\n🔄 Проверяю письма...")
            messages = mail.get_messages()
            
            if not messages:
                print("📭 Писем пока нет")
                input("\nНажми Enter...")
                continue
            
            print(f"\n📬 Найдено писем: {len(messages)}\n")
            
            for msg in messages:
                print("="*55)
                print(f"От: {msg.get('from', {}).get('address', 'N/A')}")
                print(f"Тема: {msg.get('subject', 'N/A')}")
                print(f"Дата: {msg.get('createdAt', 'N/A')}")
                
                full_msg = mail.get_message(msg['id'])
                if full_msg:
                    text_content = full_msg.get('text', '')
                    html_content = full_msg.get('html', [])
                    
                    all_text = text_content
                    if html_content:
                        all_text += ' ' + re.sub(r'<[^>]+>', ' ', ' '.join(html_content))
                    
                    codes = extract_codes(all_text)
                    
                    if codes:
                        print("\n🔑 НАЙДЕННЫЕ КОДЫ:")
                        for code in codes:
                            print(f"   ➜ {code}")
                            log(f"code found: {code} from {msg.get('from', {}).get('address', 'N/A')}")
                    else:
                        print("\n⚠️ Коды не найдены")
                    
                    if text_content:
                        preview = text_content[:200].replace('\n', ' ')
                        print(f"\n📄 Превью: {preview}...")
                
                print("="*55)
                print()
            
            input("\nНажми Enter...")
        
        elif choice == "2" and mail.email:
            mail = MailTM()
            print("\n🔄 Текущая почта сброшена")
            time.sleep(1)


def find_windsurf_data():
    found = {}
    for base in SEARCH_PATHS:
        if not base.exists():
            continue
        try:
            for entry in base.rglob("*"):
                name = entry.name.lower()
                full = str(entry).lower()
                if any(k in name or k in full for k in TARGET_KEYWORDS):
                    size = folder_size(entry)
                    found[str(entry)] = size
        except Exception:
            continue
    items = sorted(found.items(), key=lambda x: x[1], reverse=True)
    return items


def remove_targets(items):
    if not items:
        print("Ничего не найдено для удаления.")
        return
    confirm = input("⚠️  Напиши EXACTLY 'DELETE' для подтверждения удаления: ").strip()
    if confirm != "DELETE":
        print("Отменено пользователем.")
        return

    for path_str, _ in items:
        p = Path(path_str)
        try:
            if not str(p).startswith(str(HOME)):
                print(f"⛔ Пропуск системного пути: {p}")
                log(f"skip system path: {p}")
                continue
            if p.is_dir():
                shutil.rmtree(p)
                print(f"🗑️  Удалена папка: {p}")
                log(f"removed dir: {p}")
            elif p.exists():
                p.unlink()
                print(f"🗑️  Удалён файл: {p}")
                log(f"removed file: {p}")
        except Exception as e:
            print(f"⚠️ Ошибка при удалении {p}: {e}")
            log(f"remove error {p}: {e}")

    print("\n✅ Очистка завершена.")
    log("cleanup complete.")


def view_accounts_menu():
    while True:
        clear_screen()
        print("="*55)
        print(t("view_accounts_title"))
        print("="*55)
        print(f"1) {t('view_only_mails')}")
        print(f"2) {t('view_only_windsurf')}")
        print(f"3) {t('view_full_list')}")
        print(f"0) {t('back')}")
        print("="*55)
        choice = input(t("choose_action")).strip()
        
        if choice == "0":
            break
        elif choice == "1":
            clear_screen()
            print("="*55)
            print(t("saved_mails_title"))
            print("="*55)
            
            if not MAIL_ACCOUNTS_FILE.exists():
                print(t("file_not_found"))
            else:
                try:
                    with open(MAIL_ACCOUNTS_FILE, 'r', encoding='utf-8') as f:
                        mail_accounts = json.load(f)
                    
                    if not mail_accounts:
                        print(t("no_saved_mails"))
                    else:
                        print(t("total_mails").format(len(mail_accounts)))
                        for i, acc in enumerate(mail_accounts, 1):
                            print(f"{i}. {t('email')}: {acc.get('email', 'N/A')}")
                            print(f"   {t('password')}: {acc.get('password', 'N/A')}")
                            print(f"   {t('created')}: {acc.get('created_at', 'N/A')}")
                            if acc.get('used_for'):
                                print(f"   {t('used_for')}: {acc.get('used_for')}")
                            print()
                except Exception as e:
                    print(t("read_error").format(e))
            
            input(t("press_enter_short"))
        
        elif choice == "2":
            clear_screen()
            print("="*55)
            print(t("windsurf_accounts_title"))
            print("="*55)
            
            if not WINDSURF_ACCOUNTS_FILE.exists():
                print(t("windsurf_file_not_found"))
            else:
                try:
                    with open(WINDSURF_ACCOUNTS_FILE, 'r', encoding='utf-8') as f:
                        windsurf_accounts = json.load(f)
                    
                    if not windsurf_accounts:
                        print(t("no_saved_accounts"))
                    else:
                        print(t("total_accounts").format(len(windsurf_accounts)))
                        for i, acc in enumerate(windsurf_accounts, 1):
                            print(f"{i}. {t('name')}: {acc.get('first_name', 'N/A')} {acc.get('last_name', 'N/A')}")
                            print(f"   {t('mail')}: {acc.get('email', 'N/A')}")
                            print(f"   {t('windsurf_password')}: {acc.get('windsurf_password', 'N/A')}")
                            print(f"   {t('created')}: {acc.get('created_at', 'N/A')}")
                            print()
                except Exception as e:
                    print(t("read_error").format(e))
            
            input(t("press_enter_short"))
        
        elif choice == "3":
            clear_screen()
            print("="*55)
            print(t("full_list_title"))
            print("="*55)
            
            if not WINDSURF_ACCOUNTS_FILE.exists():
                print(t("windsurf_file_not_found"))
            else:
                try:
                    with open(WINDSURF_ACCOUNTS_FILE, 'r', encoding='utf-8') as f:
                        windsurf_accounts = json.load(f)
                    
                    if not windsurf_accounts:
                        print(t("no_saved_accounts_generic"))
                    else:
                        print(t("total_accounts_generic").format(len(windsurf_accounts)))
                        print(t("format_label"))
                        print("-" * 55)
                        
                        for acc in windsurf_accounts:
                            email = acc.get('email', 'N/A')
                            email_pass = acc.get('email_password', 'N/A')
                            windsurf_pass = acc.get('windsurf_password', 'N/A')
                            print(f"{email}:{email_pass}:{windsurf_pass}")
                        
                        print("-" * 55)
                        print(t("save_to_file"), end="")
                        save_choice = input().strip().lower()
                        
                        if save_choice == 'y':
                            export_file = ACCOUNTS_DIR / "accounts_export.txt"
                            with open(export_file, 'w', encoding='utf-8') as f:
                                f.write("# " + t("format_label"))
                                for acc in windsurf_accounts:
                                    email = acc.get('email', 'N/A')
                                    email_pass = acc.get('email_password', 'N/A')
                                    windsurf_pass = acc.get('windsurf_password', 'N/A')
                                    f.write(f"{email}:{email_pass}:{windsurf_pass}\n")
                            print(t("exported_to").format(export_file))
                except Exception as e:
                    print(t("read_error").format(e))
            
            input(t("press_enter_short"))
        
        else:
            print(t("invalid_choice"))
            time.sleep(1)


def change_language_menu():
    global CURRENT_LANG
    while True:
        clear_screen()
        print("="*55)
        print(" 🌐 Language / Язык")
        print("="*55)
        print("1) 🇷🇺 Русский")
        print("2) 🇬🇧 English")
        print("0) ⬅️  Back / Назад")
        print("="*55)
        print(f"Current / Текущий: {'Русский' if CURRENT_LANG == 'ru' else 'English'}")
        print("="*55)
        choice = input("Choose / Выбери: ").strip()
        
        if choice == "0":
            break
        elif choice == "1":
            save_language("ru")
            print("\n✅ Язык изменен на Русский")
            time.sleep(1)
            break
        elif choice == "2":
            save_language("en")
            print("\n✅ Language changed to English")
            time.sleep(1)
            break
        else:
            print("Invalid choice / Неверный выбор")
            time.sleep(1)

def menu():
    while True:
        clear_screen()
        print("="*55)
        print(t("main_menu_title"))
        print("="*55)
        print(f"1) {t('scan_data')}")
        print(f"2) {t('delete_data')}")
        print(f"3) {t('temp_mail')}")
        print(f"4) {t('register_auto')}")
        print(f"5) {t('view_accounts')}")
        print(f"6) {t('change_language')}")
        print(f"0) {t('exit')}")
        print("="*55)
        choice = input(t("choose_action")).strip()

        if choice == "0":
            print(t("exiting"))
            break
        elif choice == "1":
            items = find_windsurf_data()
            if not items:
                print(t("data_not_found"))
            else:
                print(t("found_items").format(len(items)))
                for p, s in items:
                    print(f" - {p} [{human_size(s)}]")
            input(t("press_enter"))
        elif choice == "2":
            items = find_windsurf_data()
            if not items:
                print(t("no_data_to_delete"))
            else:
                print(t("found_items_to_delete").format(len(items)))
                remove_targets(items)
            input(t("press_enter"))
        elif choice == "3":
            mail_tm_menu()
        elif choice == "4":
            register_windsurf_auto()
        elif choice == "5":
            view_accounts_menu()
        elif choice == "6":
            change_language_menu()
        else:
            print(t("invalid_choice"))
            time.sleep(1)


if __name__ == "__main__":
    LOGS_DIR.mkdir(exist_ok=True)
    ACCOUNTS_DIR.mkdir(exist_ok=True)
    
    if not LOG_FILE.exists():
        try:
            LOG_FILE.write_text("")
        except Exception:
            pass
    
    load_language()
    
    try:
        menu()
    except KeyboardInterrupt:
        print("\n" + ("Остановка пользователем." if CURRENT_LANG == "ru" else "Stopped by user."))
