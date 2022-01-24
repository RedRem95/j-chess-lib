=====
Usage
=====

See here some examples to use this library.
For more detailed explanation see Usage_

Start
-----

See below for an example to start the client with your ai

.. code-block:: python

    from j_chess_lib.communication import Connection
    from j_chess_lib.client import Client
    from j_chess_lib.ai.Sample import SampleAI

    with Connection(server_address, server_port) as connection:
        ai = SampleAI()
        client = Client(connection=connection, ai=your_ai)
        client.start()
        client.join()

This example shows how to setup the connection and the client.
The client is its own thread so you could for example start multiple clients parallel or do some other stuff. Like a gui...

AI
--

See below for an example to implement a very easy AI.
It uses the base-class that automatically stores match and game data when started so you can query it in the move generation when needed

.. code-block:: python

    from uuid import UUID
    from j_chess_lib.ai import StoreAI
    from j_chess_lib.ai.Container import GameState
    from j_chess_lib.communication import MoveData

    class SampleAI(StoreAI):
        def __init__(self):
            super(SampleAI, self).__init__(name=f"Unique Name of your very good AI")

        def get_move(self, game_id: UUID, match_id: UUID, game_state: GameState) -> MoveData:
            enemy, match_data = self.get_match(match_id=match_id)
            white_player = self.get_game(game_id=game_id, match_id=match_id)

            # Your super intelligent code to generate the best chess move ever generated

            move_data = # result of your code
            return move_data

This example initializes a SampleAI
