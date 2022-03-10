if __name__ == "__main__":
    import logging

    logger = logging.getLogger("j_chess_lib")
    logger.setLevel(logging.DEBUG)

    from j_chess_lib.communication import Connection
    from j_chess_lib.client import Client
    from j_chess_lib.ai.examples import Random
    from uuid import uuid4

    with Connection("localhost", 5123) as connection1:
        with Connection("localhost", 5123) as connection2:
            ai1 = Random("RNJesus", min_turn_time=1)
            ai2 = Random("RNJesus the second", min_turn_time=1)

            tournament_code = str(uuid4())

            logger.info(f"Will start the tournament {tournament_code}")

            client1 = Client(connection=connection1, ai=ai1, tournament_code=tournament_code)
            client2 = Client(connection=connection2, ai=ai2, tournament_code=tournament_code)

            client1.start()
            logger.info("Client1 started")
            client2.start()
            logger.info("Client2 started")

            client1.join()
            logger.info("Client1 finished")
            client2.join()
            logger.info("Client2 finished")
