

# MD5 Decryption Protocol Documentation

## Overview

This protocol enbales decryption requests, manage ranges of values to search, and results.

## Protocol Structure
- This protocol is text and keyword based,
- It uses simple and short keywords and parameters to explain what it needs,
- The client and server has different commands that they use.

## Message Definitions

### 1. Range Message

- **Purpose**: To inform the client of the range of values to search for the target MD5 hash.
- **Parameters**:
  - `start`: Integer representing the starting point of the range.
  - `end`: Integer representing the endpoint of the range.
  - `target`: String representing the MD5 hash to decrypt.
 - **Format**: `start-end,target`
 - **Example**: `1-100,5d41402abc4b2a76b9719d911017c592`

### 2. Stop Message

- **Purpose**: To signal the client to stop any ongoing processes related to decryption.
- **No parameters required**.
- **Format**: `stop`
- **Example**: `stop`

### 3. Request Message

- **Purpose**: To initiate a decryption request from the server and get a block.
- **No parameters required**.
- **Format**: `request`
- **Example**: `request`

### 4. Found Message

- **Purpose**: To notify the server that a solution has been found.
- **Parameters**:
  - `num`: Integer representing the result of the decryption attempt.
- **Format**: `found:num`
- **Example**: `found:42`

## Sequence Diagram

Below is the sequence diagram illustrating the interaction of the components in the MD5 Decryption Protocol.

```mermaid
sequenceDiagram
Client1 --> Server: request
Server --> Client1: 1-100,5d41402abc4b2a76b9719d911017c592`
Client2 --> Server: request
Server --> Client2: 101-200,5d41402abc4b2a76b9719d911017c592`
Client1 --> Server: found:42
Server --> Client2: stop