# Parcel Management System

## Overview
The Parcel Management System is a Django-based web application designed to manage users, parcels, and related logistics. It allows users to register, track parcels, and manage their account details.

## Features

### User Management
- **User Registration**: Custom user model with fields for Georgian and Latin name formats, email authentication, and balance management.
- **User Login/Logout**: Standard login/logout functionality.
- **Address Management**: Users can view their static addresses in China and the USA.
- **Balance Management**: Users can update their balance.

### Parcel Management
- **Add Parcels**: Users can add new parcels with details such as tracking number, category, and price.
- **Update Parcel Status**: Parcel status updates to indicate progress, including `“გატანილია”` (Delivered).
- **Pay for Parcels**: Users can mark parcels as paid if their balance is sufficient.
- **Delete Parcels**: Users can delete their parcels if necessary.
- **Declaration**: Users can declare parcels with necessary details.

### Admin Management
- **Flight Management**: Admins can manage flights with automatic flight number generation.
- **Country Management**: Each country has transportation pricing and unique codes.
- **Category and Currency Management**: Manage parcel categories and currencies.

### Dynamic Calculations
- **Room Numbers**: Automatically generated room numbers for users starting with "SD".
- **Transporting Fees**: Dynamic calculation based on weight, country price, and exchange rates.
- **Custom Clearance**: Automatically flagged if parcel price exceeds the threshold.

## Installation

### Prerequisites
1. Python 3.8+
2. Django 4.2+
3. PostgreSQL (or any other preferred database backend)

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/tumana777/Solo_Delivery
   ```
2. Navigate to the project directory:
   ```bash
   cd parcel-management-system
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure the database in `settings.py`.
5. Apply migrations:
   ```bash
   python manage.py migrate
   ```
6. Run the development server:
   ```bash
   python manage.py runserver
   ```
7. Access the application at `http://127.0.0.1:8000`.

## Models

### CustomUser
- Fields: First name (Georgian and Latin), last name (Georgian and Latin), email, balance, personal ID, address, phone number, branch, room number.
- Custom save method: Generates unique room numbers.

### Parcel
- Fields: Tracking number, user, flight, country, category, price, currency, online store, branch, status, delivery and taken time, weight, custom clearance, declared status, transporting fee.
- Custom save method: Calculates transporting fee, flags custom clearance, and updates declaration status.

### Country
- Fields: Name, code, transporting price.

### Currency
- Fields: Name.

### Status
- Fields: Name.

### Flight
- Fields: Country, status, departure date, estimated arrival date, arrival date, flight number.
- Custom save method: Generates unique flight numbers based on country codes.

### Branch
- Fields: Name, address.

### ChinaAddress
- Fields: Country, address, street, district, city, province, zip code, cell phone.

### USAAddress
- Fields: Country, address, city, state, zip code, cell phone.

## Views

### User Views
- **UserRegistrationView**: Handles user registration.
- **UserAddressesView**: Displays user's China and USA addresses.
- **UserParcelsView**: Lists user's parcels with filtering by status.
- **UserBalanceUpdateView**: Updates user's balance.

### Parcel Views
- **AddParcelView**: Adds a new parcel.
- **ParcelStatusUpdateView**: Updates parcel status to `“გატანილია”` (Delivered).
- **ParcelPaidUpdateView**: Marks parcel as paid.
- **UserParcelDeclareView**: Updates parcel declaration details.
- **UserParcelDeleteView**: Deletes a parcel.

## URL Patterns
| URL                          | View                          | Description                  |
|------------------------------|-------------------------------|------------------------------|
| `/register/`                 | `UserRegistrationView`        | User registration page.      |
| `/login/`                    | `LoginView`                   | User login page.             |
| `/logout/`                   | `LogoutView`                  | User logout.                 |
| `/addresses/`                | `UserAddressesView`           | Display user addresses.      |
| `/room/parcels/`             | `UserParcelsView`             | List user parcels.           |
| `/parcel/<int:pk>/update/`   | `UserParcelDeclareView`       | Update parcel declaration.   |
| `/parcel/<int:pk>/delete/`   | `UserParcelDeleteView`        | Delete a parcel.             |
| `/add_parcel/`               | `AddParcelView`               | Add a new parcel.            |
| `/update_balance/`           | `UserBalanceUpdateView`       | Update user balance.         |
| `/parcel/<int:pk>/update_status/` | `ParcelStatusUpdateView` | Update parcel status.        |
| `/parcel/<int:pk>/update_paid/` | `ParcelPaidUpdateView`      | Mark parcel as paid.         |

## Templates
- **register.html**: User registration page.
- **login.html**: User login page.
- **addresses.html**: Displays user addresses.
- **room.html**: Lists parcels with filtering options.
- **add_parcel.html**: Add parcel form.

## Future Enhancements
1. Add notifications for parcel updates.
2. Implement admin dashboard for better management.
3. Enhance filtering options for parcels.

## License
This project is licensed under the MIT License.

