#pragma once

const string PYTHON_INTERPRETER = "C:/Users/griff/anaconda3/envs/tts/python.exe"; // Set to your python interpreter path

const int neededReinforcement = 3;
const int forgettingThreshold = 4;
const string PYTHON_SCRIPT = "tts/main.py"; 

const string RUN_PYTHON_SCRIPT = PYTHON_INTERPRETER + " " + PYTHON_SCRIPT + " ";