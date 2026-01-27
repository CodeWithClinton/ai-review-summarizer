


# 🔐 SSL (HTTPS) Setup for Django REST API on DigitalOcean (Beginner Guide)

This guide explains **how to enable SSL / HTTPS** for a **Django REST API deployed on a DigitalOcean Droplet** using **Nginx** and **Let’s Encrypt**.

It is written for **absolute beginners** — no prior SSL knowledge required.

---

## 📌 What is SSL and why do you need it?

SSL (also called TLS) is what enables **HTTPS**.

When SSL is enabled:

* 🔒 Data between users and your API is encrypted
* ✅ Browsers show the **lock icon**
* 🚫 Users don’t see “This site is not secure”
* 📱 Mobile apps and frontends can safely call your API
* 🔑 Authentication tokens and passwords are protected

Without SSL, **modern browsers and APIs will block or warn users**.

---

## 🧠 How SSL works (simple explanation)

1. A user visits `https://api.example.com`
2. The browser asks the server:
   *“Prove you are really api.example.com”*
3. The server presents an **SSL certificate**
4. The browser checks that:

   * The certificate matches the domain
   * It was issued by a trusted authority
   * It hasn’t expired
5. If valid → secure connection is established 🔒

We will use **Let’s Encrypt**, a free and trusted Certificate Authority.

---

## ✅ Prerequisites (VERY IMPORTANT)

Before installing SSL, make sure **all of these are true**:

### 1️⃣ You already deployed Django + Gunicorn + Nginx

Your API must already be reachable via HTTP.

Example:

```
http://api.example.com
```

Even a 404 page is fine — the key is that the domain reaches your server.

---

### 2️⃣ Your domain points to your Droplet IP

In your domain DNS settings:

* **A Record**
* Host: `api`
* Value: `YOUR_DROPLET_PUBLIC_IP`

DNS changes may take a few minutes to propagate.

---

### 3️⃣ Nginx server block uses the correct domain

Your Nginx config **must include**:

```nginx
server_name api.example.com;
```

Certbot uses this to know which domain to secure.

---

### 4️⃣ Firewall allows HTTP and HTTPS

```bash
sudo ufw allow 'Nginx Full'
sudo ufw status
```

---

## 🛠️ Step-by-Step SSL Setup (Recommended Method)

We’ll use **Certbot with Nginx**, which automates everything.

---

## Step 1 — SSH into your server

```bash
ssh youruser@YOUR_DROPLET_IP
```

---

## Step 2 — Install Certbot (official & recommended way)

```bash
sudo snap install core
sudo snap refresh core
sudo apt remove certbot -y
sudo snap install --classic certbot
sudo ln -s /snap/bin/certbot /usr/bin/certbot
```

---

## Step 3 — Run Certbot for your API domain

Replace `api.example.com` with your real domain:

```bash
sudo certbot --nginx -d api.example.com
```

Certbot will:

* Ask for your email
* Ask you to accept the terms
* Ask if you want to **redirect HTTP → HTTPS**
  👉 **Choose YES (recommended)**

---

## Step 4 — Reload Nginx

```bash
sudo systemctl reload nginx
```

---

## Step 5 — Verify HTTPS is working

Open in your browser:

```
https://api.example.com
```

You should see:

* 🔒 Lock icon
* No security warnings

---

## 🔄 Auto-Renewal (Very Important)

Let’s Encrypt certificates expire every **90 days**.

Certbot automatically installs a renewal timer, but always test it:

```bash
sudo certbot renew --dry-run
```

If this succeeds, your SSL will renew automatically forever.

---

## 🔍 Check installed certificates

```bash
sudo certbot certificates
```

---

## 📁 What Certbot changes behind the scenes

Certbot automatically:

* Adds an HTTPS (port 443) server block
* Configures SSL certificates
* Redirects HTTP → HTTPS
* Reloads Nginx safely

You **do NOT** need to manually edit SSL files.

---

## 🧠 Important Notes for Django REST APIs

* SSL is handled **entirely by Nginx**
* Django and Gunicorn do **not** need SSL config
* Works with:

  * Gunicorn socket (`unix:/run/gunicorn.sock`)
  * Gunicorn port (`127.0.0.1:8000`)

---

## 🚨 Common Errors & Fixes

### ❌ Certbot failed to authenticate

Usually caused by:

* Wrong DNS IP
* Domain not fully propagated
* Port 80 blocked
* Incorrect `server_name`

Fix DNS first, then retry.

---

### ❌ HTTPS works but frontend still fails

Make sure:

* Frontend uses `https://` API URL
* No hardcoded `http://` calls
* CORS settings allow your frontend domain

---

## 🔐 Best Practices (Optional but Recommended)

### Increase upload size (if API handles images/files)

```nginx
client_max_body_size 20M;
```

### Always force HTTPS

Certbot already does this if you choose redirect.

---

## ✅ Final Result

After completing this guide:

* Your API runs securely on HTTPS
* Browsers trust your domain
* Mobile apps and frontends work safely
* SSL renews automatically
* You’re production-ready 🚀


