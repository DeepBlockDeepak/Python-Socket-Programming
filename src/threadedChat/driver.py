from configuration_file_reader import ConfigurationFileReader
from client import Client


if __name__ == "__main__":

    node_A = ConfigurationFileReader("NODE_A", "testA.txt")
    node_B = ConfigurationFileReader("NODE_B", "testB.txt")
    node_C = ConfigurationFileReader("NODE_C", "testC.txt")

    port_A_to_B, msg_A_to_B = node_A.parse_config()
    port_B_to_A, port_B_to_C, msg_B_to_A = node_B.parse_config()
    port_C_to_B = node_C.parse_config()

    print(f"port A to B = {port_A_to_B}\nmsg from A to B = {msg_A_to_B}", end="\n---\n")
    print(f"port B to A = {port_B_to_A}\nport B to C = {port_B_to_C}\nmsg from B to C = {msg_B_to_A}", end="\n---\n")
    print(f"port C to B = {port_C_to_B}")


