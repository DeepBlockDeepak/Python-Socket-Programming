class ConfigurationFileReader:

    def __init__(self, node_type, config_file):
        self.node_type = node_type
        self.config_file = config_file

    def parse_config(self):

        returned_config = []

        with open(self.config_file, 'r') as file:
            raw_message: list[str] = file.readlines()
            # raw_message = [line.rstrip() for line in file.readlines()]

        # *** Switch based on the Node ("NODE_A", "NODE_B", "NODE_C") ***#

        # case when NODE_A is the initialized node
        if self.node_type == "NODE_A":
            # obtain the port value for the Node B socket connection (convert to integer
            server_B_port: int = int(raw_message[0].rstrip())
            # obtain the remaining list of data lines
            node_A_data: list[str] = raw_message[1:]

            # store A's configuration information
            returned_config.extend([server_B_port, node_A_data])

        elif self.node_type == "NODE_B":
            client_A_port: int = int(raw_message[0].rstrip())
            server_C_port: int = int(raw_message[1].rstrip())
            node_C_data: list[str] = raw_message[2:]

            returned_config.extend([client_A_port, server_C_port, node_C_data])

        # self.node_type == "NODE_C"
        else:
            client_B_port: int = int(raw_message[0].rstrip())

            returned_config = client_B_port

        return returned_config

    def RepresentsInt(self, s):
        try:
            int(s)
            return True
        except ValueError:
            return False
