import argparse
import logging
from rexec_server.server import RExecServer

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "broker_addr", type=str,
        help="The broker's address to connect."
    )

    parser.add_argument(
        "--broker_port", type=str, default="5560",
        help="The broker's port to connect. [0-65535]"
    )

    parser.add_argument(
        "--dspaces_api_addr", type=str,
        help="The DataSpaces API address to connect."
    )

    parser.add_argument(
        "-v", "--verbose",
        help="Be verbose",
        action="store_const", dest="loglevel", const=logging.INFO,
    )

    args = parser.parse_args()
    logging.basicConfig(level=args.loglevel)

    server = RExecServer(args)
    server.run()
