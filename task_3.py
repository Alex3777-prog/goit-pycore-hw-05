import sys
from datetime import datetime


ALLOWED_LEVELS = {"INFO", "DEBUG", "ERROR", "WARNING"}


def parse_log_line(line: str) -> dict:
    """Parse and validate a single log entry."""
    date, time, level, message = line.split(maxsplit=3)

    if level not in ALLOWED_LEVELS:
        raise ValueError("Invalid log level")

    # Validate the date and time; no need to store the parsed datetime.
    datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M:%S")

    return dict(date=date, time=time, level=level, message=message)


def load_logs(file_path: str) -> list:
    """Load and parse log entries from a file."""
    logs = []

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            clean_line = line.strip()
            if not clean_line:
                continue

            logs.append(parse_log_line(clean_line))

    return logs


def filter_logs_by_level(logs: list, level: str) -> list:
    """Filter log entries by level, ignoring case."""
    return [log for log in logs if log['level'] == level.upper()]


def count_logs_by_level(logs: list) -> dict:
    """Count log entries for each logging level."""
    counts = {}

    for log in logs:
        level = log['level']
        if level in counts:
            counts[level] += 1
        else:
            counts[level] = 1

    return counts


def display_log_counts(counts: dict) -> None:
    """Display log level counts in a formatted table."""
    print(f"{'Рівень логування':<16} | Кількість")
    print(f"{'-' * 17}|{'-' * 10}")

    for key, value in counts.items():
        print(f"{key:<16} | {value}")


def main() -> None:
    """Run the log analyzer using command-line arguments."""
    if len(sys.argv) < 2:
        print("Incorrect file path")
        return

    file_path = sys.argv[1]

    # FileNotFoundError inherits OSError;
    # UnicodeDecodeError inherits ValueError.
    try:
        logs = load_logs(file_path)
    except FileNotFoundError:
        print("File not found!")
        return
    except UnicodeDecodeError:
        print("Unable to decode the file as UTF-8.")
        return
    except OSError as error:
        print(f"File reading error: {error}")
        return
    except ValueError:
        print("Incorrect log file format")
        return

    counts = count_logs_by_level(logs)
    display_log_counts(counts)

    if len(sys.argv) >= 3:
        level = sys.argv[2]
        filtered_logs = filter_logs_by_level(logs, level)

        print()
        print(f"Деталі логів для рівня '{level.upper()}':")
        for log in filtered_logs:
            print(f"{log['date']} {log['time']} - {log['message']}")


if __name__ == "__main__":
    main()
