# teleinfo-app
Solución completa con frontend y backend para Teleinfo.

Instrucciones de despliegue en AWS Linux

    Preparar el servidor:

bash

# Conectarse al servidor
ssh -i "tu-key.pem" ubuntu@tu-ip-aws

# Actualizar el sistema
sudo apt update && sudo apt upgrade -y

# Instalar Python y pip
sudo apt install python3 python3-pip python3-venv -y

# Instalar Nginx
sudo apt install nginx -y

    Configurar la aplicación:

bash

# Crear directorio para la aplicación
sudo mkdir -p /var/www/teleinfo
sudo chown -R ubuntu:ubuntu /var/www/teleinfo

# Clonar o subir los archivos de la aplicación
cd /var/www/teleinfo
# Subir todos los archivos creados anteriormente

    Configurar entorno virtual:

bash

cd /var/www/teleinfo/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

    Configurar Nginx:

bash

# Crear configuración para la aplicación
sudo nano /etc/nginx/sites-available/teleinfo

Contenido del archivo de configuración:
nginx

server {
    listen 80;
    server_name tu-dominio.com;  # o la IP de tu servidor

    location / {
        root /var/www/teleinfo/frontend;
        index index.html;
        try_files $uri $uri/ =404;
    }

    location /api {
        include proxy_params;
        proxy_pass http://localhost:5000;
    }

    location /uploads {
        alias /var/www/teleinfo/backend/uploads;
    }
}

    Habilitar el sitio y reiniciar Nginx:

bash

sudo ln -s /etc/nginx/sites-available/teleinfo /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

    Configurar el servicio systemd para el backend:

bash

sudo nano /etc/systemd/system/teleinfo.service

Contenido del servicio:
ini

[Unit]
Description=Teleinfo Backend Service
After=network.target

[Service]
User=ubuntu
Group=ubuntu
WorkingDirectory=/var/www/teleinfo/backend
Environment="PATH=/var/www/teleinfo/backend/venv/bin"
ExecStart=/var/www/teleinfo/backend/venv/bin/python server.py

[Install]
WantedBy=multi-user.target

    Iniciar el servicio:

bash

sudo systemctl daemon-reload
sudo systemctl start teleinfo
sudo systemctl enable teleinfo

    Ajustar permisos:

bash

sudo chown -R ubuntu:ubuntu /var/www/teleinfo

    Abrir el firewall:

bash

sudo ufw allow 'Nginx Full'

Ahora tu aplicación estará disponible en la IP de tu servidor AWS. El admin puede iniciar sesión con usuario "admin" y contraseña "admin123", y el editor con "editor" y "editor123".

Recuerda cambiar las contraseñas en producción y configurar HTTPS para mayor seguridad.
