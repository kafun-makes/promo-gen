import json
import random
import string
import os
from datetime import datetime

# Название файла для сохранения настроек
SETTINGS_FILE = 'promo_settings.json'
PROMO_HISTORY_FILE = 'promo_history.json'

def load_settings():
    """Загрузка настроек из JSON файла"""
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, KeyError):
            return {}
    return {}

def save_settings(language, promo_config):
    """Сохранение настроек в JSON файл"""
    settings = {
        'language': language,
        'promo_config': promo_config,
        'last_used': datetime.now().isoformat()
    }
    with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
        json.dump(settings, f, ensure_ascii=False, indent=4)

def save_promo_history(promo_codes):
    """Сохранение истории промокодов"""
    history = load_promo_history()
    timestamp = datetime.now().isoformat()
    
    for code in promo_codes:
        history.append({
            'code': code,
            'generated_at': timestamp
        })
    
    with open(PROMO_HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=4)

def load_promo_history():
    """Загрузка истории промокодов"""
    if os.path.exists(PROMO_HISTORY_FILE):
        try:
            with open(PROMO_HISTORY_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, KeyError):
            return []
    return []

def generate_promo_part(length, use_letters=True, use_digits=True, prefix="", suffix=""):
    """Генерация части промокода"""
    characters = ""
    if use_letters:
        characters += string.ascii_uppercase
    if use_digits:
        characters += string.digits
    
    if not characters:
        characters = string.ascii_uppercase + string.digits
    
    part = ''.join(random.choice(characters) for _ in range(length))
    return prefix + part + suffix

def generate_promo_code(config):
    """Генерация полного промокода на основе конфигурации"""
    parts = []
    for part_config in config['parts']:
        part = generate_promo_part(
            length=part_config['length'],
            use_letters=part_config.get('use_letters', True),
            use_digits=part_config.get('use_digits', True),
            prefix=part_config.get('prefix', ''),
            suffix=part_config.get('suffix', '')
        )
        parts.append(part)
    
    return config['separator'].join(parts)

def get_language():
    """Выбор языка"""
    print("=" * 50)
    print("Выберите язык / Choose language:")
    print("1. Русский")
    print("2. English")
    print("=" * 50)
    
    while True:
        choice = input("Введите номер / Enter number (1 или 2): ").strip()
        if choice == '1':
            return 'ru'
        elif choice == '2':
            return 'en'
        else:
            print("Неверный выбор. Пожалуйста, введите 1 или 2 / Invalid choice. Please enter 1 or 2")

def get_promo_config(language):
    """Настройка конфигурации промокодов"""
    if language == 'ru':
        # Запрос количества частей
        while True:
            try:
                parts_count = int(input("Сколько частей в промокоде? (например: 3 для XXX-YYY-ZZZ): "))
                if 1 <= parts_count <= 10:
                    break
                else:
                    print("Введите число от 1 до 10")
            except ValueError:
                print("Пожалуйста, введите число")
        
        # Запрос разделителя
        separator = input("Введите разделитель (например: - или _ или пробел): ").strip()
        if not separator:
            separator = "-"
        
        # Настройка каждой части
        parts = []
        for i in range(parts_count):
            print(f"\n--- Настройка части {i+1} ---")
            
            # Длина части
            while True:
                try:
                    length = int(input(f"Длина части {i+1}: "))
                    if 1 <= length <= 20:
                        break
                    else:
                        print("Длина должна быть от 1 до 20")
                except ValueError:
                    print("Пожалуйста, введите число")
            
            # Использование букв
            use_letters_input = input("Использовать буквы? (да/нет): ").lower().strip()
            use_letters = use_letters_input in ['да', 'д', 'yes', 'y', '']
            
            # Использование цифр
            use_digits_input = input("Использовать цифры? (да/нет): ").lower().strip()
            use_digits = use_digits_input in ['да', 'д', 'yes', 'y', '']
            
            # Префикс и суффикс
            prefix = input("Префикс (необязательно): ").strip()
            suffix = input("Суффикс (необязательно): ").strip()
            
            parts.append({
                'length': length,
                'use_letters': use_letters,
                'use_digits': use_digits,
                'prefix': prefix,
                'suffix': suffix
            })
        
        return {
            'parts': parts,
            'separator': separator
        }
    
    else:  # English
        # Get number of parts
        while True:
            try:
                parts_count = int(input("How many parts in promo code? (e.g., 3 for XXX-YYY-ZZZ): "))
                if 1 <= parts_count <= 10:
                    break
                else:
                    print("Please enter a number from 1 to 10")
            except ValueError:
                print("Please enter a number")
        
        # Get separator
        separator = input("Enter separator (e.g., - or _ or space): ").strip()
        if not separator:
            separator = "-"
        
        # Configure each part
        parts = []
        for i in range(parts_count):
            print(f"\n--- Configuring part {i+1} ---")
            
            # Part length
            while True:
                try:
                    length = int(input(f"Length of part {i+1}: "))
                    if 1 <= length <= 20:
                        break
                    else:
                        print("Length must be from 1 to 20")
                except ValueError:
                    print("Please enter a number")
            
            # Use letters
            use_letters_input = input("Use letters? (yes/no): ").lower().strip()
            use_letters = use_letters_input in ['yes', 'y', 'да', 'д', '']
            
            # Use digits
            use_digits_input = input("Use digits? (yes/no): ").lower().strip()
            use_digits = use_digits_input in ['yes', 'y', 'да', 'д', '']
            
            # Prefix and suffix
            prefix = input("Prefix (optional): ").strip()
            suffix = input("Suffix (optional): ").strip()
            
            parts.append({
                'length': length,
                'use_letters': use_letters,
                'use_digits': use_digits,
                'prefix': prefix,
                'suffix': suffix
            })
        
        return {
            'parts': parts,
            'separator': separator
        }

def show_current_config(config, language):
    """Показать текущую конфигурацию"""
    if language == 'ru':
        print("\n--- Текущая конфигурация ---")
        print(f"Разделитель: '{config['separator']}'")
        print("Части промокода:")
        for i, part in enumerate(config['parts'], 1):
            chars = []
            if part.get('use_letters', True):
                chars.append("буквы")
            if part.get('use_digits', True):
                chars.append("цифры")
            prefix_suffix = []
            if part.get('prefix'):
                prefix_suffix.append(f"префикс: '{part['prefix']}'")
            if part.get('suffix'):
                prefix_suffix.append(f"суффикс: '{part['suffix']}'")
            
            print(f"  Часть {i}: длина {part['length']} ({', '.join(chars)}) {', '.join(prefix_suffix)}")
    else:
        print("\n--- Current Configuration ---")
        print(f"Separator: '{config['separator']}'")
        print("Promo code parts:")
        for i, part in enumerate(config['parts'], 1):
            chars = []
            if part.get('use_letters', True):
                chars.append("letters")
            if part.get('use_digits', True):
                chars.append("digits")
            prefix_suffix = []
            if part.get('prefix'):
                prefix_suffix.append(f"prefix: '{part['prefix']}'")
            if part.get('suffix'):
                prefix_suffix.append(f"suffix: '{part['suffix']}'")
            
            print(f"  Part {i}: length {part['length']} ({', '.join(chars)}) {', '.join(prefix_suffix)}")

def main():
    """Основная функция"""
    # Загрузка настроек
    settings = load_settings()
    
    # Если язык не сохранен, запрашиваем его и настройки промокодов
    if 'language' not in settings:
        language = get_language()
        print("\n" + "="*50)
        if language == 'ru':
            print("Настройка формата промокодов")
        else:
            print("Promo code format configuration")
        print("="*50)
        
        promo_config = get_promo_config(language)
        save_settings(language, promo_config)
        
        if language == 'ru':
            print("✓ Настройки сохранены")
        else:
            print("✓ Settings saved")
    else:
        language = settings['language']
        promo_config = settings.get('promo_config', {
            'parts': [{'length': 4, 'use_letters': True, 'use_digits': True}],
            'separator': '-'
        })
    
    # Тексты на разных языках
    texts = {
        'ru': {
            'welcome': "=== Генератор промокодов ===",
            'enter_count': "Сколько промокодов нужно сгенерировать? ",
            'invalid_number': "Пожалуйста, введите целое положительное число!",
            'generated': "Сгенерированные промокоды:",
            'continue': "\nХотите сгенерировать еще промокоды? (да/нет): ",
            'reconfigure': "Хотите изменить настройки промокодов? (да/нет): ",
            'goodbye': "До свидания!",
            'error': "Ошибка:",
            'total_generated': "Всего сгенерировано:",
            'history_saved': "Промокоды сохранены в историю",
            'regenerating': "Перенастройка формата промокодов..."
        },
        'en': {
            'welcome': "=== Promo Code Generator ===",
            'enter_count': "How many promo codes to generate? ",
            'invalid_number': "Please enter a positive integer!",
            'generated': "Generated promo codes:",
            'continue': "\nGenerate more promo codes? (yes/no): ",
            'reconfigure': "Do you want to change promo code settings? (yes/no): ",
            'goodbye': "Goodbye!",
            'error': "Error:",
            'total_generated': "Total generated:",
            'history_saved': "Promo codes saved to history",
            'regenerating': "Reconfiguring promo code format..."
        }
    }
    
    t = texts[language]
    
    print(f"\n{t['welcome']}")
    print(f"{t['total_generated']} {len(load_promo_history())}")
    show_current_config(promo_config, language)
    
    while True:
        try:
            # Запрос на изменение настроек
            reconfigure = input(f"\n{t['reconfigure']}").lower().strip()
            if (language == 'ru' and reconfigure in ['да', 'д', 'yes', 'y']) or \
               (language == 'en' and reconfigure in ['yes', 'y', 'да', 'д']):
                print(t['regenerating'])
                promo_config = get_promo_config(language)
                save_settings(language, promo_config)
                show_current_config(promo_config, language)
            
            # Запрос количества промокодов
            count_input = input(f"\n{t['enter_count']}")
            count = int(count_input)
            
            if count <= 0:
                print(t['invalid_number'])
                continue
            
            # Генерация промокодов
            promo_codes = []
            for i in range(count):
                promo_code = generate_promo_code(promo_config)
                promo_codes.append(promo_code)
            
            # Сохранение в историю
            save_promo_history(promo_codes)
            
            # Вывод результатов
            print(f"\n{t['generated']}")
            for i, code in enumerate(promo_codes, 1):
                print(f"{i}. {code}")
            
            print(f"✓ {t['history_saved']}")
            
            # Запрос на продолжение
            continue_choice = input(t['continue']).lower().strip()
            if (language == 'ru' and continue_choice not in ['да', 'д', 'yes', 'y']) or \
               (language == 'en' and continue_choice not in ['yes', 'y', 'да', 'д']):
                print(t['goodbye'])
                break
                
        except ValueError:
            print(t['invalid_number'])
        except KeyboardInterrupt:
            print(f"\n{t['goodbye']}")
            break
        except Exception as e:
            print(f"{t['error']} {e}")

if __name__ == "__main__":
    main()