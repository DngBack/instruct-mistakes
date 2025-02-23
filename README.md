# Instruct Mistakes

Instruct Mistakes is an AI-powered tool that analyzes mistakes and provides step-by-step guidance to correct them, helping users learn and improve efficiently.

## Description

## To Do List

## Install and run

### Set up

#### Set up env

Using python 3.10.13

```bash
conda create -n instruct_mistakes python=3.10 -y

conda activate instruct_mistakes
```

#### Set up pre-commit to format code

    - Install:
    ```bash
    pip install pre-commit
    ```

    - Add pre-commit to git hook:
    ```bash
    pre-commit install
    ```

    - Run pre-commit for formating code (only staged files in git):
    ```bash
    pre-commit run
    ```

    - Run pre-commit for formating code with all files:
    ```bash
    pre-commit run --all-files

## Code Structure

backend/ (Main code in here)

exp/ (Testing in here)
