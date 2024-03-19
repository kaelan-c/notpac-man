# !Pac-Man: Reinforcement Learning Workshop

## University of Lethbridge Computer Science Club

Welcome to the !Pac-Man Reinforcement Learning Workshop! This project is designed to introduce you to the fundamentals of reinforcement learning (RL) through the implementation of an AI agent that learns to play a Pac-Man-like game.

### Project Overview

!Pac-Man is a simplified version of the classic arcade game Pac-Man. In this workshop, you'll use reinforcement learning techniques to train an AI agent to navigate through a maze, eat dots, avoid ghosts, and try to score as high as possible. The game is built using Python and Pygame, offering a hands-on experience with a Q-Learning Agent implementation.

### Prerequisites

- Basic knowledge of Python programming (Not Required but nice to have).
- Familiarity with fundamental concepts in machine learning or AI is helpful but not required.
- Python 3.6 or higher installed on your system.
- Python Dependencies installed:
  - Pygame `pip install pygame`
  - Numpy `pip install numpy`
  - Pickle `pip install pickle-mixin`

### Getting Started

1. **Clone the Repository**: Clone this repository to your local machine using:
  -`git clone https://github.com/kaelan-c/notpac-man.git`
  or
  - Downloading the code directly as a zip file.

2. **Install Dependencies**: Ensure you have Python and the Dependencies installed on your system.

   ### For All Platforms:
   - **Install Python**: Ensure you have Python installed on your system. If not, download and install Python from [python.org](https://www.python.org/downloads/).

   ### For Mac:
   1. **Install Homebrew**: Homebrew is a package manager for macOS. Install it from [brew.sh](https://brew.sh/) if you don't already have it.
   2. **Install Python and Packages**:
      ```bash
      brew install python3
      pip3 install pygame numpy pickle-mixin
      ```

   ### For Linux:
   1. **Install Python**:
      - For Ubuntu/Debian-based systems:
        ```bash
        sudo apt update
        sudo apt install python3 python3-pip
        ```
      - For Fedora:
        ```bash
        sudo dnf install python3 python3-pip
        ```
      - For Arch Linux:
        ```bash
        sudo pacman -S python python-pip
        ```

   2. **Install Packages**:
      ```bash
      pip3 install pygame numpy pickle-mixin
      ```

   ### For Windows:
   1. **Install Python**:
      - Download the Python installer from [python.org](https://www.python.org/downloads/).
      - Run the installer. Ensure to check the box that says "Add Python to PATH" during installation.
   2. **Install Packages**:
      - Open Command Prompt (CMD) as an administrator.
      - Install the packages using pip:
        ```cmd
        pip install pygame numpy pickle-mixin
        ```

   ### Verification
   To verify that everything is installed correctly, you can run the following command in your terminal or command prompt:
   ```bash
   python -c "import pygame, numpy, pickle; print('Success')"
   ```
   If you see the word 'Success' without any errors, you have successfully installed the necessary dependencies.

3. **Explore the Code**: The project consists of several Python files that define the game environment, the AI agent, and the training script.
   - `game.py`: Contains the game logic and rendering for !Pac-Man.
   - `agent.py`: Defines the AI agent using Q-learning.
   - `train.py`: Script to train the AI agent.
   - Other game resource files like `gamemap.py`, `ghost.py`, etc.

4. **Train the AI**: To train the AI agent, run `python train.py`. This will start the training process, and you can observe how the AI learns over time.

5. **Run the Game**: You can run the game to see the non-AI version in action. Use `python main.py` to start.

### Workshop Goals

- **Understand Reinforcement Learning**: Grasp the basics of how reinforcement learning works.
- **Explore an AI Agent Implementation**: Learn how a basic Q-learning agent is implemented.
- **Experiment and Learn**: Experiment with different parameters, reward structures, and state representations to see how they affect the AI's learning process.

### Contributing

We welcome contributions and suggestions! Please feel free to fork the repository, make changes, and submit pull requests. If you find any issues or have ideas for improvements, don't hesitate to open an issue.
