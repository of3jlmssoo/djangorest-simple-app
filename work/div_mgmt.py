class Div_Mgmt():
    def __init__(self) -> None:
        self._div_info = ''
        self._port_info = ''

    @property
    def div_info(self):
        return self._div_info

    @div_info.setter
    def div_info(self, file_name):
        """ TODO: file_name確認。存在するか？ """
        self._div_info = file_name

    @property
    def port_info(self):
        return self._port_info

    @port_info.setter
    def port_info(self, file_name):
        """ TODO: file_name確認。存在するか？ """
        self._port_info = file_name


# i = Input_files()
# i.div_info = "/home/div.txt"
# i.port_info = "/home/port.txt"

# print(f'{i.div_info=} {i.port_info=}')
