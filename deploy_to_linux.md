

---

# 🖥️ Initial Server Setup (Ubuntu)

In this section, we’ll set up a fresh Ubuntu server on DigitalOcean and prepare it for secure access.

## 1. Create a Droplet on DigitalOcean

Create a new droplet on DigitalOcean. For this tutorial, choose a **basic, low-cost plan** since we don’t need heavy infrastructure yet.

### ⚠️ Important: Use SSH Key Authentication

When selecting the authentication method, **choose SSH Key** instead of password authentication. This is more secure and recommended for production environments.

---

## 2. Generate an SSH Key (On Your Local Machine)

Open your terminal and run:

```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
```

When prompted:

* Press **Enter** to accept the default file location
* Press **Enter** again if you don’t want to set a passphrase (optional but recommended)

Once done:

* A `.ssh` folder will be created in your home directory
* Inside it, you’ll find:

  * `id_ed25519` → your **private key** (keep this safe!)
  * `id_ed25519.pub` → your **public key**

### View Your Public Key

Run:

```bash
cat ~/.ssh/id_ed25519.pub
```

Copy the output and paste it into the **SSH key** field when creating your droplet on DigitalOcean.

---

## 3. Log Into Your Server as Root

After the droplet is created, log in using:

```bash
ssh root@your_server_ip
```

### If You Have Multiple SSH Keys

You may need to specify the key explicitly:

```bash
ssh -i /path/to/private/key root@your_server_ip
```

---

## 4. Why You Shouldn’t Use Root Daily ⚠️

The `root` user has **full administrative privileges** on a Linux server. This means:

* It can modify or delete anything
* Mistakes can be catastrophic
* It’s a major security risk if compromised

For safety, you should **never** use root for daily work.

Instead, we’ll create a regular user with limited permissions and only elevate privileges when needed.

---

## 5. Create a New User

While logged in as `root`, run:

```bash
adduser clinton
```

> Replace `clinton` with any username you prefer.

You’ll be prompted to:

* Set a password (use a strong one)
* Optionally fill in extra details (you can skip these)

💡 **Important:** Don’t forget this password. You’ll need it later for administrative actions.

---



## 6. Grant Admin (sudo) Privileges to the New User

Right now, your new user has **regular permissions**. However, some tasks (like installing packages or editing system files) require **administrative access**.

On Ubuntu, users in the `sudo` group can run admin commands using `sudo`.

While logged in as `root`, run:

```bash
usermod -aG sudo clinton
```

> Replace `clinton` with your chosen username.

### What This Does

This allows your user to run admin commands like:

```bash
sudo apt update
sudo apt install nginx
```

Instead of logging in as root, you’ll now use `sudo` when needed — which is safer.

---

## 7. Set Up a Basic Firewall (UFW)

Ubuntu ships with a firewall called **UFW (Uncomplicated Firewall)**. We’ll configure it to only allow essential connections.

### Allow SSH

If you don’t do this, you could lock yourself out of the server.

```bash
ufw allow OpenSSH
```

### Enable the Firewall

```bash
ufw enable
```

When prompted, type `y` and press Enter.

💡 This blocks all other incoming connections except SSH.

---

## 8. Log In With Your Regular User (SSH Access)

Currently, your SSH key is only configured for the `root` user. We need to copy it to your new user so you can log in without a password.

Run this command **while still logged in as root**:

```bash
rsync --archive --chown=clinton:clinton ~/.ssh /home/clinton
```

> Replace `clinton` with your actual username.

### ⚠️ Important rsync Note

Do NOT add a trailing slash to the source directory.

❌ Wrong:

```bash
~/.ssh/
```

✅ Correct:

```bash
~/.ssh
```

Why?
A trailing slash changes how `rsync` copies files and can break SSH authentication.

---

## 9. Log In Using Your New User

Now open a **new terminal** on your local machine and run:

```bash
ssh clinton@your_server_ip
```

If everything was done correctly:

* You should log in **without a password**
* You’re now using your safer, regular user

---

## 10. Using sudo

Whenever you need admin permissions, prefix the command with `sudo`:

```bash
sudo apt update
```

The first time you use `sudo` in a session, you’ll be asked for your user password.

---

### ✅ At This Point, You Have:

* A secure Ubuntu server
* SSH key authentication
* A non-root user
* Firewall enabled
* sudo privileges

This is the foundation of any **production-ready server setup**.

---

# ⚙️ Set Up Django with PostgreSQL, Gunicorn, and Nginx on Ubuntu

In this section, we’ll install and configure the core components needed to run a Django app in production:

* **PostgreSQL** → production-grade database
* **Gunicorn** → application server for Django
* **Nginx** → reverse proxy + static file server

By the end of this section, your server will be ready to host real Django applications.

---

## 1. Install Required Packages

First, update your package list:

```bash
sudo apt update
```

Then install all required dependencies:

```bash
sudo apt install python3-venv python3-dev libpq-dev postgresql postgresql-contrib nginx curl
```

### What These Packages Are For

| Package              | Purpose                                   |
| -------------------- | ----------------------------------------- |
| `python3-venv`       | For creating isolated Python environments |
| `python3-dev`        | Required for compiling Python packages    |
| `libpq-dev`          | PostgreSQL development headers            |
| `postgresql`         | PostgreSQL database                       |
| `postgresql-contrib` | Extra PostgreSQL utilities                |
| `nginx`              | Web server and reverse proxy              |
| `curl`               | For testing HTTP endpoints                |

---

## 2. Create a PostgreSQL Database and User

Django works best with PostgreSQL in production. Let’s create a database and a user.

### Enter the PostgreSQL Shell

```bash
sudo -u postgres psql
```

---

### Create a Database

```sql
CREATE DATABASE myproject;
```

⚠️ **Note:** Every PostgreSQL command must end with a semicolon (`;`).

---

### Create a Database User

```sql
CREATE USER myprojectuser WITH PASSWORD 'password';
```

> ⚠️ Replace `'password'` with a strong, secure password.

---

## 3. Configure the Database User (Recommended for Django)

These settings match Django’s recommendations and improve consistency and performance.

```sql
ALTER ROLE myprojectuser SET client_encoding TO 'utf8';
ALTER ROLE myprojectuser SET default_transaction_isolation TO 'read committed';
ALTER ROLE myprojectuser SET timezone TO 'UTC';
```

---

## 4. Grant Permissions

Give the user full access to the database:

```sql
GRANT ALL PRIVILEGES ON DATABASE myproject TO myprojectuser;
```

Allow table creation in the public schema:

```sql
GRANT USAGE, CREATE ON SCHEMA public TO myprojectuser;
```

Make the user the database owner:

```sql
ALTER DATABASE myproject OWNER TO myprojectuser;
```

---

## 5. Exit PostgreSQL

```sql
\q
```

---

### ✅ At This Point

PostgreSQL is now properly configured for Django. You have:

* A production-grade database
* A dedicated database user
* Correct encoding and timezone settings
* Proper permissions

---


# 🚀 Preparing Your Django Project for Production

Before deploying, we need to make sure your Django project is properly configured for a production environment.

---

## 1. Update Your Django Settings for Production

Open your `settings.py` and verify the following:

### Required Production Settings

* `SECRET_KEY`
* `DEBUG`
* `STATIC_ROOT`
* `ALLOWED_HOSTS`
* Database config (PostgreSQL)

### Important Notes

* Add your **server IP address** to `ALLOWED_HOSTS`
* Temporarily set:

  ```python
  DEBUG = True
  ```

  This helps you see detailed error messages during deployment. We’ll disable it later.

Once you’re done, **push your changes to GitHub**.

---

## 2. Clone Your Project on the Ubuntu Server

Make sure you are in your home directory:

```bash
pwd
```

You should see something like:

```
/home/clinton
```

Now clone your repository:

```bash
git clone your_github_repo_url
```

If you don’t have a project, you can use mine:

```bash
git clone https://github.com/CodeWithClinton/deploy-practice-ii
```

---

## 3. GitHub Authentication (Important ⚠️)

GitHub no longer accepts account passwords for Git operations. You must use a **Personal Access Token (PAT)**.

### How to Generate a Token

1. Go to GitHub
2. Click your profile picture → **Settings**
3. **Developer settings**
4. **Personal access tokens**
5. **Tokens (classic)**
6. Click **Generate new token**

Use this token as your **password** when cloning or pulling from GitHub.

---

## 4. Create a Virtual Environment

Move into your project directory:

```bash
ls
cd deploy-practice-ii
```

Create a virtual environment:

```bash
python3 -m venv venv
```

Activate it:

```bash
source venv/bin/activate
```

Your terminal should now look like:

```
(venv) clinton@your_server_ip:~/deploy-practice-ii$
```

---

## 5. Install Project Dependencies

Install all packages from `requirements.txt`:

```bash
pip install -r requirements.txt
```

If these are missing, install them manually:

```bash
pip install gunicorn psycopg2-binary
```

---

## 6. Create a `.env` File

Still inside your project directory, run:

```bash
nano .env
```

Paste the contents of your local `.env` file.

Save and exit:

* Press **Ctrl + S** → Save
* Press **Ctrl + X** → Exit

---

## 7. Run Migrations

Make sure your virtual environment is active.

```bash
python manage.py makemigrations
python manage.py migrate
```

This creates the database tables inside PostgreSQL.

---

## 8. Create an Admin User

```bash
python manage.py createsuperuser
```

⚠️ Save these credentials. You’ll need them for the Django admin.

---

## 9. Collect Static Files

```bash
python manage.py collectstatic
```

This moves all static assets into the directory specified by `STATIC_ROOT`.

---

## 10. (Optional) Seed Sample Data

If you’re using my test project:

```bash
python manage.py seed_products
```

This populates the database with sample products and reviews.

---

### ✅ At This Stage, You Have:

* A cloned Django project
* Virtual environment set up
* Dependencies installed
* PostgreSQL connected
* Database migrated
* Admin user created
* Static files collected

---


# ▶️ Running and Testing Your Django Application

Before setting up Gunicorn and Nginx, let’s make sure your Django app runs correctly.

---

## 1. Open Port 8000 on the Firewall

If you followed the earlier steps, UFW is already active. Django’s development server runs on port `8000`, so we need to allow traffic to it.

```bash
sudo ufw allow 8000
```

---

## 2. Run the Django Development Server

Start the dev server:

```bash
python manage.py runserver 0.0.0.0:8000
```

Now open your browser and visit:

```
http://server_domain_or_IP:8000
```

Example:

```
http://134.122.101.50:8000
```

If you used my test project, you can log into the Django admin and explore the seeded products and reviews.

When you’re done testing, stop the server:

```text
CTRL + C
```

---

# 🧪 Testing Gunicorn

Now we’ll test whether **Gunicorn** can serve your Django app. This is important before automating it with systemd.

---

## 3. Run Gunicorn Manually

```bash
gunicorn --bind 0.0.0.0:8000 myproject.wsgi
```

Replace `myproject` with the name of the folder that contains your `wsgi.py` file.

Now visit:

```
http://server_domain_or_IP:8000
```

---

## 4. Port Already in Use?

If you get an error like:

> Address already in use

Allow another port:

```bash
sudo ufw allow 8001
```

Then run Gunicorn again on that port:

```bash
gunicorn --bind 0.0.0.0:8001 myproject.wsgi
```

Open:

```
http://server_domain_or_IP:8001
```

---

## 5. Missing Admin Styling? That’s Normal

You may notice the Django admin looks broken or unstyled. This is expected.

Gunicorn **does not serve static files** — that’s Nginx’s job. We’ll fix this later.

---

## 6. Stop Gunicorn and Deactivate venv

Stop Gunicorn:

```text
CTRL + C
```

Deactivate your virtual environment:

```bash
deactivate
```

---

# ⚙️ Configuring Gunicorn with systemd

You’ve confirmed that Gunicorn works. Now we’ll configure it to run automatically using **systemd**.

This setup:

* Starts Gunicorn automatically
* Restarts it if it crashes
* Uses socket-based activation
* Integrates with Nginx

---

## 7. Create a Gunicorn Socket File

```bash
sudo nano /etc/systemd/system/gunicorn.socket
```

Paste this:

```ini
[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/gunicorn.sock

[Install]
WantedBy=sockets.target
```

Save and exit:
**Ctrl + S**, then **Ctrl + X**

---

## 8. Create a Gunicorn Service File

```bash
sudo nano /etc/systemd/system/gunicorn.service
```

Paste this:

```ini
[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
User=clinton
Group=www-data
WorkingDirectory=/home/clinton/deploy-practice-ii
ExecStart=/home/clinton/deploy-practice-ii/venv/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/gunicorn.sock \
          review_summarizer.wsgi:application

[Install]
WantedBy=multi-user.target
```

⚠️ **Important:**
Do NOT copy this blindly. You must update:

* `User=clinton`
* `WorkingDirectory=...`
* Path to `gunicorn`
* `review_summarizer.wsgi:application`

To match your own project.

---

## 9. Start and Enable the Gunicorn Socket

```bash
sudo systemctl start gunicorn.socket
sudo systemctl enable gunicorn.socket
```

This ensures:

* Gunicorn starts automatically on boot
* It activates when Nginx sends a request

---

### ✅ At This Stage, You Have:

* Django tested and working
* Gunicorn tested
* systemd socket configured
* systemd service configured
* Gunicorn running in production mode

---


# 🔍 Verifying Gunicorn Socket Activation

Now that we’ve configured Gunicorn with systemd, we need to verify that everything is working correctly.

---

## 1. Check Gunicorn Socket Status

Run:

```bash
sudo systemctl status gunicorn.socket
```

You should see output similar to:

```
● gunicorn.socket - gunicorn socket
   Loaded: loaded (/etc/systemd/system/gunicorn.socket; enabled)
   Active: active (listening)
   Triggers: ● gunicorn.service
   Listen: /run/gunicorn.sock
```

This means the socket is active and waiting for connections.

---

## 2. Confirm the Socket File Exists

```bash
file /run/gunicorn.sock
```

Expected output:

```
/run/gunicorn.sock: socket
```

If this file is missing, Gunicorn was not set up correctly.

---

## 3. Troubleshooting Socket Issues

If the socket is not active or the file is missing, check the logs:

```bash
sudo journalctl -u gunicorn.socket
```

Then re-open and verify:

```bash
sudo nano /etc/systemd/system/gunicorn.socket
```

Fix any errors before continuing.

---

# 🧪 Testing Socket Activation

Gunicorn is currently configured to **start only when a request hits the socket**. That means it won’t be running yet.

Let’s confirm that.

---

## 4. Check Gunicorn Service Status

```bash
sudo systemctl status gunicorn
```

You should see something like:

```
Active: inactive (dead)
TriggeredBy: ● gunicorn.socket
```

This is expected.

---

## 5. Trigger Gunicorn Using curl

Now we’ll manually trigger the socket.

```bash
curl --unix-socket /run/gunicorn.sock localhost
```

If everything is working, you’ll see your Django app’s HTML output in the terminal.

This means:
✅ Socket is working
✅ Gunicorn started automatically
✅ Django app is being served

---

## 6. Confirm Gunicorn Is Now Running

```bash
sudo systemctl status gunicorn
```

You should now see:

```
Active: active (running)
```

This confirms Gunicorn was started by the socket.

---

# 🛠️ Troubleshooting Gunicorn

If something goes wrong, check Gunicorn logs:

```bash
sudo journalctl -u gunicorn
```

---

## 7. Reload systemd If You Make Changes

If you edit the Gunicorn service or socket files, you must reload systemd:

```bash
sudo systemctl daemon-reload
sudo systemctl restart gunicorn
```

---

### ✅ At This Point, You Have:

* Gunicorn socket activation working
* Gunicorn auto-starting on demand
* Django app responding correctly
* Logs accessible for debugging

---



# 🌐 Configure Nginx as a Reverse Proxy for Gunicorn

Now that Gunicorn is running correctly, we need Nginx to handle incoming web traffic and forward requests to Gunicorn.

Nginx will:

* Accept requests from users (HTTP)
* Forward them to Gunicorn
* Serve static files
* Improve security and performance

---

## 1. Create an Nginx Server Block

Create a new Nginx configuration file:

```bash
sudo nano /etc/nginx/sites-available/myproject
```

Paste the following configuration:

```nginx
server {
    listen 80;
    server_name server_domain_or_IP;

    location = /favicon.ico { 
        access_log off; 
        log_not_found off; 
    }

    location /static/ {
        alias /home/clinton/deploy-practice-ii/staticfiles/;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}
```

⚠️ **Important:**
Do NOT copy this blindly. You must update:

* `server_name`
* Your username (`clinton`)
* Your project directory path

Save and exit:
**Ctrl + S**, then **Ctrl + X**

---

## 2. Enable the Nginx Configuration

Create a symbolic link to enable the site:

```bash
sudo ln -s /etc/nginx/sites-available/myproject /etc/nginx/sites-enabled
```

---

## 3. Allow Nginx to Access Your Home Directory

```bash
sudo chmod 711 /home/clinton
```

> Replace `clinton` with your actual username.

This allows Nginx to access your project files.

---

## 4. Test Nginx Configuration

Before restarting Nginx, always test for syntax errors:

```bash
sudo nginx -t
```

If everything looks good, restart Nginx:

```bash
sudo systemctl restart nginx
```

---

## 5. Update Firewall Rules

We no longer need port `8000`, since traffic will now go through Nginx on port `80`.

Close port 8000:

```bash
sudo ufw delete allow 8000
```

Allow normal web traffic:

```bash
sudo ufw allow 'Nginx Full'
```

### What These Commands Do

* `sudo ufw delete allow 8000` → Closes the test port
* `sudo ufw allow 'Nginx Full'` → Opens ports **80** and **443**

---

## 6. Visit Your Site

Open your browser and go to:

```
http://your_server_ip
```

Your Django app should now load publicly through Nginx 🎉

---

# ✅ Deployment Complete (Without SSL)

At this point, your Django REST project is fully deployed using:

* Ubuntu (DigitalOcean Droplet)
* PostgreSQL
* Gunicorn
* systemd
* Nginx

This is a **real production-style setup**, not a toy deployment.

---

Next, we’ll:

➡️ Add SSL (HTTPS) with Let’s Encrypt
➡️ Set up automatic renewals
➡️ Harden security
➡️ Turn off DEBUG




