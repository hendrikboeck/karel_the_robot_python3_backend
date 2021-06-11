<p align="center"><img width=64px src="assets/64x/karel.png"></p>
<h1 align="center">Karel The Robot - Universal Backend</h1>

[![Codacy Badge](https://app.codacy.com/project/badge/Grade/ddbd2001e3184abe93073fc11b672712)](https://www.codacy.com/gh/hendrikboeck/karel_the_robot_python3_backend/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=hendrikboeck/karel_the_robot_python3_backend&amp;utm_campaign=Badge_Grade) ![Python](https://img.shields.io/badge/python-3.9+-blue.svg) [![License](https://img.shields.io/badge/license-GPL_v3.0-blue.svg)](https://opensource.org/licenses/GPL-3.0) [![GitHub release](https://img.shields.io/github/release/hendrikboeck/karel_the_robot_python3_backend.svg)](https://github.com/hendrikboeck/karel_the_robot_python3_backend/releases/) [![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://GitHub.com/hendrikboeck/karel_the_robot_python3_backend/graphs/commit-activity)

- [1. General](#1-general)
  - [1.1. Abstract](#11-abstract)
  - [1.2. Why this project exists?](#12-why-this-project-exists)
- [2. Using the PBE](#2-using-the-pbe)
  - [2.1. Downloading a Frontend](#21-downloading-a-frontend)
  - [2.2. Downloading PBE](#22-downloading-pbe)
  - [2.3. Building PBE](#23-building-pbe)
  - [2.4. Maps](#24-maps)
- [3. Frontends](#3-frontends)
  - [3.1. Create your own](#31-create-your-own)
  - [3.2. API](#32-api)
    - [3.2.1. Errors](#321-errors)
    - [3.2.2. Request (JSON)](#322-request-json)
    - [3.2.3. Response (JSON)](#323-response-json)
    - [3.2.4. Commands](#324-commands)

# 1. General

## 1.1. Abstract
Karel The Robot was invented in th 1970s by Richard E. Pattis at Standford Univeristy. Karel The Robot is a program, that should make the intruduction to coding for newcomers and beginners more simple. Its aim is to teach basic principles such as top-down programming and establish them from the beginning. Futhermore is learning programming with Karel The Robot a way more visual and rewarding experience then just printing out some strings and numbers onto the command-line.  

## 1.2. Why this project exists?
Since its original development in th 1970s many projects have replicated and improved on the originial idea. The biggest drawback of the original Karel The Robot is however, that he has its own programming-language. This is usefull if you primary focus is on establishing programmically thinking, as mentioned above. If there should however be taught a programming language besides that, Karel The Robot had to implemented in this language.

For this reason there is quite a limited number of ports of Karel The Robot to different programming languages. And even if there is a port of Karel The Robot for your programming language, cross system compatablility is quite rare. This is why I started this project. The cross system compatability of Python and pygame covers Linux, MacOS and Windows. The project will feature precompiled versions for all of those systems. Then you can choose a suitable Frontend for your language and if none exists you can easily and fast create one (see [3.1. Create your own](#31-create-your-own)).

# 2. Using the PBE

## 2.1. Downloading a Frontend

You can find a list of frontend under [3. Frontends](#3-frontends). Most frontends will provide a starter project for most systems and IDEs under the releases tab.

## 2.2. Downloading PBE

If you are creating a frontend or want to update your bundled PBE, than you can download a precompiled version of the PBE for your system under the [Releases](https://github.com/hendrikboeck/karel_the_robot_python3_backend/releases) tab. The downloaded directory will have the following structure. If you want to add maps just place your .xml-files in `PBE_PKG/assets/map`.

```
PBE_PKG
├── assets
│   ├── map
│   │   ├── 1x1.xml
│   │   ├── 1x8.xml
│   │   └── ...
│   └── pbe.yaml
├── karel_pbe
└── run_karel_pbe.sh
```

## 2.3. Building PBE

```sh
# clone the repo and cd into into it
git clone https://github.com/hendrikboeck/karel_the_robot_python3_backend.git
cd karel_the_robot_python3_backend

# create a virtual env and download dependecies
python3 -m venv env
./env/bin/activate
pip install -r requirements.txt

# build the project
pyinstaller karel_pbe.spec
```

Now you have to create a folder `assets` in the folder, where you want to execute `./karel_pbe`, and copy the file `assets/pbe.yaml` to your `assets` folder and your `.xml`-files into the `assets/map` folder.

## 2.4. Maps

New maps can be added by adding the file to the `assets/map` folder. If you want to create a new map use the following example: 

```xml
<?xml version="1.0" encoding="UTF-8"?>

<!-- DOCUMENT START -->
<map size="(10, 7)" speed="1.00">

  <!-- METADATA -->
  <metadata name="TestRoom" version="1.0" author="Hendrik Boeck" />

  <!-- MAP OBJECTS -->
  <karel position="(1, 2)" orientation="SOUTH" beeperbag="inf" />
  <wall start="(7, 1)" length="3" orientation="WEST" />
  <wall start="(7, 4)" length="4" orientation="SOUTH" />
  <beeper position="(8, 4)" n="2" />

</map>
<!-- DOCUMENT END -->
```

# 3. Frontends
| Language | Language Version | Project |
| -------- |:----------------:| ------- |
| Java | 11 =< | [hendrikboeck/karel_the_robot_java_frontend](https://github.com/hendrikboeck/karel_the_robot_java_frontend) |
| C | 99 =< | [hendrikboeck/karel_the_robot_c_frontend](https://github.com/hendrikboeck/karel_the_robot_c_frontend) |

## 3.1. Create your own
The project uses a websocket as its communication. It can be configured over the configuration (`assets/pbe.yaml`) file. The backend supports UDP as well as TCP-sockets. The commands use a variation of JSON-RPC as its format (more accurate information and all the commands can be found under [3.2. API](#32-api)). You dont have to check if an instance of the Karel is already running. The backend will not start if the port is occupied (this also means, do not use a port pre-occupied on your system).

## 3.2. API
The API uses json-encoded messages inspired by JSON-RPC v2. Every request to the server will need a autoincrementing `id` for identifying the corresponding response. If the request resembles a Karel-Action (e.g. `move`) or System-Update (e.g. `EOS`) the returned type will `null`; for Karel-Questions (e.g. `frontIsClear`) the returned type will be a `boolean`. If an error was thown in the backend the returned type will always be `string` identifying the error.

### 3.2.1. Errors
- `ActionExecutionError`: an Karel-Action could not be performed (e.g. "Karel hit a wall")
- `MapLoadingError`: map could not found or could not be read correctly
- `UnallowedActionError`: A command has been received, even though the game is already finished or another error, that was sent early, has been ignored.

### 3.2.2. Request (JSON)
```
{
    "id": 0,  // autoincrement
    "function": <functionname>,
    "args": <arguments>  
}
```

### 3.2.3. Response (JSON)
```
{
    "id": 0,  // same id as request
    "result": <return>
}
```

### 3.2.4. Commands
<dl>
  <dt>loadWorld</dt>
  <dd>
    loads a <code>mapname.xml</code> file as World into the game. (<code>mapname.xml</code> can eighter be loaded from local file in <code>assets/map/</code> or from a embedded maps in the exe).
  <ul>
    <li><i>arguments:</i> <code>dictionary</code>
    <ul><li>map: <code>string</code>, name of map that should be loaded</li></ul></li> 
    <li><i>return:</i> <code>null</code></li> 
  </ul>
  </dd>

  <dt>EOS</dt>
  <dd>
    terminates command sequence for backend. Has to be called as last command in program.
  <ul>
    <li><i>arguments:</i> <code>null</code></li> 
    <li><i>return:</i> <code>null</code></li> 
  </ul>
  </dd>

  <dt>move</dt>
  <dd>
    is a Karel-Action. Makes Karel move 1 tile forward in the direction he is looking at. If Karel can not execute <code>move</code> a <code>ActionExecutionError</code> is thrown.
  <ul>
    <li><i>arguments:</i> <code>null</code></li> 
    <li><i>return:</i> <code>null</code></li> 
  </ul>
  </dd>

  <dt>turnLeft</dt>
  <dd>
    is a Karel-Action. Makes Karel turn left.
  <ul>
    <li><i>arguments:</i> <code>null</code></li> 
    <li><i>return:</i> <code>null</code></li> 
  </ul>
  </dd>

  <dt>pickBeeper</dt>
  <dd>
    is a Karel-Action. Makes Karel pick a beeper from current position. If Karel can not execute <code>pickBeeper</code> a <code>ActionExecutionError</code> is thrown.
  <ul>
    <li><i>arguments:</i> <code>null</code></li> 
    <li><i>return:</i> <code>null</code></li> 
  </ul>
  </dd>

  <dt>putBeeper</dt>
  <dd>
    is a Karel-Action. Makes Karel put a beeper at current position. If Karel can not execute <code>putBeeper</code> a <code>ActionExecutionError</code> is thrown.
  <ul>
    <li><i>arguments:</i> <code>null</code></li> 
    <li><i>return:</i> <code>null</code></li> 
  </ul>
  </dd>

  <dt>frontIsClear</dt>
  <dd>
    is a Karel-Question. Returns wether there is a wall in front of Karel.
  <ul>
    <li><i>arguments:</i> <code>null</code></li> 
    <li><i>return:</i> <code>boolean</code></li> 
  </ul>
  </dd>

  <dt>rightIsClear</dt>
  <dd>
    is a Karel-Question. Returns wether there is a wall to the right of Karel.
  <ul>
    <li><i>arguments:</i> <code>null</code></li> 
    <li><i>return:</i> <code>boolean</code></li> 
  </ul>
  </dd>

  <dt>leftIsClear</dt>
  <dd>
    is a Karel-Question. Returns wether there is a wall to the left of Karel.
  <ul>
    <li><i>arguments:</i> <code>null</code></li> 
    <li><i>return:</i> <code>boolean</code></li> 
  </ul>
  </dd>

  <dt>beeperInBag</dt>
  <dd>
    is a Karel-Question. Returns wether Karel has at least one beeper left in his bag.
  <ul>
    <li><i>arguments:</i> <code>null</code></li> 
    <li><i>return:</i> <code>boolean</code></li> 
  </ul>
  </dd>

  <dt>beeperPresent</dt>
  <dd>
    is a Karel-Question. Returns wether at least one beeper is present on the position Karel is at.
  <ul>
    <li><i>arguments:</i> <code>null</code></li> 
    <li><i>return:</i> <code>boolean</code></li> 
  </ul>
  </dd>

  <dt>facingNorth</dt>
  <dd>
    is a Karel-Question. Returns wether Karel is currently facing north.
  <ul>
    <li><i>arguments:</i> <code>null</code></li> 
    <li><i>return:</i> <code>boolean</code></li> 
  </ul>
  </dd>

  <dt>facingEast</dt>
  <dd>
    is a Karel-Question. Returns wether Karel is currently facing east.
  <ul>
    <li><i>arguments:</i> <code>null</code></li> 
    <li><i>return:</i> <code>boolean</code></li> 
  </ul>
  </dd>

  <dt>facingSouth</dt>
  <dd>
    is a Karel-Question. Returns wether Karel is currently facing south.
  <ul>
    <li><i>arguments:</i> <code>null</code></li> 
    <li><i>return:</i> <code>boolean</code></li> 
  </ul>
  </dd>

  <dt>facingWest</dt>
  <dd>
    is a Karel-Question. Returns wether Karel is currently facing west.
  <ul>
    <li><i>arguments:</i> <code>null</code></li> 
    <li><i>return:</i> <code>boolean</code></li> 
  </ul>
  </dd>
</dl>