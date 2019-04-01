import os
import colorama as cl
import sys
import argparse
import itertools


class OwlHex:
    def __init__(self):
        self.BEG_OF_PRINTABLE_BYTES = 0x20
        self.END_OF_PRINTABLE_BYTES = 0xFF
        return

    def hex_bytes_grouper(self, iterable, n=4, fill_value=0):
        """
        example: grouper('ABCDEF', 4, '0') --> ABCD EFxx
        :param iterable: the data to be grouped
        :param n: number of group member
        :param fill_value = fill value if padding to form groups
        :return: generator of hex byte converted line
        """
        group_bytes = [iter(iterable)] * n  # group the bytes into n
        return '-'.join(' '.join(format(byte, '0>2x') for byte in grp_bytes)
                        for grp_bytes in itertools.zip_longest(*group_bytes, fillvalue=fill_value))

    def bytes_to_ascii(self, iterable):
        return''.join(chr(x) if self.BEG_OF_PRINTABLE_BYTES <= x <= self.END_OF_PRINTABLE_BYTES else '.'
                      for x in iterable)

    def owl_hex_view(self, target_file, chunk_len=0x10):
        """
        notes:
        * ^ - center align, < - left align, > - right align
        :param target_file:
        :param chunk_len:
        :return:
        """
        print(cl.Fore.LIGHTWHITE_EX + "[+]FileName: {}".format(target_file))
        print(cl.Fore.LIGHTWHITE_EX + "[+]FileSize: {}\n".format(hex(os.path.getsize(target_file))))

        hdr = self.hex_bytes_grouper(range(chunk_len))
        print(cl.Fore.MAGENTA + "{0:^18} :       {1:<53}   ||   {2:<16}".format("FILE OFFSET", hdr, "ASCII"))
        print(cl.Fore.MAGENTA + "{}".format("-" * 100))


        with open(target_file, 'rb') as f:
            for line_num in itertools.count(0, chunk_len):
                byte_chunks = f.read(chunk_len)
                if byte_chunks:

                    # 0x{:0>16x} : => 0x0000000000000000 :
                    print(cl.Fore.GREEN + "0x{:0>16x} :".format(line_num), end="")
                    print(cl.Fore.YELLOW + "       {:<53}   ".format(self.hex_bytes_grouper(byte_chunks)), end="")
                    print(cl.Fore.LIGHTGREEN_EX + "||   {:<16}".format(self.bytes_to_ascii(byte_chunks)))

                else:
                    break
                    return

        return


def banner():
    print(cl.Fore.GREEN + """
   ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


      "_ _"                          _|  _|   |_|    "_ _"    _     _
      |-|-|    |_|      |_|     |_|  _|  _|   |_|    |-|-|   |_|   |_|
    |_|   |_|  |_|      |_|     |_|  _|  _|_|_|_|  |_|_|_|_|   |_|_|
    |_|   |_|    |_|  |_|  |_| |_|   _|  _|   |_|  |_|       |_|   |_|
      |_|_|        |_|      |_|      _|  _|   |_|   |_|_|_| |_|     |_|
       ""                                              ""
       "                                                "
                                   by:

                           teoderick.contreras

   ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    """)
    return


def is_windows():
    if os.name == 'nt':
        return True
    else:
        return False


def ask_input():
    parser = argparse.ArgumentParser(description="commandline hex viewer")
    parser.add_argument('-f', '--target_file',help="file to be in hex view", required=True)

    args = vars(parser.parse_args())
    target_file = args['target_file']
    return target_file


def clear_screen():
    win_flag = is_windows()
    if win_flag:
        os.system('cls')
    else:
        os.system('clear')


def main():
    cl.init(autoreset=True)
    clear_screen()
    banner()
    target_file = ask_input()
    o = OwlHex()
    o.owl_hex_view(target_file)

    return


if __name__ == "__main__":
    main()
