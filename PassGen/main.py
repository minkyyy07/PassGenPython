import string
import secrets
import argparse
import sys
import subprocess
import random


class PasswordGenerator:
    @staticmethod
    def gen_sequence(
        conditions,
    ):  # must have  conditions (in a list format), for each member of the list possible_characters
        possible_characters = [
            string.ascii_lowercase,
            string.ascii_uppercase,
            string.digits,
            string.punctuation,
        ]
        sequence = ""
        for x in range(len(conditions)):
            if conditions[x]:
                sequence += possible_characters[x]
            else:
                pass
        return sequence

    @staticmethod
    def gen_password(sequence, length=8, pools=None, require_each=False):
        if not sequence:
            return ""
        if not require_each or not pools:
            return "".join(secrets.choice(sequence) for _ in range(length))
        # Ensure at least one from each enabled pool
        enabled_pools = [p for p in (pools or []) if p]
        if not enabled_pools:
            return ""
        if length < len(enabled_pools):
            # Fallback: not enough length to satisfy constraint
            return "".join(secrets.choice(sequence) for _ in range(length))
        chars = [secrets.choice(p) for p in enabled_pools]
        remaining = length - len(chars)
        chars += [secrets.choice(sequence) for _ in range(remaining)]
        random.SystemRandom().shuffle(chars)
        return "".join(chars)


class Interface:
    has_characters = {
        "lowercase": True,
        "uppercase": True,
        "digits": True,
        "punctuation": True,
    }
    exclude_chars = ""
    no_similar = False
    require_each = False
    count = 1
    last_password = None

    @classmethod
    def change_has_characters(cls, change):
        try:
            cls.has_characters[
                change
            ]  # to check if the specified key exists in the dicitonary
        except Exception as err:
            print(f"Invalid \nan Exception: {err}")
        else:
            cls.has_characters[change] = not cls.has_characters[
                change
            ]  # automaticly changres to the oppesite value already there
            print(f"{change} is now set to {cls.has_characters[change]}")

    @classmethod
    def show_has_characters(cls):
        print(cls.has_characters)  # print the output
        print(
            {
                "exclude": cls.exclude_chars,
                "no_similar": cls.no_similar,
                "require_each": cls.require_each,
                "count": cls.count,
            }
        )

    def build_sequence_and_pools(self):
        # Build pools by each category for require_each feature
        pools = []
        if self.has_characters["lowercase"]:
            pools.append(string.ascii_lowercase)
        else:
            pools.append("")
        if self.has_characters["uppercase"]:
            pools.append(string.ascii_uppercase)
        else:
            pools.append("")
        if self.has_characters["digits"]:
            pools.append(string.digits)
        else:
            pools.append("")
        if self.has_characters["punctuation"]:
            pools.append(string.punctuation)
        else:
            pools.append("")

        # Merge pools
        sequence = "".join(pools)

        # Remove similar characters if requested
        if Interface.no_similar:
            similar = set("O0oIl1|")
            sequence = "".join(ch for ch in sequence if ch not in similar)
            pools = ["".join(ch for ch in p if ch not in similar) for p in pools]

        # Exclude custom characters
        if Interface.exclude_chars:
            excl = set(Interface.exclude_chars)
            sequence = "".join(ch for ch in sequence if ch not in excl)
            pools = ["".join(ch for ch in p if ch not in excl) for p in pools]

        return sequence, pools

    def generate_password(self, length):
        sequence, pools = self.build_sequence_and_pools()
        if not sequence:
            print("No character sets selected. Please enable at least one of: lowercase, uppercase, digits, punctuation.")
            return
        try:
            length = int(length)
        except Exception:
            print("Length must be a number.")
            return
        if length <= 0:
            print("Length must be positive.")
            return
        for i in range(Interface.count):
            pwd = PasswordGenerator.gen_password(
                sequence, length, pools=pools, require_each=Interface.require_each
            )
            print(pwd)
            Interface.last_password = pwd
        # Clipboard copy if requested
        if CLIContext.copy_to_clipboard and Interface.last_password:
            copy_to_clipboard(Interface.last_password)


def list_to_vertical_string(list):
    to_return = ""
    for member in list:
        to_return += f"{member}\n"
    return to_return


class Run:
    def prompt_yes_no(self, question: str, default: bool = True) -> bool:
        yn = "Y/n" if default else "y/N"
        while True:
            ans = input(f"{question} [{yn}]: ").strip().lower()
            if ans == "":
                return default
            if ans in ("y", "yes"):
                return True
            if ans in ("n", "no"):
                return False
            print("Введите 'y' или 'n'.")

    def prompt_int(self, question: str, min_value: int = 1, default: int | None = None) -> int:
        while True:
            suffix = f" (по умолчанию {default})" if default is not None else ""
            ans = input(f"{question}{suffix}: ").strip()
            if ans == "" and default is not None:
                return default
            try:
                value = int(ans)
                if value < min_value:
                    print(f"Число должно быть >= {min_value}.")
                    continue
                return value
            except Exception:
                print("Введите целое число.")

    def prompt_str(self, question: str, default: str = "") -> str:
        ans = input(f"{question} (Enter чтобы пропустить): ").strip()
        return ans if ans != "" else default

    def wizard(self):
        print("Добро пожаловать в PassGen — мастер настройки пароля.\nОтветьте на вопросы по очереди, затем мы сгенерируем пароль.")

        while True:
            # 1) Наборы символов
            use_lower = self.prompt_yes_no("Использовать строчные буквы (a-z)?", default=Interface.has_characters["lowercase"])
            use_upper = self.prompt_yes_no("Использовать заглавные буквы (A-Z)?", default=Interface.has_characters["uppercase"])
            use_digits = self.prompt_yes_no("Использовать цифры (0-9)?", default=Interface.has_characters["digits"])
            use_punct  = self.prompt_yes_no("Использовать знаки препинания (символы)?", default=Interface.has_characters["punctuation"])
            if not any([use_lower, use_upper, use_digits, use_punct]):
                print("Нужно выбрать хотя бы один набор символов. Попробуйте снова.\n")
                continue

            # 2) Исключить похожие символы
            no_similar = self.prompt_yes_no("Исключить похожие символы (O,0,o,I,l,1,|)?", default=Interface.no_similar)

            # 3) Исключить конкретные символы
            exclude = self.prompt_str("Введите символы, которые нужно исключить")

            # 4) Требовать минимум по одному из каждого включённого набора
            require_each = self.prompt_yes_no("Гарантировать хотя бы один символ из каждого выбранного набора?", default=Interface.require_each)

            # 5) Длина
            length = self.prompt_int("Введите длину пароля", min_value=1, default=12)

            # 6) Количество
            count = self.prompt_int("Сколько паролей сгенерировать", min_value=1, default=1)

            # 7) Копировать в буфер обмена
            copy_last = self.prompt_yes_no("Скопировать последний пароль в буфер обмена?", default=False)

            # Резюме
            print("\nИтоговые настройки:")
            print({
                "lowercase": use_lower,
                "uppercase": use_upper,
                "digits": use_digits,
                "punctuation": use_punct,
                "no_similar": no_similar,
                "exclude": exclude,
                "require_each": require_each,
                "length": length,
                "count": count,
                "copy": copy_last,
            })
            if not self.prompt_yes_no("Подтвердить и сгенерировать?", default=True):
                if self.prompt_yes_no("Перезапустить мастер?", default=True):
                    print("")
                    continue
                else:
                    print("Выход...")
                    raise SystemExit(0)

            # Применяем настройки и генерируем
            Interface.has_characters["lowercase"] = use_lower
            Interface.has_characters["uppercase"] = use_upper
            Interface.has_characters["digits"] = use_digits
            Interface.has_characters["punctuation"] = use_punct
            Interface.no_similar = no_similar
            Interface.exclude_chars = exclude
            Interface.require_each = require_each
            Interface.count = count
            CLIContext.copy_to_clipboard = copy_last

            Interface().generate_password(length)

            # После генерации: повторить / начать заново / выйти
            print("")
            again = input("Сгенерировать снова с теми же настройками (y), начать заново (r), или выйти (q)? [y/r/q]: ").strip().lower()
            if again == "y" or again == "":
                Interface().generate_password(length)
                print("")
                continue
            elif again == "r":
                print("")
                continue
            else:
                print("Выход...")
                raise SystemExit(0)

    def decide_operation(self):
        user_input = input(": ").strip()
        if user_input.lower() in ("q", "quit", "exit"):
            print("Exiting...")
            raise SystemExit(0)
        if user_input.lower() in ("help", "h"):
            self.print_help()
            return
        if user_input.lower() == "show":
            Interface.show_has_characters()
            return
        if user_input.lower().startswith("exclude "):
            Interface.exclude_chars = user_input.split(" ", 1)[1]
            print(f"Exclude set updated: {Interface.exclude_chars!r}")
            return
        if user_input.lower() == "nosimilar":
            Interface.no_similar = not Interface.no_similar
            print(f"no_similar is now set to {Interface.no_similar}")
            return
        if user_input.lower() == "require":
            Interface.require_each = not Interface.require_each
            print(f"require_each is now set to {Interface.require_each}")
            return
        if user_input.lower().startswith("count "):
            try:
                Interface.count = max(1, int(user_input.split(" ", 1)[1]))
                print(f"count is now set to {Interface.count}")
            except Exception:
                print("Usage: count <number>")
            return
        if user_input.lower() == "copy":
            if Interface.last_password:
                copy_to_clipboard(Interface.last_password)
            else:
                print("No password to copy yet.")
            return
        try:
            int(user_input)
        except:
            Interface.change_has_characters(user_input)
        else:
            Interface().generate_password(int(user_input))
        finally:
            print("\n\n")

    def manual_run(self):
        menu = f"""Welcome to the PassGen App (manual mode)!
Interactive usage:
    - Enter a number to generate a password of that length (e.g., 12)
    - Enter one of the following words to toggle that character set on/off:
{list_to_vertical_string(Interface.has_characters.keys())}
    - Commands: show, exclude <chars>, nosimilar, require, count <n>, copy, help, q

CLI (non-interactive) examples:
    - python main.py -n 12
    - python main.py -n 16 --lower --upper  # only lowercase + uppercase
    - python main.py -n 12 -c 5 --no-similar --require-each --copy
"""
        print(menu)
        while True:
            self.decide_operation()

    def run(self):
        # По умолчанию запускаем мастер. Для старого режима наберите 'manual'.
        choice = input("Запустить мастер настройки (Enter) или ввести команды вручную (manual)? ").strip().lower()
        if choice == "manual":
            self.manual_run()
        else:
            self.wizard()

    def print_help(self):
        print(
            "Commands: show | exclude <chars> | nosimilar | require | count <n> | copy | q"
        )

class CLIContext:
    copy_to_clipboard = False


def copy_to_clipboard(text: str):
    try:
        if sys.platform == "darwin":
            subprocess.run(["pbcopy"], input=text, text=True, check=True)
            print("Copied to clipboard.")
        elif sys.platform.startswith("linux"):
            # Try xclip or wl-copy if available
            for cmd in ("xclip -selection clipboard", "wl-copy"):
                try:
                    subprocess.run(cmd.split(), input=text, text=True, check=True)
                    print("Copied to clipboard.")
                    return
                except Exception:
                    continue
            print("Clipboard copy not available. Install xclip or wl-clipboard.")
        elif sys.platform.startswith("win"):
            subprocess.run(["clip"], input=text, text=True, check=True)
            print("Copied to clipboard.")
        else:
            print("Clipboard copy not supported on this platform.")
    except Exception as e:
        print(f"Clipboard error: {e}")


def main():
    parser = argparse.ArgumentParser(description="PassGen - Password Generator")
    parser.add_argument("-n", "--length", type=int, help="Password length for non-interactive mode")
    parser.add_argument("-c", "--count", type=int, default=1, help="How many passwords to generate in non-interactive mode")
    parser.add_argument("--lower", action="store_true", help="Include lowercase in non-interactive mode")
    parser.add_argument("--upper", action="store_true", help="Include uppercase in non-interactive mode")
    parser.add_argument("--digits", action="store_true", help="Include digits in non-interactive mode")
    parser.add_argument("--punct", action="store_true", help="Include punctuation in non-interactive mode")
    parser.add_argument("--no-similar", action="store_true", help="Exclude similar-looking characters (O,0,o,I,l,1,|)")
    parser.add_argument("--exclude", type=str, default="", help="Characters to exclude (e.g., !@#$0OIl1)")
    parser.add_argument("--require-each", action="store_true", help="Require at least one character from each enabled set")
    parser.add_argument("--copy", action="store_true", help="Copy the last generated password to clipboard")
    args = parser.parse_args()

    # Configure selected character sets if any are specified for CLI mode
    if any([args.lower, args.upper, args.digits, args.punct]):
        Interface.has_characters["lowercase"] = args.lower
        Interface.has_characters["uppercase"] = args.upper
        Interface.has_characters["digits"] = args.digits
        Interface.has_characters["punctuation"] = args.punct

    # Extra CLI toggles
    Interface.exclude_chars = args.exclude or ""
    Interface.no_similar = args.no_similar
    Interface.require_each = args.require_each
    Interface.count = max(1, int(args.count or 1))
    CLIContext.copy_to_clipboard = args.copy

    if args.length:
        Interface().generate_password(args.length)
        return

    # Fallback to interactive mode
    try:
        Run().run()
    except (EOFError, KeyboardInterrupt, SystemExit):
        print("\nBye.")


if __name__ == "__main__":
    main()