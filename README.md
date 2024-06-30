# Start

* This is my first game in the pygame. Because of that I have given this name to the project.

## Game Screenshots

![alt text](https://github.com/umutcanekinci/start/blob/main/images/samples/sample-1.png?raw=true)
![alt text](https://github.com/umutcanekinci/start/blob/main/images/samples/sample-2.png?raw=true)

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Requirments

To run the project, you will need the following:

- Python 3.x
- Required libraries (listed below)
    - pygame=2.5.2

### Installation

If you prefer to use the precompiled executable without installation, you can skip the setup and run the __main__.exe file directly.


Follow these steps to install the required libraries:

1. Clone this project:
    ```sh
    git clone https://github.com/umutcanekinci/start.git
    cd start
    ```

2. Create a virtual environment:
    ```sh
    python -m venv venv
    source venv/bin/activate # If you are using Windows: venv\Scripts\activate
    ```

3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

### Running the Game

To start the game, use the following command:
```sh
python __main__.py
```

## Gameplay

The objective of the game: 

* In every round, a player wiil be vampire and other one will be peasant randomly. Catch the peasant if you are the vampire, otherwise try to not be catched!
* The vampire is faster than peasants.
* Only the peasant can fire.
* I have not added an enemy ai so one player mode is not available. It should be added in future paths.
* I took musics and pictures from google searching without getting license, I know this is not legal. This is my first project so (I hope) this can be ignored.

#### Controls:

##### Player 1

* Move ==> ARROW KEYS

* Fire ==> CONTROL

##### Player 2

* Move ==> W, A, S, D

* Fire ==> SPACE

## Contributing

If you would like to contribute, please follow these steps:

1. Fork this repository (click the Fork button at the top right).

2. Clone your forked repository locally:
```sh
git clone https://github.com/umutcanekinci/start.git
cd start
```

3. Create a new branch (e.g., feature/new-feature):
```sh
git checkout -b feature/yenilik
```

4. Make your changes and commit them:
```sh
git commit -am 'Yeni özellik ekledim'
```

5. Push your changes to your branch on GitHub:
```sh
git push origin feature/yenilik
```

6. Create a pull request.

## Authors

Umutcan Ekinci - Developer


See also the list of <a href="https://github.com/umutcanekinci/start/contributors">contributors</a> who participated in this project.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

For questions or suggestions, feel free to contact me at umutcannekinci@gmail.com.
