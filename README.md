# The Santa Claus Problem – Concurrent Programming

This project implements a solution to the classical Santa Claus
synchronization problem, a well-known problem in concurrent programming.

The objective is to coordinate the interaction between Santa, elves,
and reindeer using synchronization mechanisms.

## Problem Description

The system must satisfy the following rules:

- Santa sleeps until awakened by either the reindeer or a group of elves.
- All reindeer must return before Santa prepares the sleigh.
- Elves can only wake Santa in groups of three.
- Reindeer have priority over elves.

## Implementation

The solution is implemented in Python using threads and shared
synchronization structures.

Each component of the system is represented as a separate module.

## Project Structure

main.py  
Entry point of the program.

santa.py  
Santa's behaviour and logic.

elf.py  
Implementation of elf threads.

reindeer.py  
Reindeer thread behaviour.

shared_data.py  
Shared synchronization structures and state.

## Concepts

- Concurrent programming
- Thread synchronization
- Classical synchronization problems
- Shared memory coordination

## Author

Sergio De Maria Saiz
