# Assignment 1. Multi-agent Pac-Man

## Files

Pac-Man project의 file 구조는 다음과 같다.

- `submission.py` : Where all of your multi-agent search agents will reside and the only file you need to concern yourself with for this assignment. Write your student Id and name at the top of this file. Rename the file to `submission studentid.py` before submission (Replace the studentid with your student ID).
- `pacman.py` : The main file that runs Pac-Man games. This file also describes a Pac-Man GameState type, which you will use extensively in this project
- `game.py` : The logic behind how the Pac-Man world works. This file describes several supporting types like AgentState, Agent, Direction, and Grid.
- `util.py` : Useful data structures for implementing search algorithms.
- `graphicsDisplay.py` : Graphics for Pac-Man
- `graphicsUtils.py` : Support for Pac-Man graphics
- `textDisplay.py` : ASCII graphics for Pac-Man
- `ghostAgents.py` : Agents to control ghosts
- `keyboardAgents.py` : Keyboard interfaces to control Pac-Man
- `layout.py` : Code for reading layout files and storing their contents

<br>

## Warm up

terminal에 `python pacman.py` 커멘드를 이용하여 Pac-Man game을 해보면서 룰 익히기!

`python pacman.py -p ReflexAgent` 커멘드를 이용하면 `submission.py`에 정의되어 있는 `ReflexAgent`에 의해 Pac-Man이 움직이도록 실행할 수 있다. `ReflexAgent`를 잘 참고하면 나중에 GameState를 query하는 로직을 작성할 때 도움이 됨.

### ReflexAgent(Agent)

Pac-Man이 움직일 수 있는 모든 action에 대해서 successor를 계산하여 그 중 max값을 택하는 방식.

<br>

<hr>

<br>

## Problem 1: Minimax

우선, 구현해야 하는 Pac-Man game의 경우 수업시간에 배운 minimax와 다르게 adversary(ghost)가 두 개이기 때문에 **알고리즘의 확장**이 필요하다. 기존 class는 하나의 min stage를 가지고 있는데, 이제 multi adversaries를 고려할 수 있도록 수정해야 한다. **특히 minimax tree가 모든 max layer마다 multiple min layer(ghost당 하나씩)를 가져야 한다.** 

a<sub>0</sub>부터 a<sub>n</sub>까지 n+1개의 agent가 있다고 생각하면, a<sub>0</sub>는 Pac-Man이고 나머지는 ghost이다. Pac-Man은 max agent로, ghost는 min agent로 움직이다. single depth에서 이 모든 n+1개의 agent가 한 번씩 움직인다고 생각하면 된다. `depth 2 == height of 2(n+1) minimax game tree`

### Minimax에 대해 알아보자!

(아마 다음 수업시간에 이야기 해주실 것 같음)

`max_value`를 찾는 부분에서 agent(여기서는 아마 Pac-Man)의 max 움직임을 구하고, `min_value`에서는 agent(maybe ghost)의 min값을 구해서 이 value들의 최댓값을 구하는 알고리즘인 것 같음.

### idea

multiple ghost를 어떻게 고려할 것인가! `min-value(state)` 함수를 모든 agent에 대해서 구한 다음에 그것들의 합의 최소를 골라내야 하나?

`calValue()`: 재귀적으로 terminate state까지 DFS를 불러서 score값을 계산(여기서는 value)

`maxValue()`: 각 action에 대한 max successor를 구함

`minValue()`: 각 action에 대한 min successor를 구함


<br>

## Problem 2: Alpha-beta pruning

[Alpha-Beta Pruning 참고영상](https://www.youtube.com/watch?v=xBXHtz4Gbdo)

Problem1의 로직과 거의 유사하게 구현했음.

특별히 고려한 점은 `maxValue()` 함수와 `minValue()` 함수에 대해서 alpha값과 beta값을 적절히 초기화해서 인자로 넘겨주었음

<br>

## Problem 3: Expectimax

모든 ghost의 action을 minimize하는 선택을 하지 않음. 대신 ghost의 움직임을 expactation한다. Ghost는 getLegalActions를 random하게 선택을 함.

### idea

확률 계산을 어떻게 해야하는걸까? :thinking:

`utils.py`에 `getProbability`는 관계없는 함수일까?

<br>

## Problem 4: Evaluation function

evaluate function을 보다 후하게(?) 짜는 것이 목표

`util.py`에 있는 어느 값이라도 가져다 쓰면 됨

### current evaluation function

`pacman.py`의 `getScore()` 함수를 호출한다. 

score값의 경우 `generateSuccessor()` 함수를 통해 업데이트된다.
