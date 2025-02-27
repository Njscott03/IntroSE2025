# Our Team
Caleb Stockton - cls1268 - Cable07 (backend)

Terrance Moncure - tdm594 - TJMonc (backend)

Chandler Bryant - ncb211 - steameam (frontend)

Noah Scott - njs283 - Njscott03 (frontend)

# Languages
We intend on using Django as our backend language and intend on either using Javascript or HTML for our frontend language.

# Objective
We’re building an e-commerce platform with Django (Python) on the backend, HTML/CSS/JavaScript on the frontend, and a SQLite database. Our system supports three types of users—Buyers, Sellers, and Admins—each with their own permissions and tools. Below is a  look at what we’re aiming to achieve and the main features that make our platform work.

# Features
1. **Account Management**
    - Create new accounts (Buyer, Seller, Admin).
    - Login/Logout securely.
    - Edit or Delete account details as needed.
2. **Buyer Role**
    - Search Products: Easily find items from a catalog of up to 50,000 products.
    - View Product Details: Click an item to see detailed information.
    - Shopping Cart: Add or remove products and proceed to checkout.
    - Order History & Refunds: Check past purchases and request refunds if necessary.
3. **Seller Role**
    - List & Manage Items: Add new products, remove existing ones, and edit product details.
    - Receive Payments: Automatically get "paid" when items are sold.
    - Refund Handling: Approve or deny buyer refund requests.
4. **Admin Role**
    - Approve/Block Users: Control who gets access to the platform.
    - Monitor Items & Transactions: Remove problematic listings and view or cancel transactions.
    - Refund Escalation: Manage refund requests that need higher-level attention.
5. **Shopping Cart & Orders**
    - Cart Table: Stores items before purchase and clears them on successful checkout.
    - Order Table: Keeps a record of every completed transaction for Buyers, Sellers, and Admins to review.
6. **Performance & Security**
    - Fast Responses: Searches, logins, and checkouts typically load within 2–3 seconds.
    - Concurrent Users: Handles up to 50 users at once and around 10 transactions per minute.
    - Role-Based Access: Ensures each role sees only what they need.
    - Session Management: Sessions expire after about 30 minutes to maintain security.
    - Regular Backups: Data is backed up every 1–2 weeks to prevent major losses.

   

