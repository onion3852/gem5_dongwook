# dongwook start
tick_gap = [0]
# dongwook end

# Turn .bin to .txt
def binary_to_text(input_file_path, output_file_path):
    try:
        with open(input_file_path, "rb") as binary_file, open(
            output_file_path, "w"
        ) as text_file:
            # Read binary data
            binary_data = binary_file.read()

            # Convert binary data to hexadecimal representation
            hex_representation = " ".join(
                format(byte, "02x") for byte in binary_data
            )

            # Split the hexadecimal representation into chunks of 16 bytes
            hex_chunks = [
                hex_representation[i : i + 48]
                for i in range(0, len(hex_representation), 48)
            ]

            # Join the chunks with line breaks and write to the output file
            text_data = "\n".join(hex_chunks)
            text_file.write(text_data)

        print("Conversion success!")
    except Exception as e:
        print(f"Error: {e}")


# Turn character to Hex
# ex) 'a' -> 10
def char_to_hex(input_char):
    ascii_num = ord(input_char)
    dec_num = 0

    if (ascii_num >= 48) & (ascii_num <= 57):  # 0~9
        hex_num = ascii_num - 48
    elif (ascii_num >= 97) & (ascii_num <= 102):  # a~f
        hex_num = ascii_num - 87
    else:
        print("Error: Wrong ascii number. Program failed")
        exit()

    return hex_num


# Decode informations -> {command(r/w)},{address(Hex)},{size(bytes)},{tick(decimal)}
def extract(input_file_path, output_file_path, size):
    try:
        with open(input_file_path, "r") as text_file, open(
            output_file_path, "w"
        ) as output_file:
            # dongwook start
            with open("tick_gap.txt", "w") as file:
                # dongwok end
                for line in text_file:
                    # Split the line into columns
                    columns = line.split()
                    # column 0  : len
                    # column 1~4: address
                    # column 5~8: command type(r/w) + tick
                    # column 9~ : garbage

                    # Extract address (column 1~4)
                    address = "".join(columns[4:0:-1])
                    address = list(address)
                    address[0] = "8"
                    address = "".join((address))

                    # Extract "command + tick" (column 5~8)
                    command_tick = "".join(columns[8:4:-1])
                    command_tick = list(command_tick)
                    for i in range(0, 8):
                        command_tick[i] = format(
                            char_to_hex(command_tick[i]), "04b"
                        )

                    # Decoding command (Read or Write)
                    command = "-"
                    if command_tick[0].startswith("1"):
                        command = "w"
                    elif command_tick[0].startswith("0"):
                        command = "r"

                    # Tick to Decimal
                    command_tick = "".join(command_tick[0:9])
                    command_tick = list(command_tick)
                    tick_str = command_tick[1:]
                    tick = 0
                    for item in tick_str:
                        tick += ord(item) - 48
                        tick *= 2
                    tick //= 2
                    # tick *= 3125
                    # dongwook start
                    tick_gap.append(tick - sum(tick_gap))
                    file.write(str(tick_gap[-1]) + "\n")
                    # dongwook end

                    # Write the extracted information to the output file
                    output_file.write(f"{command},{address},{size},{tick}\n")
        print("Extraction success!")
        # dongwook start
        print("minimum gap between tick: ", min(tick_gap))
        print("maximun gap between tick: ", max(tick_gap))
        print("average gap between tick: ", sum(tick_gap) / len(tick_gap))
        # dongwook end
    except Exception as e:
        print(f"Error: {e}")
