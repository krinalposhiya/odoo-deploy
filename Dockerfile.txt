FROM python:3.10

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    libpq-dev \
    libxml2-dev \
    libxslt-dev \
    libjpeg-dev \
    zlib1g-dev \
    libsasl2-dev \
    libldap2-dev \
    libssl-dev \
    libffi-dev \
    node-less \
    npm

# Create Odoo user
RUN useradd -m -d /opt/odoo -U -r -s /bin/bash odoo

# Set working directory
WORKDIR /opt/odoo

# Copy requirements and install Python packages
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# Copy official and custom addons
COPY official_addons /opt/odoo/official_addons
COPY custom /opt/odoo/custom

# Expose port
EXPOSE 8069

# Run Odoo
CMD ["python3", "odoo-bin", "-c", "odoo.conf"]
