 🏫 Campus Navigation System

A Python-based **Campus Navigation System** that helps users find the **shortest path between two locations** inside a campus.
It uses **Dijkstra’s Algorithm** to calculate the shortest distance and displays the recommended route.

---

 📌 Overview

Finding your way around a large campus can be confusing. This project provides a **graph-based navigation system** that models the campus as a set of locations (nodes) and pathways (edges with weights).
Given a **start point** and a **destination**, the system computes the **shortest path** and the **total distance**.

---

 ✨ Features

* 📍 Represents campus locations as a graph
* 🔗 Calculates the shortest path using **Dijkstra’s Algorithm**
* 🖥️ Console-based interaction (start & end locations entered by user)
* 📊 Displays route and total distance clearly
* 🛠 Easily customizable for **any campus or building map**

---

 🛠 Tech Stack

* **Language:** Python 3.x
* **Algorithm:** Dijkstra’s Shortest Path
* **Data Representation:** Adjacency List / Weighted Graph
* **Environment:** Works on any OS with Python installed

---

 📂 Project Structure

```
Campus_Navigation_System/
├── main.py          # Main program entry point
├── graph.py         # Graph & Dijkstra implementation (if modularized)
├── data/            # Campus map data (optional)
│   └── campus_map.csv
└── README.md        # Documentation
```

---

 ⚙️ Installation & Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/maksudrakib44/Campus_Navigation_System.git
   cd Campus_Navigation_System
   ```

2. **Run the program:**

   ```bash
   python main.py
   ```

3. **Follow prompts:**

   * Enter **start location**
   * Enter **destination**
   * Get the **shortest path + distance**

---

 🎮 Example Usage

```
Enter starting location: Library
Enter destination: Computer Lab

Shortest path: Library → Hallway → Main Building → Computer Lab
Total distance: 180 meters
```

---

 🚀 Future Enhancements

* 🗺️ Add a **GUI** or **Web interface** for interactive navigation
* 🧭 Integrate **A**\* or other pathfinding algorithms
* 📱 Mobile app version for real-time campus navigation
* 🎨 Visualize the campus map and highlighted path

---

 🤝 Contribution

Contributions are welcome!

1. Fork the repository
2. Create a branch (`feature-xyz`)
3. Commit your changes
4. Push and open a Pull Request

---

 📜 License

This project is released under the **MIT License**.
You are free to use, modify, and distribute it.

---
