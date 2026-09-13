# Intent Taxonomy

This taxonomy was derived empirically from the `AmazonHelp` dataset using TF-IDF and KMeans clustering on the customer messages in the training set.

## 1. Order Status & Logistics
**Definition:** Issues related to delayed deliveries, missing packages, courier complaints, and tracking orders.
- **Inclusion criteria:** "delayed", "delivered", "driver", "where is my order", "tracking", "missing", "parcel"
- **Exclusion criteria:** "refund", "return", "prime subscription"
- **Example:** "My order #12345 was guaranteed for today but it's still not here!"

## 2. Returns, Refunds & Cancellations
**Definition:** Issues regarding canceling orders, returning items, or asking about the status of a refund.
- **Inclusion criteria:** "refund", "return", "cancel", "money back", "cashback"
- **Exclusion criteria:** "prime membership fee", "card declined"
- **Example:** "I cancelled my order 5 days ago and still haven't received my refund."

## 3. Account, Billing & Prime
**Definition:** Questions or issues about Amazon Prime subscriptions, account access, double charges, or general payment failures.
- **Inclusion criteria:** "prime", "charged", "subscription", "account", "payment", "login"
- **Exclusion criteria:** "refund for a returned item"
- **Example:** "I was charged for a Prime subscription even though I cancelled it last month."

## 4. Product Quality & Hardware
**Definition:** Complaints or questions about the quality of the product received (e.g., damaged items, Kindle issues, fake products).
- **Inclusion criteria:** "broken", "damaged", "fake", "quality", "kindle", "not working"
- **Exclusion criteria:** "missing package"
- **Example:** "I just received my book and the cover is completely torn."

## 5. Non-English Support
**Definition:** Customer messages in a language other than English (e.g., Spanish, French, German).
- **Inclusion criteria:** "que", "la", "el", "je", "est"
- **Exclusion criteria:** English text.
- **Example:** "¿Cómo puedo cancelar mi pedido?"

## 6. General Inquiry & Feedback
**Definition:** General questions about services, feature requests, or general positive/negative feedback not tied to a specific order failure.
- **Inclusion criteria:** "thank you", "how to", "discount", "festival"
- **Exclusion criteria:** Explicit complaints about delayed orders.
- **Example:** "When is the Great Indian Festival starting for Prime members?"
