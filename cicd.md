

# 🚀 Automating Django REST API Deployment with CI/CD on a DigitalOcean Droplet

This guide explains how to automate deployment of a **Django REST API** running on a **DigitalOcean Droplet** using **GitHub Actions (CI/CD)**.

Once configured, every push to the `main` branch will automatically:
- pull the latest code on the server
- install dependencies
- run database migrations
- collect static files
- restart Gunicorn
- reload Nginx

No manual SSH deployments.

---

## 🧠 What CI/CD means (simple explanation)

**CI (Continuous Integration)**  
Automatically checks and prepares your code when you push changes.

**CD (Continuous Deployment)**  
Automatically updates your live server when those changes are ready.

In simple terms:

> **Push to GitHub → GitHub Actions → Server updates itself**

---

## ✅ Prerequisites

Before starting, you should already have:
- A **Django REST API deployed on a DigitalOcean Droplet**
- **Gunicorn** running as a systemd service
- **Nginx** configured as a reverse proxy
- A **non-root user** (e.g. `clinton`)
- Your project cloned on the droplet
- A GitHub repository for the project

---

## 1️⃣ Create a dedicated SSH key for CI/CD (local machine)

This SSH key will be used **only by GitHub Actions**, not for your personal SSH access.

On your local machine:

```bash
ssh-keygen -t ed25519 -C "github-actions-ci" -f github_actions_ci
````

This creates:

* `github_actions_ci` → **private key** (goes to GitHub Secrets)
* `github_actions_ci.pub` → **public key** (goes to the droplet)

---

## 2️⃣ Add the public key to the droplet (append, don’t replace)

SSH into your droplet as your non-root user:

```bash
ssh clinton@YOUR_SERVER_IP
```

Open the authorized keys file:

```bash
nano ~/.ssh/authorized_keys
```

Paste the **entire contents** of `github_actions_ci.pub` on a **new line**, then save.

Set correct permissions:

```bash
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys
```

> ⚠️ Important:
> Always **append** new keys. Do **not overwrite** this file or you may lock yourself out.

---

## 3️⃣ Allow passwordless service control (required for CI/CD)

GitHub Actions cannot type sudo passwords, so we explicitly allow the deploy user to restart Gunicorn and reload Nginx **without a password**.

### Check your Gunicorn service name

```bash
systemctl list-units --type=service | grep -i gunicorn
```

Example output:

```text
gunicorn.service
```

### Check your Nginx service name

```bash
systemctl status nginx
```

Example output:

```text
● nginx.service - A high performance web server and a reverse proxy server
     Loaded: loaded (/lib/systemd/system/nginx.service; enabled)
     Active: active (running)
```
👉 The service name is **`nginx.service`**


### Create a sudoers rule

```bash
sudo visudo -f /etc/sudoers.d/clinton-deploy
```

Add this line:

```bash
clinton ALL=(root) NOPASSWD: /bin/systemctl restart gunicorn.service, /bin/systemctl reload nginx.service
```

### Test it

```bash
sudo -n systemctl restart gunicorn.service
sudo -n systemctl reload nginx.service
```

If no errors appear, you’re good.

---

## 4️⃣ Create the deployment script on the droplet

This script defines **what happens during deployment**.

Create the file:

```bash
nano ~/deploy.sh
```

Example script:

```bash
#!/usr/bin/env bash
set -e

APP_DIR="/home/clinton/your-project-folder"
VENV_DIR="$APP_DIR/venv"

cd "$APP_DIR"

echo "Pulling latest code..."
git fetch --all
git reset --hard origin/main

echo "Installing dependencies..."
"$VENV_DIR/bin/pip" install -r requirements.txt

echo "Running database migrations..."
"$VENV_DIR/bin/python" manage.py migrate --noinput

echo "Collecting static files..."
"$VENV_DIR/bin/python" manage.py collectstatic --noinput

echo "Restarting Gunicorn..."
sudo -n systemctl restart gunicorn.service

echo "Reloading Nginx..."
sudo -n systemctl reload nginx.service

echo "Deployment completed successfully."
```

Make it executable:

```bash
chmod +x ~/deploy.sh
```

Test it manually:

```bash
bash ~/deploy.sh
```

---

## 5️⃣ Add GitHub Secrets

In your GitHub repository:

**Settings → Secrets and variables → Actions**

Add the following secrets:

* `DROPLET_HOST` → your server IP or domain
* `DROPLET_USER` → `clinton`
* `DROPLET_KEY` → contents of `github_actions_ci` (private key)

---

## 6️⃣ Create the GitHub Actions workflow

Create the file:

```text
.github/workflows/deploy.yml
```

Add:

```yaml
name: Deploy to DigitalOcean Droplet

on:
  push:
    branches: ["main"]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Deploy via SSH
        uses: appleboy/ssh-action@v1.2.0
        with:
          host: ${{ secrets.DROPLET_HOST }}
          username: ${{ secrets.DROPLET_USER }}
          key: ${{ secrets.DROPLET_KEY }}
          script: |
            bash ~/deploy.sh
```

---

## 🎉 Final Result

Now, every time you run:

```bash
git push origin main
```

Your server will automatically:

* update the code
* apply migrations
* restart Gunicorn
* reload Nginx

Your Django REST API is deployed **without manual SSH work**.

---

## 🔐 Security Notes

* Use **separate SSH keys** for CI/CD
* Never commit `.env` or secrets
* Do not give full sudo access
* Restrict CI permissions to only required services

---

## 📌 Final Thoughts

This CI/CD setup:

* reduces deployment mistakes
* saves time
* scales well
* reflects real production practices

This is a solid, professional deployment workflow for **Django REST APIs on VPS servers like DigitalOcean Droplets**.


