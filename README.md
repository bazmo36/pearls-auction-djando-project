# 🐚 Pearl Auction 

A Django web application that allows users to post and showcase their **pearls**, upload **certifications**, and optionally list them for **auction every Thursday**. Users can **bid on pearls** during active auctions and manage their profiles.

---

## 🚀 Features

- **User Authentication**
  - Signup, Login, Logout
  - User Profiles with avatar and bio

- **Pearl Management**
  - Add, update, delete pearls
  - View pearls posted by others

- **Certification System**
  - Upload official certifications for pearls
  - Certification includes grade, certifier, and image

- **Weekly Auction System**
  - Users can choose to list pearls in auctions
  - Auctions are automatically scheduled to start every **Thursday**
  - Real-time countdown and dynamic bid validation
  - Bidding system with increment rules and reserve pricing
  - Auction status: Scheduled, Running, Closed, Sold

- **Dynamic Bid Logic**
  - Minimum bid increments based on current price
  - Validations to prevent owners from bidding on their own pearls
  - Auto-update of last bid time and auction status

---

## 🛠️ Tech Stack

- **Backend:** Django
- **Frontend:** HTML, CSS, JavaScript
- **Database:** SQLite (default, configurable)
- **User Auth:** Django’s built-in system
- **Media Management:** Image upload for pearls, avatars, and certificates
- **Countdown Logic:** Vanilla JavaScript (`countdown.js`)

---


## ⏳ Auction Logic

- **Schedule:**
  - Auctions always start on **Thursdays at 00:00** and end at **23:59** the same day.
  - Auction `start_time` and `end_time` are automatically calculated upon creation.

- **Status Types:**
  - `Scheduled` – Upcoming
  - `Running` – Currently Active
  - `Closed` – Time's up, not sold
  - `Sold` – Auction ended with a valid winner

- **Bid Rules:**
  - Only non-owners can bid
  - Minimum bid is auto-calculated
  - Price increment depends on current bid

---

## ✨ Highlights

- Clean separation of **CBVs (Class-Based Views)** for reusability
- Secure bidding and object-level permissions
- Rich profile management with media support
- Realtime countdown UI using `data-start` and `data-end` attributes

---

## 🔒 Permissions & Validations

- Only owners can modify or delete their pearls and certifications
- Pearls can only have one auction at a time
- Auction listings can be updated or deleted **only before** they start
- Auction participation restricted to **logged-in** users
- Bid form validates:
  - Auction is open
  - Bidder is not the owner
  - Bid meets the minimum increment


---

## 🧪 Optional Enhancements

- Email notifications for auction winners
- Admin dashboard for auction analytics
- Real-time bidding with Django Channels
- Pagination and filtering for pearls


