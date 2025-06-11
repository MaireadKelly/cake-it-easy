# 🎂 Cake It Easy

A Django-based custom cake shop with ordering, optional accessories, admin control, and a sleek, responsive UI.

---

## ✨ Features

### Customer-Facing
- Browse products by category
- Filter by dietary preferences (vegan, gluten-free)
- Add cakes to basket with optional accessories
- User registration, login, and profile with order history
- Secure Stripe checkout flow
- Toasts and splash screen welcome modal

### Admin Features
- Product, category, and accessory management via admin panel
- Site settings (promo banners, contact info)
- Signal-based user profile creation and order handling

---

## 🧱 Tech Stack

- Django 4+
- PostgreSQL (via dj-database-url)
- Stripe Payments
- Crispy Forms + Bootstrap
- FontAwesome Icons

---

## 🚀 Setup Guide

See [`Run Local Guide`](./Run%20Local%20Guide.md) for full step-by-step local install.

---

## 🔧 Testing Plan

- Unit tests for models, forms, views
- Acceptance tests for:
  - Homepage splash modal
  - Add to cart flow
  - Profile and order history

---

## 📸 Screenshots

_Coming soon..._

---

## 📅 Roadmap / Milestones

- Setup & Infrastructure ✅
- Models, Admin, Fixtures ⏳
- Product Display & Basket
- Checkout & Stripe
- User Accounts
- Polish & Deploy
