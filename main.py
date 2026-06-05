from parsing import parsing_file


def main() -> None:
    parsing_file("maps/easy/01_linear_path.txt")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
        exit()
