if __name__ == "__main__":
    import logging

    logger = logging.getLogger("j_chess_lib")
    logger.setLevel(logging.DEBUG)

    from j_chess_lib.communication import Connection
    from j_chess_lib.client import Client
    from j_chess_lib.ai.examples import Random, PGNPlayer

    rng_game = True

    with Connection("localhost", 5123) as connection1:
        with Connection("localhost", 5123) as connection2:
            timeout = 0
            if rng_game:
                ai1 = Random("RNJesus", min_turn_time=timeout)
                ai2 = Random("RNJudas", min_turn_time=timeout)
            else:
                ai1 = PGNPlayer(pgn="game.pgn", name="Pager")
                ai2 = PGNPlayer(pgn="game.pgn", name="Paginator")

            client1 = Client(connection=connection1, ai=ai1)
            client2 = Client(connection=connection2, ai=ai2)

            client1.start()
            logger.info("Client1 started")
            client2.start()
            logger.info("Client2 started")

            client1.join()
            logger.info("Client1 finished")
            client2.join()
            logger.info("Client2 finished")
