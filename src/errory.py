def find_problematic_character(filepath, encoding='cp1250'):
    try:
        with open(filepath, 'r', encoding=encoding) as file:
            file.read()
    except UnicodeDecodeError as e:
        position = e.start
        print(f"Problematic character in file {filepath} at position {position}:")
        with open(filepath, 'rb') as file:  # Open in binary mode to inspect raw bytes
            file.seek(position)
            raw_byte = file.read(1)
            print(f"Raw byte: {raw_byte}, Possible character: {raw_byte.decode('latin1', errors='ignore')}")


find_problematic_character('../data/O2_clenove_oddily_2017.csv', encoding='cp1250')
find_problematic_character('../data/S2_clenove_strediska_zvoj_2022.csv', encoding='cp1250')
# Add other files as needed
