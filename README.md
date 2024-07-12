# BPMN

> business process modeling and notation generation solution using crewai library.

> this repo contains the tasks to generate the bpmn.

## running the the tasks

### activate the venv

```bash

py -m venv ./venv

.\venv\Scripts\activate

pip install -r requirements.txt
```

### sync the packages

```bash
pip freeze > requirements.txt
```

### running some task example

```bash
py .\crews\pools\text-rewriting-for-better-understanding\main.py
```

## folders structure

- crews
  - pools
    - text-rewriting-for-better-understanding
  - activities

> the crews folder contains the components that we want to extract to generate bpmn each component folder contains the tasks to extract some stuff to generate bpmn.
