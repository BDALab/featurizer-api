import argparse
from api import prepare_app


def main(host, port, debug=False):
    """
    Runs the API.

    :param host: hostname or ip address to listen on
    :type host: str
    :param port: port of the web-server
    :type port: int
    :param debug: debug mode, defaults to False
    :type debug: bool, optional
    :return: None
    :rtype: None type
    """

    # Featurizer API initialization
    app = prepare_app(__name__)

    # Featurizer API start
    app.run(host=host, port=port, debug=debug)


if __name__ == "__main__":

    # Prepare the command line arguments
    parser = argparse.ArgumentParser(description="Featurizer API")
    parser.add_argument("--host", help="the hostname to listen on (defaults to '0.0.0.0')", type=str)
    parser.add_argument("--port", help="the port of the web-server (defaults to 5000)", type=int)
    parser.add_argument("--debug", help="debug run", action="store_true")

    # Parse the command line arguments
    args = parser.parse_args()

    # Prepare the default args
    host_ = args.host if args.host else "0.0.0.0"
    port_ = args.port if args.port else 5000
    debug_ = True if args.debug else False

    # Run the API
    main(host=host_, port=port_, debug=debug_)
