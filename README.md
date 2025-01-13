# Car Finder Search Engine

## Overview
The **Car Finder Search Engine** is a powerful tool designed to help users search for vehicles using Boolean queries and ranked results based on advanced information retrieval techniques. The system leverages algorithms like **TF-IDF** and **BM25** for ranking, ensuring users receive the most relevant results. It features a user-friendly web interface built with Flask, making it intuitive for car buyers and enthusiasts to find their ideal vehicles.

---

## Features
- **Boolean Search**: Supports advanced queries using operators like `AND`, `OR`, and `NOT`.
- **Ranked Search**: Utilizes TF-IDF and BM25 to prioritize relevant documents.
- **Web Interface**: Easy-to-use, responsive interface for entering queries and viewing results.
- **Dynamic Results**: Displays car details such as make, model, price, fuel type, and images.

---

## Data Sources
The system uses data collected from the following sources:
- [Automobile Dimension](https://www.automobiledimension.com)
- [Honest John](https://www.honestjohn.co.uk/car-specs/)
- [Auto Data](https://www.auto-data.net/en/)
- [Cars Data](https://www.cars-data.com)
- [Car Photos](https://www.carwow.co.uk)

The dataset is preprocessed and stored in `cars.json`, including attributes like make, model, type, fuel type, price, and more.

---

## Key Components
1. **Inverted Index**:
   - Efficiently maps terms to the documents where they appear.
   - Enables fast Boolean and ranked searches.

2. **Ranking Algorithms**:
   - **TF-IDF**: Combines term frequency and inverse document frequency to rank results.
   - **BM25**: Adds document length normalization for better ranking precision.

3. **Web Interface**:
   - Built with Flask.
   - Allows users to input queries and view ranked results, including images of the cars.

---

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/car-finder-search-engine.git
   ```

2. Navigate to the project directory:
   ```bash
   cd car-finder-search-engine
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   python app.py
   ```

5. Open the browser and visit:
   ```
   http://127.0.0.1:5000/
   ```

---

## Usage
- Enter queries like `"Toyota Sedan"` or `"Electric Car"` in the search bar.
- View Boolean search results alongside ranked results using TF-IDF and BM25.
- Click on images for a better visual representation of the car.


---

## License
This project is licensed under the MIT License. See the `LICENSE` file for more information.

---
