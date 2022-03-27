=======
History
=======

0.0.1 (2022-01-23)
------------------

* Engage in Project

0.1.0 (2022-01-24)
------------------

* Implemented basic api. Still some features to do

0.2.0 (2022-01-24)
------------------

* Added more docu
* Added readthedocs build config

0.2.4 (2022-01-24)
------------------

* Fixed setup.py so it automatically loads xsd and installs classes based on them

0.7.0 (2022-03-10)
------------------

* Added tournament code to client

0.7.3 (2022-03-20)
------------------

* Implemented error messages on not supported messages
* Fixed client not loading completed message when delay between packages is too big

0.8.0 (2022-03-20)
------------------

* Added method to check if move results in the new board you beeing in chess

0.9.0 (2022-03-21)
------------------

* Implemented Example AI that replays a loaded PGN. Automatically selects "path" from pgn matching player color

0.9.1 (2022-03-26)
------------------

* Is promotion Method now returns False on non valid moves

0.10.0 (2022-03-26)
-------------------

* Added methods to predict boards and create fen notation from boards

0.10.2 (2022-03-26)
-------------------

* Fixed pgn analysis when white moved last

0.10.3 (2022-03-27)
-------------------

* Fixed bug in PGNPlayer with empty pgn
