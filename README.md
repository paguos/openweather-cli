# openweather-cli
A CLI to interact with the OpenWeather API.

## Installation (macOS)
Add the following line to your `.bash_profile` file:
```sh
alias openweather="python <your_path>/openweather.py"
```

## Usage

Invoke the CLI:

    openweather [-command] [-argument(s)]
    
The following commnads are supported: 

| Name | Arguments | Description |
| ---- | --------- | ----------- |
| `config`         | -  | Configurates the OpenWeather API Key 
| `current`            | -                | Show the current weather in a given city
| `forecast`          | `--results`, `-r`              | Show the forecast weather for the next 5 days each 3 hours in a given city


The following options are supported:

| Option | Type | Description |
| ---- | ----------- | ----------- |
| `--api-key`, `-a` | TEXT | Invoke a command with an specific API KEY
| `--celsius`, `-c` | FLAG | Show all the temperatures in celsius

### Examples
After executing `openweather -c current berlin` command the result should look something like this:
```sh
OpenWeather CLI ✨

City: Berlin 
Country: DE 

few clouds 🌤
 
Current Temperature: 8.49 
Max Temperature: 9.00 
Min Temperature: 8.00
```

And for this `openweather forecast london -r 4` command like this: 

```sh
OpenWeather CLI ✨

City: London 
Country: GB

Thursday 18h
light rain 🌦
Temperature: 280.77

Thursday 21h
clear sky ☀️
Temperature: 279.03

Friday 0h
scattered clouds 🌥
Temperature: 277.30

Friday 3h
clear sky ☀️
Temperature: 275.25
```