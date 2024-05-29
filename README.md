# Covid Essentials

![Covid Essentials](./static/logo.png)

**Covid Essentials** is a community-driven platform developed during the COVID-19 pandemic to help people in need by connecting them with essential resources like food, medicine, water, and more. This project empowers NGOs and government agencies to efficiently provide assistance by mapping the locations of individuals requiring help.

## Overview

### Features

- **Two-Factor Authentication**: Ensures secure access for users and NGOs using OTP.
- **Request Upload**: Users can upload their requirements (food, medicine, water, etc.).
- **Interactive Map**: Pinpoints the locations of those in need, making it easier for NGOs and government agencies to respond.
- **Resource Management**: Categorizes resources for efficient distribution.

## How It Works

1. **User Authentication**: Users sign up and authenticate using two-factor authentication for secure access.
2. **Requirement Upload**: Authenticated users upload their needs (e.g., food, medicine, water).
3. **Mapping Requests**: The platform pins the user’s location on an interactive map.
4. **Resource Allocation**: NGOs and government bodies access the map to identify and assist users in their vicinity.

## Tech Stack

- **Backend**: Python, Flask
- **Frontend**: HTML, CSS (Bootstrap), JavaScript (likely Leaflet.js for maps)
- **Database**: CSV for initial data
- **Authentication**: Two-Factor Authentication using OTP
- **Third-party Services**: Firebase for various services, Textlocal for SMS

## Getting Started

### Prerequisites

- Python
- Flask
- Firebase credentials

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Tayalarajan7/covid-essentials.git
   cd covid-essentials
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   Create a `.env` file in the root directory and add the following:
   ```env
   FIREBASE_CONFIG=path/to/your/firebase/config.json
   SECRET_KEY=your_secret_key
   ```

4. **Start the application**:
   ```bash
   python app.py
   ```

### Usage

1. **Sign Up**: Register and authenticate using two-factor authentication.
2. **Upload Requirements**: Post your needs such as food, water, or medicine.
3. **View Map**: See your request pinned on the map along with other users.
4. **NGO/Gov Response**: NGOs and government agencies can view the map and provide necessary assistance.

## Contributing

We welcome contributions from the community to enhance this project. To contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeature`).
3. Commit your changes (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Open a pull request.

## License

This project is licensed under the MIT License.

## Acknowledgements

- **Flask** for the web framework.
- **Leaflet.js** for the interactive maps.
- **Bootstrap** for styling.
- **Firebase** for backend services.
- **Textlocal** for SMS services.
- All the developers and volunteers who contributed to this project during the pandemic.

## Contact

For any inquiries or feedback, please contact:
- **Tayalarajan Ramanujadurai**: [LinkedIn](https://www.linkedin.com/in/tayalarajan-ramanujadurai/)

---
